#!/usr/bin/env python3
"""Validate Lean-SDLC Agent spawn arguments before execution."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from session_state import lean_repository, load_state, owner_id, repository_resolution
from task_ledger import TASK_ID_PATTERN, TaskError, find_task, read_ledger, task_path


GREEK_LABELS = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "omicron",
    "pi",
    "rho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega",
)
ROLE_PREFIXES = frozenset({"maintainer", "verifier", "scout"})
SUPPORT_MODEL = "gpt-6.2-sol"
SUPPORT_REASONING = "medium"
T3_DELEGATE = "mcp__t3_code_direct__delegate_task"
LABEL_PATTERN = re.compile(
    r"^(?P<prefix>[a-z0-9]+(?:_[a-z0-9]+)*)_(?P<label>"
    + "|".join(GREEK_LABELS)
    + r")$"
)


def _deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def _fork_turns_is_non_full_history(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value > 0
    if isinstance(value, str):
        return value.casefold() == "none" or value.isdigit() and int(value) > 0
    return False


def _validate_tool_input(tool_input: Any, fast_children: bool) -> str | None:
    if not isinstance(tool_input, dict):
        return "Provide Agent tool_input with a role-prefixed Greek task_name."

    task_name = tool_input.get("task_name")
    match = LABEL_PATTERN.fullmatch(task_name) if isinstance(task_name, str) else None
    if match is None:
        return "Set task_name to a role-prefixed Greek label, for example scout_beta."

    role, _, extra = match.group("prefix").partition("_")
    if role == "engineer":
        return "Use host-managed worktree isolation for authorized Engineers, never a shared Agent checkout."
    if role not in ROLE_PREFIXES:
        return None
    if extra:
        return f"Use only the support role and one Greek letter: {role}_{match.group('label')}."

    model = tool_input.get("model")
    reasoning_effort = tool_input.get("reasoning_effort")
    if model != SUPPORT_MODEL:
        return f"Set model to {SUPPORT_MODEL} for support roles. No automatic fallback is permitted."

    if reasoning_effort != SUPPORT_REASONING:
        return f"Set reasoning_effort to {SUPPORT_REASONING} for {model}."
    if "agent_type" in tool_input:
        return "Remove agent_type from direct native model spawns."
    if "fork_turns" not in tool_input or not _fork_turns_is_non_full_history(
        tool_input["fork_turns"]
    ):
        return "Set fork_turns to none or a positive non-full-history value."

    service_tier = tool_input.get("service_tier")
    if "service_tier" in tool_input:
        if service_tier != "priority":
            return "Omit service_tier for Standard children or set priority for Fast children."
        if not fast_children:
            return "Omit service_tier for the standard child tier, or enable Fast children first."
    return None


def _validate_t3(args: Any, root: Path, cwd: Path, owner: str) -> str | None:
    title = args.get("title") if isinstance(args, dict) else None
    if not isinstance(title, str):
        return "Set the T3 title to Role Greek or Engineer TASK-ID."
    role, _, suffix = title.partition(" ")
    if role == "Engineer" or args.get("role") == "implementation":
        if role != "Engineer" or not TASK_ID_PATTERN.fullmatch(suffix):
            return "Use Engineer followed by the exact ledger task ID."
        if args.get("isolation") != "worktree":
            return "Set isolation to worktree for an Engineer."
        target = args.get("target", {})
        if (cwd != root or not (root / ".git").exists() or not isinstance(target, dict)
                or "projectId" in target or "environmentId" in target):
            return "Launch the Engineer from the ledger repository root without a project or environment override."
        ledger = task_path(root)
        if ledger.is_symlink():
            return "Use the launch project's own task ledger."
        try:
            _, rows = read_ledger(ledger)
            row = find_task(rows, suffix)
        except (TaskError, UnicodeError) as exc:
            return f"Cannot confirm the Engineer task: {exc}"
        if row["Status"] != "In Progress" or row["Owner"] != owner:
            return f"{suffix} must be In Progress and owned by the assigning Lead."
        return None
    prefix, _, letter = title.rpartition(" ")
    if (not re.fullmatch(r"[A-Z][a-z0-9]*(?: [A-Z][a-z0-9]*)*", prefix)
            or letter.lower() not in GREEK_LABELS or letter != letter.capitalize()
            or role.lower() == "engineer" or (role.lower() in ROLE_PREFIXES and prefix != role)):
        return "Use the role and one Greek letter, such as Scout Beta."
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
        session_id = event["session_id"]
        cwd = event["cwd"]
        tool_input = event.get("tool_input")
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(cwd, str) or not cwd:
            raise ValueError("cwd must be a non-empty string")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Lean-SDLC spawn guard failed: {exc}", file=sys.stderr)
        return 2

    if event.get("tool_name") == T3_DELEGATE:
        current = Path(cwd).resolve()
        root, ambiguous = repository_resolution(cwd, require_ledger=False)
        if ambiguous:
            _deny("Select one Lean-SDLC repository before launching a T3 agent.")
            return 0
        if root is None:
            return 0
        error = _validate_t3(tool_input, root, current, owner_id(session_id))
    else:
        if lean_repository(cwd) is None:
            return 0
        state = load_state(owner_id(session_id))
        error = _validate_tool_input(tool_input, state["fast_children"])
    if error is not None:
        _deny(error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
