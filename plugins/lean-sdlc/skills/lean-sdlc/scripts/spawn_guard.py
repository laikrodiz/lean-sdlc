#!/usr/bin/env python3
"""Validate Lean-SDLC Agent spawn arguments before execution."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

sys.dont_write_bytecode = True

from session_state import lean_repository, load_state, owner_id


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
ROLE_PREFIXES = frozenset({"engineer", "maintainer", "verifier", "scout"})
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


def _task_name_error(task_name: Any) -> str | None:
    if not isinstance(task_name, str):
        return "Set task_name to a role-prefixed Greek label, for example engineer_beta."
    match = LABEL_PATTERN.fullmatch(task_name)
    if match is None:
        return "Set task_name to a role-prefixed Greek label, for example engineer_beta."
    return None


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
    error = _task_name_error(task_name)
    if error is not None:
        return error

    task_prefix = LABEL_PATTERN.fullmatch(task_name).group("prefix").casefold()
    if tool_input.get("agent_type") == "lean_sdlc_luna":
        if task_prefix not in ROLE_PREFIXES:
            return "Use Engineer, Maintainer, Verifier, or Scout before the Greek label for Luna."
        if "model" in tool_input or "reasoning_effort" in tool_input:
            return "Remove direct model and reasoning fields from lean_sdlc_luna spawns."
        if "fork_turns" not in tool_input or not _fork_turns_is_non_full_history(
            tool_input["fork_turns"]
        ):
            return "Set fork_turns to none or a positive non-full-history value for Luna."

    service_tier = tool_input.get("service_tier")
    if service_tier == "priority" and not fast_children:
        return "Omit service_tier for the standard child tier, or enable Fast children first."
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
        return 1

    if lean_repository(cwd) is None:
        return 0

    owner = owner_id(session_id)
    state = load_state(owner)
    if state["mode"] == "solo":
        _deny("Solo mode is lead-only; restore Assisted mode before spawning an Agent.")
        return 0
    error = _validate_tool_input(tool_input, state["fast_children"])
    if error is not None:
        _deny(error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
