#!/usr/bin/env python3
"""Create the minimal Lean-SDLC control files without overwriting project work."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    TASK_COLUMNS,
    TaskError,
    find_task,
    ledger_lock,
    read_ledger,
    require_integrity,
    task_path,
    thread_owner,
    write_ledger,
)
from startup_contract import StartupContractError, read_template_block, repair_text


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
    parser.add_argument(
        "--repair-startup",
        "--repair",
        dest="repair_startup",
        action="store_true",
        help="Repair only the managed AGENTS.md startup block",
    )
    parser.add_argument("--task", help="Owned In Progress task authorizing repair")
    parser.add_argument("--owner", help="Owner of the authorizing task")
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


def atomic_replace_text(path: Path, content: str) -> None:
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


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


def authorize_repair(root: Path, args: argparse.Namespace) -> None:
    if not args.task or not args.owner:
        raise TaskError(
            "--repair-startup requires --task TASK-ID and --owner OWNER"
        )

    path = task_path(root)
    columns, rows = read_ledger(path)
    if columns != list(TASK_COLUMNS):
        raise TaskError("Existing tasks.csv has an unsupported header.")
    require_integrity(rows)
    selected = find_task(rows, args.task)
    if selected.get("Status") != "In Progress":
        raise TaskError(f"{args.task} must be In Progress before repair")
    try:
        owner = thread_owner(
            args.owner,
            allow_bootstrap=selected.get("Context") == "Bootstrap",
        )
    except TaskError as exc:
        raise TaskError(f"invalid repair owner: {exc}") from exc
    if selected.get("Owner") != owner:
        raise TaskError(f"{args.task} is not owned by {owner}")


def repair_startup(root: Path, args: argparse.Namespace) -> int:
    authorize_repair(root, args)
    target = root / "AGENTS.md"
    try:
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        replacement = read_template_block()
        repaired = repair_text(current, replacement)
    except (OSError, StartupContractError) as exc:
        raise TaskError(str(exc)) from exc

    if repaired == current:
        print("kept    AGENTS.md")
        print("Lean-SDLC startup repair complete: 0 control change(s).")
        return 0

    try:
        atomic_replace_text(target, repaired)
    except OSError as exc:
        raise TaskError(f"Cannot repair AGENTS.md: {exc}") from exc
    print("repaired AGENTS.md")
    print("Lean-SDLC startup repair complete: 1 control change(s).")
    return 0


def main() -> int:
    args = parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")
    if not args.repair_startup and (args.task or args.owner):
        raise SystemExit("--task and --owner require --repair-startup")

    try:
        with ledger_lock(root):
            if args.repair_startup:
                return repair_startup(root, args)
            return initialize(root)
    except TaskError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    raise SystemExit(main())
