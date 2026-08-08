#!/usr/bin/env python3
"""Restore and update the small amount of Lean-SDLC session state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_STATE = {"mode": "assisted", "fast_children": False}
MODES = frozenset({"assisted", "solo"})


def owner_id(session_id: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).digest()
    return f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"


def lean_repository(cwd: str) -> Path | None:
    current = Path(cwd).resolve()
    for candidate in (current, *current.parents):
        agents = candidate / "AGENTS.md"
        if agents.is_file() and (candidate / "tasks.csv").is_file():
            try:
                instructions = agents.read_text(encoding="utf-8")
            except OSError:
                return None
            if "$lean-sdlc" in instructions or "Lean-SDLC" in instructions:
                return candidate
        if (candidate / ".git").exists():
            break
    return None


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser()


def state_path(owner: str) -> Path:
    if not isinstance(owner, str) or not owner.isdigit() or len(owner) != 8:
        raise ValueError("owner must be an 8-digit string")
    return _codex_home() / "state" / "lean-sdlc" / f"{owner}.json"


def _valid_state(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    mode = value.get("mode")
    fast_children = value.get("fast_children")
    if mode not in MODES or not isinstance(fast_children, bool):
        return None
    return {"mode": mode, "fast_children": fast_children}


def load_state(owner: str) -> dict[str, Any]:
    try:
        path = state_path(owner)
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return DEFAULT_STATE.copy()
    valid = _valid_state(value)
    return valid if valid is not None else DEFAULT_STATE.copy()


def save_state(owner: str, state: dict[str, Any]) -> Path:
    valid = _valid_state(state)
    if valid is None:
        raise ValueError("state must contain a valid mode and fast_children flag")
    path = state_path(owner)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(valid, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
    return path


def _parse_bool(value: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on", "fast"}:
        return True
    if normalized in {"0", "false", "no", "off", "standard"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", help="eight-digit session owner")
    parser.add_argument("--mode", choices=sorted(MODES))
    parser.add_argument(
        "--fast-children",
        nargs="?",
        const=True,
        default=None,
        type=_parse_bool,
        metavar="BOOL",
        help="enable or disable the priority child tier",
    )
    parser.add_argument(
        "--no-fast-children",
        dest="fast_children",
        action="store_false",
        help="use the standard child tier",
    )
    return parser.parse_args()


def _run_cli(arguments: argparse.Namespace) -> int:
    if arguments.owner is None:
        return 0
    try:
        state = load_state(arguments.owner)
        if arguments.mode is None and arguments.fast_children is None:
            raise ValueError("set --mode or --fast-children")
        if arguments.mode is not None:
            state["mode"] = arguments.mode
        if arguments.fast_children is not None:
            state["fast_children"] = arguments.fast_children
        path = save_state(arguments.owner, state)
    except (OSError, ValueError) as exc:
        print(f"Lean-SDLC state update failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"owner": arguments.owner, **state, "path": str(path)}))
    return 0


def _run_hook() -> int:
    try:
        event = json.load(sys.stdin)
        session_id = event["session_id"]
        cwd = event["cwd"]
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(cwd, str) or not cwd:
            raise ValueError("cwd must be a non-empty string")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Lean-SDLC state hook failed: {exc}", file=sys.stderr)
        return 1

    if lean_repository(cwd) is None:
        return 0

    owner = owner_id(session_id)
    state = load_state(owner)
    tier = "Fast" if state["fast_children"] else "Standard"
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"Lean-SDLC Owner: {owner}. "
                    f"Mode: {state['mode']}. Child tier: {tier}. "
                    "After lifecycle restoration, reload subagents.md before Deliver."
                )
            }
        )
    )
    return 0


def main() -> int:
    arguments = _arguments()
    if arguments.owner is not None:
        return _run_cli(arguments)
    return _run_hook()


if __name__ == "__main__":
    raise SystemExit(main())
