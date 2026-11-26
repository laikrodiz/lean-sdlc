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


DEFAULT_STATE = {"fast_children": False}
SCAN_DEPTH = 3
SCAN_EXCLUSIONS = frozenset(
    {".git", ".hg", ".svn", ".venv", "__pycache__", "build", "dist", "node_modules", "target", "vendor", "venv"}
)


def owner_id(session_id: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).digest()
    return f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"


def _has_lean_instructions(candidate: Path) -> bool:
    agents = candidate / "AGENTS.md"
    try:
        instructions = agents.read_text(encoding="utf-8")
    except OSError:
        return False
    return "$lean-sdlc" in instructions or "Lean-SDLC" in instructions


def _is_lean_repository(candidate: Path) -> bool:
    return (candidate / "tasks.csv").is_file() and _has_lean_instructions(candidate)


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


def repository_resolution(cwd: str, *, require_ledger: bool = True) -> tuple[Path | None, bool]:
    current = Path(cwd).resolve()
    for candidate in (current, *current.parents):
        if (_is_lean_repository(candidate) if require_ledger else _has_lean_instructions(candidate)):
            return candidate, False
        if (candidate / ".git").exists():
            break

    descendants = _descendant_repositories(current)
    if len(descendants) == 1:
        return descendants[0], False
    return None, len(descendants) > 1


def lean_repository(cwd: str) -> Path | None:
    repository, _ = repository_resolution(cwd)
    return repository


def skill_root() -> Path:
    loaded_skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    if not loaded_skill.is_file():
        raise ValueError(f"loaded SKILL.md is unavailable: {loaded_skill}")
    return loaded_skill.parent


def _startup_context(
    session_id: str,
    cwd: str,
) -> tuple[dict[str, str] | None, bool]:
    repository, ambiguous = repository_resolution(cwd)
    if repository is None:
        return None, ambiguous

    loaded_skill = skill_root()
    owner = owner_id(session_id)
    state = load_state(owner)
    tier = "Fast" if state["fast_children"] else "Standard"
    repository_root = str(repository)
    skill_path = str(loaded_skill)
    from startup_contract import contract_status
    from updates import load as load_policy, settings
    policy = load_policy(settings())
    status = contract_status(repository)
    return {
        **({"release_policy": "follow-stable"} if policy.get("follow") else {}),
        **({"contract_status": status} if status != "current" else {}),
        "repository_root": repository_root,
        "skill_root": skill_path,
        "tasks_helper": str(loaded_skill / "scripts/tasks.py"),
        "check_helper": str(loaded_skill / "scripts/lean_check.py"),
        "state_helper": str(loaded_skill / "scripts/session_state.py"),
        "owner": owner,
        "tier": tier,
    }, False


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser()


def state_path(owner: str) -> Path:
    if not isinstance(owner, str) or not owner.isdigit() or len(owner) != 8:
        raise ValueError("owner must be an 8-digit string")
    return _codex_home() / "state" / "lean-sdlc" / f"{owner}.json"


def _valid_state(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    fast_children = value.get("fast_children")
    if not isinstance(fast_children, bool):
        return None
    # Released state may contain mode; it never selects workflow behavior now.
    return {"fast_children": fast_children}


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
        raise ValueError("state must contain a boolean fast_children flag")
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
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--context",
        action="store_true",
        help="print exact startup repository, helper, owner, and child-tier context",
    )
    modes.add_argument("--recover-context", nargs=2, metavar=("PREVIOUS_REPO", "PREVIOUS_OWNER"),
                       help="validate recovered context against Codex plugin list JSON on stdin")
    parser.add_argument("--owner", help="eight-digit session owner")
    parser.add_argument(
        "--upgrade", action="store_true",
        help="remove retired state fields while preserving the child-tier preference",
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


def _verify_recovery(context: dict[str, str], repo: str, owner: str) -> None:
    from updates import stable

    if (repo, owner) != (context["repository_root"], context["owner"]):
        raise ValueError("repository or session owner changed; stop before writing")
    catalog = json.load(sys.stdin)
    rows = catalog.get("installed") if isinstance(catalog, dict) else None
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError("invalid installed plugin list")
    matches = [row for row in rows if row.get("pluginId") == "lean-sdlc@lean-sdlc"]
    if len(matches) != 1 or any(matches[0].get(k) is not True for k in ("enabled", "installed")):
        raise ValueError("expected one enabled Lean-SDLC installation")
    version = matches[0].get("version")
    if not isinstance(version, str) or not version.isascii() or version.startswith("v") or not stable(version):
        raise ValueError("unrecognized installed release version")
    package = _codex_home().resolve() / "plugins/cache/lean-sdlc/lean-sdlc" / version
    if Path(context["skill_root"]) != package / "skills/lean-sdlc":
        raise ValueError("loaded skill is not the selected installed version")
    manifest_path = package / ".codex-plugin/plugin.json"
    files = [manifest_path, Path(context["skill_root"]) / "SKILL.md",
             *(Path(context[key]) for key in ("tasks_helper", "state_helper", "check_helper"))]
    if any(not path.is_file() or path.resolve() != path for path in files):
        raise ValueError("recovered metadata or helper missing or redirected")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or (manifest.get("name"), manifest.get("version")) != ("lean-sdlc", version):
        raise ValueError("installed plugin manifest does not match")


def _run_context(recover: list[str] | None = None) -> int:
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
    if recover:
        _verify_recovery(context, *recover)
    print(json.dumps(context))
    return 0


def _run_cli(arguments: argparse.Namespace) -> int:
    if arguments.context or arguments.recover_context:
        if (
            arguments.owner is not None
            or arguments.upgrade
            or arguments.fast_children is not None
        ):
            raise ValueError(
                "--context cannot be combined with --owner, --upgrade, or child-tier options"
            )
        return _run_context(arguments.recover_context)
    if arguments.owner is None:
        return 0
    try:
        state = load_state(arguments.owner)
        if not arguments.upgrade and arguments.fast_children is None:
            raise ValueError("set --upgrade or --fast-children")
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

    context, ambiguous = _startup_context(session_id, cwd)
    if context is None:
        if ambiguous:
            print(
                json.dumps(
                    {
                        "systemMessage": (
                            "Lean-SDLC found multiple repositories below this directory. "
                            "Focus one repository before continuing."
                        )
                    }
                )
            )
        return 0

    message = (
        f"Lean-SDLC Owner: {context['owner']}. "
        f"Repository root: {context['repository_root']}. "
        f"Skill root: {context['skill_root']}. "
        f"Tasks helper: {context['tasks_helper']}. "
        f"Check helper: {context['check_helper']}. "
        f"State helper: {context['state_helper']}. "
        f"Child tier: {context['tier']}. "
        "Read SKILL.md and only the instructions for the current request or role. "
        "Discussion remains read-only. Recover current authority before resuming work."
    )
    if context.get("release_policy"):
        message += " Follow-stable enabled. Use references/ledger.md on authorized execution."
    if "contract_status" in context:
        message += f" Project contract: {context['contract_status']}. Consult references/ledger.md before writes."
    print(json.dumps({
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": message,
        },
    }))
    return 0


def main() -> int:
    arguments = _arguments()
    if arguments.context or arguments.recover_context or arguments.owner is not None or arguments.upgrade or arguments.fast_children is not None:
        try:
            if arguments.owner is None and not (arguments.context or arguments.recover_context):
                raise ValueError("state changes require --owner")
            return _run_cli(arguments)
        except (OSError, ValueError) as exc:
            print(f"Lean-SDLC startup context failed: {exc}", file=sys.stderr)
            return 2
    return _run_hook()


if __name__ == "__main__":
    raise SystemExit(main())
