#!/usr/bin/env python3
"""Inject a stable short owner id for the current Codex thread."""

from __future__ import annotations

import hashlib
import json
import sys


def owner_id(session_id: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).digest()
    return f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"


def main() -> int:
    try:
        event = json.load(sys.stdin)
        session_id = event["session_id"]
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Lean-SDLC owner hook failed: {exc}", file=sys.stderr)
        return 1

    owner = owner_id(session_id)
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"Lean-SDLC Owner: {owner}. "
                    "Use it for task commands; subagents share it."
                )
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
