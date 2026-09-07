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

sys.dont_write_bytecode = True

from startup_contract import legacy_contract_error

STATE_VERSION = 2
DEFAULT_STATE = {
    "version": STATE_VERSION,
    "mode": "assisted",
    "fast_children": False,
    "active_mode": None,
}
MODES = frozenset({"assisted", "delegating", "solo"})
LEGACY_MODES = frozenset({"assisted", "solo"})
SCAN_DEPTH = 3
SCAN_EXCLUSIONS = frozenset(
    {".git", ".hg", ".svn", ".venv", "__pycache__", "build", "dist", "node_modules", "target", "vendor", "venv"}
)


def owner_id(session_id: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).digest()
    return f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"


def _is_lean_repository(candidate: Path) -> bool:
    agents = candidate / "AGENTS.md"
    if not agents.is_file() or not (candidate / "tasks.csv").is_file():
        return False
    try:
        instructions = agents.read_text(encoding="utf-8")
    except OSError:
        return False
    return "$lean-sdlc" in instructions or "Lean-SDLC" in instructions


def _descendant_repositories(root: Path) -> tuple[Path, ...]:
    candidates: set[Path] = set()
    for directory, names, files in os.walk(root):
        candidate = Path(directory).resolve()
        depth = len(candidate.relative_to(root).parts)
        names[:] = [
            name
            for name in names
            if depth < SCAN_DEPTH and name not in SCAN_EXCLUSIONS and not name.startswith(".")
        ]
        if "AGENTS.md" in files and "tasks.csv" in files and _is_lean_repository(candidate):
            candidates.add(candidate)
            names.clear()
    return tuple(sorted(candidates, key=str))


def _repository_resolution(cwd: str) -> tuple[Path | None, bool]:
    current = Path(cwd).resolve()
    for candidate in (current, *current.parents):
        if _is_lean_repository(candidate):
            return candidate, False
        if (candidate / ".git").exists():
            break

    descendants = _descendant_repositories(current)
    if len(descendants) == 1:
        return descendants[0], False
    return None, len(descendants) > 1


def lean_repository(cwd: str) -> Path | None:
    repository, _ = _repository_resolution(cwd)
    return repository


def skill_root() -> Path:
    loaded_skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    if not loaded_skill.is_file():
        raise ValueError(f"loaded SKILL.md is unavailable: {loaded_skill}")
    return loaded_skill.parent


class StateError(ValueError):
    """A saved state is missing, invalid, or cannot be migrated safely."""


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key, value in pairs:
        if key in values:
            raise StateError(f"saved state contains duplicate field {key!r}")
        values[key] = value
    return values


def _startup_context(
    session_id: str,
    cwd: str,
) -> tuple[dict[str, str | None] | None, bool]:
    repository, ambiguous = _repository_resolution(cwd)
    if repository is None:
        return None, ambiguous

    loaded_skill = skill_root()
    owner = owner_id(session_id)
    state = load_state(owner)
    tier = "Fast" if state["fast_children"] else "Standard"
    repository_root = str(repository)
    skill_path = str(loaded_skill)
    return {
        "repository_root": repository_root,
        "skill_root": skill_path,
        "tasks_helper": str(loaded_skill / "scripts/tasks.py"),
        "check_helper": str(loaded_skill / "scripts/lean_check.py"),
        "state_helper": str(loaded_skill / "scripts/session_state.py"),
        "owner": owner,
        "mode": str(state["mode"]),
        "active_mode": state["active_mode"],
        "tier": tier,
    }, False


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser()


def state_path(owner: str) -> Path:
    if not isinstance(owner, str) or not owner.isdigit() or len(owner) != 8:
        raise ValueError("owner must be an 8-digit string")
    return _codex_home() / "state" / "lean-sdlc" / f"{owner}.json"


def _state_values(
    *,
    version: int,
    mode: Any,
    fast_children: Any,
    active_mode: Any = None,
) -> dict[str, Any]:
    if not isinstance(version, int) or isinstance(version, bool) or version != STATE_VERSION:
        raise StateError(
            f"unsupported state version {version!r}; expected {STATE_VERSION}"
        )
    if not isinstance(mode, str) or mode not in MODES:
        raise StateError(f"invalid saved mode {mode!r}")
    if not isinstance(fast_children, bool):
        raise StateError("saved fast_children must be true or false")
    if active_mode is not None and (
        not isinstance(active_mode, str) or active_mode not in MODES
    ):
        raise StateError(f"invalid saved active_mode {active_mode!r}")
    if active_mode is not None and active_mode != mode:
        raise StateError(
            "saved mode differs from the active session mode; "
            "repair invalid state explicitly before changing mode"
        )
    return {
        "version": STATE_VERSION,
        "mode": mode,
        "fast_children": fast_children,
        "active_mode": active_mode,
    }


def _decode_state(value: Any) -> tuple[dict[str, Any], bool]:
    """Decode current state or migrate one exact legacy shape."""

    if not isinstance(value, dict):
        raise StateError("saved state must be a JSON object")

    version = value.get("version")
    if version is None:
        legacy_keys = set(value)
        if legacy_keys != {"mode", "fast_children"}:
            raise StateError(
                "saved state has no version and does not match the legacy schema"
            )
        legacy_mode = value["mode"]
        if not isinstance(legacy_mode, str) or legacy_mode not in LEGACY_MODES:
            raise StateError(f"invalid legacy saved mode {legacy_mode!r}")
        mode = "delegating" if legacy_mode == "assisted" else "solo"
        return (
            _state_values(
                version=STATE_VERSION,
                mode=mode,
                fast_children=value["fast_children"],
                active_mode=mode,
            ),
            True,
        )

    if version != STATE_VERSION:
        raise StateError(
            f"unsupported state version {version!r}; expected {STATE_VERSION}"
        )
    allowed_keys = {"version", "mode", "fast_children", "active_mode"}
    if set(value) != allowed_keys:
        if set(value) - allowed_keys:
            raise StateError("saved state contains unknown fields")
        raise StateError("saved state is missing required fields")
    return (
        _state_values(
            version=version,
            mode=value.get("mode"),
            fast_children=value.get("fast_children"),
            active_mode=value.get("active_mode"),
        ),
        False,
    )


def _read_state(owner: str) -> tuple[dict[str, Any], bool]:
    path = state_path(owner)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return DEFAULT_STATE.copy(), False
    except UnicodeError as exc:
        raise StateError(f"saved state is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise StateError(f"cannot read saved state: {exc}") from exc
    try:
        value = json.loads(text, object_pairs_hook=_object_pairs)
    except json.JSONDecodeError as exc:
        raise StateError(f"saved state is not valid JSON: {exc.msg}") from exc
    return _decode_state(value)


def load_state(owner: str, *, activate: bool = False) -> dict[str, Any]:
    """Load state, migrate exact legacy state, and optionally lock the mode."""

    state, migrated = _read_state(owner)
    if migrated:
        try:
            save_state(owner, state)
        except OSError as exc:
            raise StateError(f"cannot migrate saved state: {exc}") from exc
    if activate and state["active_mode"] is None:
        state["active_mode"] = state["mode"]
        try:
            save_state(owner, state)
        except OSError as exc:
            raise StateError(f"cannot lock active mode: {exc}") from exc
    return state


def save_state(owner: str, state: dict[str, Any]) -> Path:
    if not isinstance(state, dict):
        raise StateError("state must be a JSON object")
    allowed_keys = {"version", "mode", "fast_children", "active_mode"}
    if set(state) - allowed_keys:
        raise StateError("state contains unknown fields")
    valid = _state_values(
        version=state.get("version", STATE_VERSION),
        mode=state.get("mode"),
        fast_children=state.get("fast_children"),
        active_mode=state.get("active_mode"),
    )
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
    parser.add_argument(
        "--context",
        action="store_true",
        help="print exact startup repository, helper, owner, mode, and tier context",
    )
    parser.add_argument("--owner", help="eight-digit session owner")
    parser.add_argument("--mode", choices=sorted(MODES))
    parser.add_argument(
        "--begin",
        action="store_true",
        help="activate the selected mode before workflow work",
    )
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


def _run_context() -> int:
    session_id = os.environ.get("CODEX_SESSION_ID", "")
    if not session_id:
        raise ValueError("CODEX_SESSION_ID is unavailable")
    try:
        cwd = os.getcwd()
    except OSError as exc:
        raise ValueError(f"current working directory is unavailable: {exc}") from exc

    context, ambiguous = _startup_context(session_id, cwd)
    if context is None:
        if ambiguous:
            raise ValueError(
                "multiple Lean-SDLC repositories found below the current directory; "
                "focus one repository before continuing"
            )
        raise ValueError(
            "Lean-SDLC repository is unavailable from the current directory"
        )
    print(json.dumps(context))
    return 0


def _run_cli(arguments: argparse.Namespace) -> int:
    if arguments.context:
        if (
            arguments.owner is not None
            or arguments.mode is not None
            or arguments.begin
            or arguments.fast_children is not None
        ):
            raise ValueError(
                "--context cannot be combined with --owner, --mode, --begin, "
                "or child-tier options"
            )
        return _run_context()
    if arguments.owner is None:
        if (
            arguments.mode is not None
            or arguments.begin
            or arguments.fast_children is not None
        ):
            raise ValueError("--owner is required for a state update")
        return 0
    try:
        if arguments.begin:
            repository = lean_repository(os.getcwd())
            if repository is not None:
                error = legacy_contract_error((repository / "AGENTS.md").read_text(encoding="utf-8"))
                if error:
                    raise StateError(error)
        state = load_state(arguments.owner)
        if (
            arguments.mode is None
            and not arguments.begin
            and arguments.fast_children is None
        ):
            raise ValueError("set --mode, --begin, or --fast-children")
        mode_changed = arguments.mode is not None and arguments.mode != state["mode"]
        if arguments.mode is not None:
            active_mode = state["active_mode"]
            if active_mode is not None and arguments.mode != active_mode:
                if arguments.begin:
                    raise StateError(
                        "select the new mode without --begin; "
                        "load its instructions, then use --begin"
                    )
                state["active_mode"] = None
            state["mode"] = arguments.mode
        if arguments.begin:
            active_mode = state["active_mode"]
            if active_mode is not None and active_mode != state["mode"]:
                raise StateError(
                    "saved mode differs from the active session mode; "
                    "repair invalid state explicitly before changing mode"
                )
            state["active_mode"] = state["mode"]
        if arguments.fast_children is not None:
            state["fast_children"] = arguments.fast_children
        path = save_state(arguments.owner, state)
    except (OSError, StateError, ValueError) as exc:
        print(f"Lean-SDLC state update failed: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "owner": arguments.owner,
                **state,
                "path": str(path),
                "instruction_reload_required": mode_changed,
            }
        )
    )
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

    try:
        context, ambiguous = _startup_context(session_id, cwd)
    except StateError as exc:
        print(
            json.dumps(
                {
                    "continue": False,
                    "systemMessage": (
                        f"Lean-SDLC state error for Owner {owner_id(session_id)}: {exc}. "
                        "Do not continue until the state is repaired explicitly."
                    )
                }
            )
        )
        return 0
    if context is None:
        if ambiguous:
            print(
                json.dumps(
                    {
                        "continue": False,
                        "systemMessage": (
                            "Lean-SDLC found multiple repositories below this directory. "
                            "Focus one repository before continuing."
                        )
                    }
                )
            )
        return 0

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": (
                        f"Lean-SDLC Owner: {context['owner']}. "
                        f"Repository root: {context['repository_root']}. "
                        f"Skill root: {context['skill_root']}. "
                        f"Tasks helper: {context['tasks_helper']}. "
                        f"Check helper: {context['check_helper']}. "
                        f"State helper: {context['state_helper']}. "
                        f"Mode: {context['mode']}. Child tier: {context['tier']}. "
                        f"Active mode: {context['active_mode'] or 'none'}. "
                        "When Active mode is none, the requested mode can be selected before --begin. "
                        "Restore the latest request and selected mode contract before work. "
                        "Check repository rules for conflicting mode, ownership, or instruction paths before task creation or handoff. "
                        "Do not load an unselected mode to satisfy a legacy reference; stop affected work and request reconciliation. "
                        "For an explicit user mode change, stop conflicting work, select without --begin, "
                        "load the selected workflow instructions, then --begin in this session. "
                        "Use the latest saved selection after a mode change, not an earlier startup mode."
                    ),
                },
            }
        )
    )
    return 0


def main() -> int:
    arguments = _arguments()
    if arguments.context or arguments.owner is not None:
        try:
            return _run_cli(arguments)
        except (OSError, ValueError) as exc:
            print(f"Lean-SDLC startup context failed: {exc}", file=sys.stderr)
            return 2
    return _run_hook()


if __name__ == "__main__":
    raise SystemExit(main())
