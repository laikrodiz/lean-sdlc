#!/usr/bin/env python3
"""Validate the small Lean-SDLC repository contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    PARENT_PATTERN,
    SPECIAL_PARENTS,
    TASK_COLUMNS,
    TASK_STATUSES,
    THREAD_OWNER_PATTERN,
    TaskError,
    integrity_errors,
    read_ledger,
    task_path,
)


REQUIRED_FILES = ("AGENTS.md", "docs/PROJECT.md", "tasks.csv", ".gitignore")
REQUIRED_IGNORES = {"/tasks.csv", "/.tasks.lock"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Lean-SDLC files, tasks, ownership, and dependencies."
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root (default: current directory)",
    )
    parser.add_argument("--task", help="Require and validate one task id")
    parser.add_argument("--owner", help="Require the selected task to have this owner")
    parser.add_argument(
        "--before-write",
        action="store_true",
        help="Require the selected task to be owned and In Progress",
    )
    return parser.parse_args()


def parent_document_exists(root: Path, parent: str) -> bool:
    folder = "features" if parent.startswith("FEAT-") else "decisions"
    directory = root / "docs" / folder
    if not directory.is_dir():
        return False
    return any(
        path.is_file()
        and (path.stem == parent or path.name.startswith(f"{parent}-"))
        for path in directory.iterdir()
    )


def main() -> int:
    args = parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")

    errors: list[str] = []
    required_files = ("tasks.csv",) if args.before_write else REQUIRED_FILES
    for relative_path in required_files:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    if not args.before_write and (root / ".gitignore").is_file():
        try:
            ignores = {
                line.strip()
                for line in (root / ".gitignore")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            }
        except OSError as exc:
            errors.append(f".gitignore: cannot read file: {exc}")
        else:
            for entry in sorted(REQUIRED_IGNORES - ignores):
                errors.append(f".gitignore: missing required entry {entry}")

    tasks: list[dict[str, str]] = []
    path = task_path(root)
    if path.is_file():
        try:
            columns, tasks = read_ledger(path)
            if columns != list(TASK_COLUMNS):
                errors.append(
                    "tasks.csv columns must be exactly: " + ", ".join(TASK_COLUMNS)
                )
        except TaskError as exc:
            errors.append(str(exc))

    for error in integrity_errors(tasks):
        errors.append(f"tasks.csv: {error}")

    tasks_by_id: dict[str, dict[str, str]] = {}
    bootstrap_tasks = 0
    for number, task in enumerate(tasks, start=2):
        task_id = task.get("Task ID", "") or f"row {number}"
        if task.get("Task ID"):
            tasks_by_id[task_id] = task
        if not task.get("Title"):
            errors.append(f"tasks.csv:{number}: {task_id} has empty title")

        status = task.get("Status", "")
        if status not in TASK_STATUSES:
            errors.append(
                f"tasks.csv:{number}: {task_id} has invalid status {status!r}; "
                "expected Planned, In Progress, or Done"
            )

        parent = task.get("Parent", "")
        if parent == "BOOTSTRAP":
            bootstrap_tasks += 1
        if not parent:
            errors.append(f"tasks.csv:{number}: {task_id} has no parent")
        elif parent not in SPECIAL_PARENTS and not PARENT_PATTERN.fullmatch(parent):
            errors.append(f"tasks.csv:{number}: {task_id} has invalid parent {parent}")
        elif (
            PARENT_PATTERN.fullmatch(parent)
            and status != "In Progress"
            and not parent_document_exists(root, parent)
        ):
            errors.append(
                f"tasks.csv:{number}: {task_id} has no document for parent {parent}"
            )

        owner = task.get("Owner", "")
        if status == "Planned" and owner:
            errors.append(f"tasks.csv:{number}: {task_id} is Planned but already owned")
        if status == "In Progress":
            valid_bootstrap = parent == "BOOTSTRAP" and owner == "bootstrap"
            if not valid_bootstrap and not THREAD_OWNER_PATTERN.fullmatch(owner):
                errors.append(
                    f"tasks.csv:{number}: {task_id} has invalid active owner "
                    f"{owner or '<empty>'}"
                )
        if status == "Done" and not owner:
            errors.append(f"tasks.csv:{number}: {task_id} has empty owner")

        if not task.get("Acceptance Criteria"):
            errors.append(f"tasks.csv:{number}: {task_id} has empty acceptance")
        if not task.get("Proof"):
            errors.append(f"tasks.csv:{number}: {task_id} has empty proof")
        if status == "Done" and not task.get("Evidence"):
            errors.append(f"tasks.csv:{number}: {task_id} is Done without evidence")

    if bootstrap_tasks > 1:
        errors.append("tasks.csv: more than one BOOTSTRAP task exists")

    if args.task and args.task not in tasks_by_id:
        errors.append(f"requested task does not exist: {args.task}")
    if args.owner and not args.task:
        errors.append("--owner requires --task TASK-ID")
    if args.before_write:
        if not args.task:
            errors.append("--before-write requires --task TASK-ID")
        if not args.owner:
            errors.append("--before-write requires --owner OWNER")
        elif args.task in tasks_by_id:
            selected = tasks_by_id[args.task]
            if selected.get("Status") != "In Progress":
                errors.append(f"{args.task} must be In Progress before mutation")
            if selected.get("Owner") != args.owner:
                errors.append(f"{args.task} is not owned by {args.owner}")

    if errors:
        print(f"Lean-SDLC check failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Lean-SDLC structural check passed ({len(tasks)} tasks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
