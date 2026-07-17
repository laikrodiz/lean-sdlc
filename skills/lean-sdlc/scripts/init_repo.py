#!/usr/bin/env python3
"""Create the minimal Lean-SDLC control files without overwriting user work."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_BRIEF = """# Project Brief

## Problem

## Target User

## Intended Outcome and Value

## Constraints and Non-Goals

## Success Criteria
"""

SCOPE = """# Scope

## In Scope

## Out of Scope and Deferred

## Assumptions and Known Limitations

## Current Framing

- Stage: discovery
- Version: V0
- Version goal:
- Version exit criteria:
- Stage exit criteria:
"""

README = """# Project

This repository uses Lean-SDLC. Start with `docs/PROJECT_BRIEF.md` and `docs/SCOPE.md`.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create missing Lean-SDLC repository control files."
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root (default: current directory)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")

    skill_root = Path(__file__).resolve().parents[1]
    agents_template = (skill_root / "assets" / "AGENTS.md").read_text(encoding="utf-8")

    files = {
        Path("AGENTS.md"): agents_template,
        Path("README.md"): README,
        Path("docs/PROJECT_BRIEF.md"): PROJECT_BRIEF,
        Path("docs/SCOPE.md"): SCOPE,
        Path("docs/FEATURE_INDEX.csv"): (
            "feature_id,name,status,actor,outcome,value_summary,file,version,notes\n"
        ),
        Path("docs/DECISION_INDEX.csv"): (
            "decision_id,name,status,type,impact_scope,reversal_cost,scope_ref,file,date,notes\n"
        ),
        Path("planning/tasks.csv"): (
            "task_id,title,status,parent_ref,depends_on,acceptance\n"
        ),
    }

    for directory in ("docs/features", "docs/decisions", "planning"):
        (root / directory).mkdir(parents=True, exist_ok=True)

    created = 0
    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("x", encoding="utf-8", newline="") as handle:
                handle.write(content)
        except FileExistsError:
            print(f"kept    {relative_path}")
        else:
            print(f"created {relative_path}")
            created += 1

    print(f"Lean-SDLC initialization complete: {created} file(s) created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
