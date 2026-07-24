#!/usr/bin/env python3
"""Validate structural Lean-SDLC repository contracts."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/PROJECT_BRIEF.md",
    "docs/SCOPE.md",
    "docs/FEATURE_INDEX.csv",
    "docs/DECISION_INDEX.csv",
    "planning/tasks.csv",
    ".codex/hooks.json",
)
REQUIRED_DIRECTORIES = (
    "docs/features",
    "docs/decisions",
)

FEATURE_COLUMNS = {
    "feature_id",
    "name",
    "status",
    "actor",
    "outcome",
    "value_summary",
    "file",
    "version",
    "notes",
}
DECISION_COLUMNS = {
    "decision_id",
    "name",
    "status",
    "type",
    "impact_scope",
    "reversal_cost",
    "scope_ref",
    "file",
    "date",
    "notes",
}
TASK_COLUMN_ORDER = (
    "Task ID",
    "Title",
    "Status",
    "Parent",
    "Dependencies",
    "Owner",
    "Acceptance Criteria",
    "Proof",
    "Evidence",
)
TASK_COLUMNS = set(TASK_COLUMN_ORDER)
TASK_STATUSES = {"Planned", "In Progress", "Done"}
SPECIAL_PARENTS = {"REPO", "BOOTSTRAP"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Lean-SDLC files, indexes, task parents, and task structure."
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
        help="Require the selected task to be owned and In Progress before mutation",
    )
    return parser.parse_args()


def read_csv(
    root: Path,
    relative_path: str,
    required_columns: set[str],
    errors: list[str],
) -> list[dict[str, str]]:
    path = root / relative_path
    if not path.is_file():
        return []

    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            columns = set(fieldnames)
            missing = sorted(required_columns - columns)
            if missing:
                errors.append(f"{relative_path}: missing columns: {', '.join(missing)}")
                return []
            if (
                relative_path == "planning/tasks.csv"
                and fieldnames != list(TASK_COLUMN_ORDER)
            ):
                errors.append(
                    f"{relative_path}: columns must be exactly: "
                    f"{', '.join(TASK_COLUMN_ORDER)}"
                )
                return []
            return [
                {key: (value or "").strip() for key, value in row.items() if key is not None}
                for row in reader
                if any((value or "").strip() for value in row.values())
            ]
    except (OSError, csv.Error) as exc:
        errors.append(f"{relative_path}: cannot read CSV: {exc}")
        return []


def collect_ids(
    rows: list[dict[str, str]],
    id_column: str,
    relative_path: str,
    errors: list[str],
) -> set[str]:
    found: set[str] = set()
    for number, row in enumerate(rows, start=2):
        item_id = row.get(id_column, "")
        if not item_id:
            errors.append(f"{relative_path}:{number}: empty {id_column}")
        elif item_id in found:
            errors.append(f"{relative_path}:{number}: duplicate id {item_id}")
        else:
            found.add(item_id)
    return found


def validate_index_paths(
    root: Path,
    rows: list[dict[str, str]],
    relative_path: str,
    errors: list[str],
) -> None:
    for number, row in enumerate(rows, start=2):
        target_text = row.get("file", "")
        if not target_text:
            errors.append(f"{relative_path}:{number}: empty file path")
            continue
        target = (root / target_text).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            errors.append(f"{relative_path}:{number}: file escapes repository: {target_text}")
            continue
        if not target.is_file():
            errors.append(f"{relative_path}:{number}: missing indexed file: {target_text}")


def main() -> int:
    args = parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")

    errors: list[str] = []
    required_files = ("planning/tasks.csv",) if args.before_write else REQUIRED_FILES
    for relative_path in required_files:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")
    if not args.before_write:
        for relative_path in REQUIRED_DIRECTORIES:
            if not (root / relative_path).is_dir():
                errors.append(f"missing required directory: {relative_path}")

    features = read_csv(
        root, "docs/FEATURE_INDEX.csv", FEATURE_COLUMNS, errors
    )
    decisions = read_csv(
        root, "docs/DECISION_INDEX.csv", DECISION_COLUMNS, errors
    )
    tasks = read_csv(root, "planning/tasks.csv", TASK_COLUMNS, errors)

    feature_ids = collect_ids(
        features, "feature_id", "docs/FEATURE_INDEX.csv", errors
    )
    decision_ids = collect_ids(
        decisions, "decision_id", "docs/DECISION_INDEX.csv", errors
    )
    task_ids = collect_ids(tasks, "Task ID", "planning/tasks.csv", errors)

    validate_index_paths(root, features, "docs/FEATURE_INDEX.csv", errors)
    validate_index_paths(root, decisions, "docs/DECISION_INDEX.csv", errors)

    valid_parents = feature_ids | decision_ids | SPECIAL_PARENTS
    tasks_by_id: dict[str, dict[str, str]] = {}
    bootstrap_tasks = 0
    for number, task in enumerate(tasks, start=2):
        task_id = task.get("Task ID", "") or f"row {number}"
        if task.get("Task ID", ""):
            tasks_by_id[task_id] = task
        if not task.get("Title", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty title")
        status = task.get("Status", "")
        if status not in TASK_STATUSES:
            errors.append(
                f"planning/tasks.csv:{number}: {task_id} has invalid status {status!r}; "
                "expected Planned, In Progress, or Done"
            )
        parent = task.get("Parent", "")
        if not parent:
            errors.append(f"planning/tasks.csv:{number}: {task_id} has no parent")
        reserved_parent = bool(
            args.before_write
            and task_id == args.task
            and status == "In Progress"
            and re.fullmatch(r"(?:FEAT|DEC)-[A-Za-z0-9][A-Za-z0-9._-]*", parent)
        )
        if parent and parent not in valid_parents and not reserved_parent:
            errors.append(
                f"planning/tasks.csv:{number}: {task_id} has unknown parent {parent}"
            )
        if parent == "BOOTSTRAP":
            bootstrap_tasks += 1
        owner = task.get("Owner", "")
        if status == "Planned" and owner:
            errors.append(
                f"planning/tasks.csv:{number}: {task_id} is Planned but already has an owner"
            )
        if status in {"In Progress", "Done"} and not owner:
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty owner")
        if not task.get("Acceptance Criteria", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty acceptance")
        if not task.get("Proof", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty proof")
        if status == "Done" and not task.get("Evidence", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} is Done without evidence")

    if bootstrap_tasks > 1:
        errors.append("planning/tasks.csv: more than one BOOTSTRAP task exists")

    if args.task and args.task not in task_ids:
        errors.append(f"requested task does not exist: {args.task}")
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

    print(
        "Lean-SDLC structural check passed "
        f"({len(features)} features, {len(decisions)} decisions, {len(tasks)} tasks)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
