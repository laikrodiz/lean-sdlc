#!/usr/bin/env python3
"""Create the minimal Lean-SDLC control files without overwriting project work."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    TASK_COLUMNS,
    TaskError,
    ledger_lock,
    read_ledger,
    task_path,
    write_ledger,
)


PROJECT = """# Project

## Problem and User

## Intended Outcome and Value

## Scope

### In

### Out or Deferred

## Constraints and Assumptions

## Success Criteria

## Current Promise

- Stage: Discovery
- Version: V0
- Version goal:
- Exit evidence:
"""

BOOTSTRAP_TASK = {
    "Task ID": "TASK-000",
    "Title": "Initialize Lean-SDLC",
    "Status": "In Progress",
    "Context": "Bootstrap",
    "Dependencies": "",
    "Owner": "bootstrap",
    "Acceptance Criteria": (
        "AGENTS.md, docs/PROJECT.md, and root tasks.csv exist without "
        "overwriting project work"
    ),
    "Proof": "Run lean_check.py --task TASK-000",
    "Evidence": "",
}
IGNORE_ENTRIES = ("/tasks.csv", "/.tasks.lock")


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


def missing_ignore_entries(root: Path) -> list[str]:
    path = root / ".gitignore"
    if not path.is_file():
        return list(IGNORE_ENTRIES)
    try:
        present = {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except OSError as exc:
        raise SystemExit(f"Cannot read .gitignore: {exc}") from exc
    return [entry for entry in IGNORE_ENTRIES if entry not in present]


def update_gitignore(root: Path, missing: list[str]) -> str:
    if not missing:
        return "kept"
    path = root / ".gitignore"
    existed = path.is_file()
    try:
        content = path.read_text(encoding="utf-8") if existed else ""
        if content and not content.endswith("\n"):
            content += "\n"
        content += "\n".join(missing) + "\n"
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Cannot update .gitignore: {exc}") from exc
    return "updated" if existed else "created"


def initialize(root: Path) -> int:
    skill_root = Path(__file__).resolve().parents[1]
    files = {
        Path("AGENTS.md"): (skill_root / "assets" / "AGENTS.md").read_text(
            encoding="utf-8"
        ),
        Path("docs/PROJECT.md"): PROJECT,
    }
    missing = [relative for relative in files if not (root / relative).is_file()]
    missing_ignore = missing_ignore_entries(root)
    ledger = task_path(root)
    task_created = False

    if not ledger.is_file():
        if (root / "planning" / "tasks.csv").is_file():
            raise SystemExit(
                "Legacy planning/tasks.csv exists. Run tasks.py upgrade first."
            )
        write_ledger(ledger, [BOOTSTRAP_TASK])
        print("created tasks.csv with active TASK-000")
        task_created = True
    else:
        try:
            columns, rows = read_ledger(ledger)
        except TaskError as exc:
            raise SystemExit(str(exc)) from exc
        if columns != list(TASK_COLUMNS):
            raise SystemExit("Existing tasks.csv has an unsupported header.")
        active_control_task = any(
            row.get("Status") == "In Progress"
            and row.get("Owner")
            and row.get("Context") in {"Bootstrap", "Project"}
            for row in rows
        )
        if (missing or missing_ignore) and not active_control_task:
            raise SystemExit(
                "Missing control files require an owned In Progress "
                "Bootstrap or Project task."
            )

    created = 1 if task_created else 0
    ignore_action = update_gitignore(root, missing_ignore)
    print(f"{ignore_action:7} .gitignore")
    if ignore_action != "kept":
        created += 1

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

    print(f"Lean-SDLC initialization complete: {created} control change(s).")
    return 0


def main() -> int:
    args = parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")

    try:
        with ledger_lock(root):
            return initialize(root)
    except TaskError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    raise SystemExit(main())
