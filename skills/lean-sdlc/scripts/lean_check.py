#!/usr/bin/env python3
"""Validate structural Lean-SDLC repository contracts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/PROJECT_BRIEF.md",
    "docs/SCOPE.md",
    "docs/FEATURE_INDEX.csv",
    "docs/DECISION_INDEX.csv",
    "planning/tasks.csv",
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
TASK_COLUMNS = {
    "task_id",
    "title",
    "status",
    "parent_ref",
    "depends_on",
    "acceptance",
}
TASK_STATUSES = {"planned", "in_progress", "done"}


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
            columns = set(reader.fieldnames or [])
            missing = sorted(required_columns - columns)
            if missing:
                errors.append(f"{relative_path}: missing columns: {', '.join(missing)}")
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
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")
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
    task_ids = collect_ids(tasks, "task_id", "planning/tasks.csv", errors)

    validate_index_paths(root, features, "docs/FEATURE_INDEX.csv", errors)
    validate_index_paths(root, decisions, "docs/DECISION_INDEX.csv", errors)

    valid_parents = feature_ids | decision_ids
    for number, task in enumerate(tasks, start=2):
        task_id = task.get("task_id", "") or f"row {number}"
        if not task.get("title", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty title")
        status = task.get("status", "")
        if status not in TASK_STATUSES:
            errors.append(f"planning/tasks.csv:{number}: {task_id} has invalid status {status!r}")
        parent = task.get("parent_ref", "")
        if not parent:
            errors.append(f"planning/tasks.csv:{number}: {task_id} has no parent_ref")
        elif parent not in valid_parents:
            errors.append(
                f"planning/tasks.csv:{number}: {task_id} has unknown parent_ref {parent}"
            )
        if not task.get("acceptance", ""):
            errors.append(f"planning/tasks.csv:{number}: {task_id} has empty acceptance")

    if args.task and args.task not in task_ids:
        errors.append(f"requested task does not exist: {args.task}")

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
