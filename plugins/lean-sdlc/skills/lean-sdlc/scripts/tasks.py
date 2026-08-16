#!/usr/bin/env python3
"""Safely plan, start, update, close, and upgrade Lean-SDLC tasks."""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    TASK_COLUMNS,
    TaskError,
    clean,
    current_rows,
    dependency_ids,
    directory_lock,
    find_task,
    ledger_lock,
    legacy_task_path,
    next_task_id,
    read_ledger,
    require_integrity,
    task_path,
    thread_owner,
    write_ledger,
)


DEFINITION_FIELDS = ("title", "context", "dependencies", "acceptance", "proof")


def add_definition_arguments(
    command: argparse.ArgumentParser,
    *,
    required: bool,
) -> None:
    command.add_argument("--title", required=required)
    command.add_argument("--context", required=required)
    command.add_argument("--dependencies", default="" if required else None)
    command.add_argument("--acceptance", required=required)
    command.add_argument("--proof", required=required)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Read or mutate the root tasks.csv ledger."
    )
    result.add_argument(
        "--repo",
        default=".",
        help="Repository root (default: current directory)",
    )
    subparsers = result.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser(
        "start",
        help="Create immediate work or claim an existing Planned task",
    )
    start.add_argument("task_id", nargs="?")
    start.add_argument("--owner", required=True)
    add_definition_arguments(start, required=False)

    plan = subparsers.add_parser("plan", help="Create an unowned Planned task")
    add_definition_arguments(plan, required=True)

    update = subparsers.add_parser(
        "update",
        help="Correct a Planned task or an owned In Progress task",
    )
    update.add_argument("task_id")
    update.add_argument("--owner")
    add_definition_arguments(update, required=False)

    close = subparsers.add_parser("close", help="Close an owned task with evidence")
    close.add_argument("task_id")
    close.add_argument("--owner", required=True)
    close.add_argument("--evidence", required=True)
    close.add_argument(
        "--user-override",
        action="store_true",
        help="Close another thread's task after a direct user request",
    )
    close.add_argument("--override-reason")

    subparsers.add_parser(
        "open",
        help="Print Planned and In Progress tasks",
    )

    show = subparsers.add_parser(
        "show",
        help="Print one task and its recursive dependencies",
    )
    show.add_argument("task_id")

    upgrade = subparsers.add_parser(
        "upgrade",
        help="Move a legacy planning/tasks.csv ledger to root tasks.csv",
    )
    upgrade.add_argument("--task", required=True)
    upgrade.add_argument("--owner", required=True)

    return result


def new_task(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
    *,
    status: str,
    owner: str,
) -> str:
    task_id = next_task_id(rows)
    rows.insert(
        0,
        {
            "Task ID": task_id,
            "Title": clean(args.title or "", "Title"),
            "Status": status,
            "Context": clean(args.context or "", "Context"),
            "Dependencies": (args.dependencies or "").strip(),
            "Owner": owner,
            "Acceptance Criteria": clean(
                args.acceptance or "",
                "Acceptance Criteria",
            ),
            "Proof": clean(args.proof or "", "Proof"),
            "Evidence": "",
        },
    )
    return task_id


def plan_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task_id = new_task(rows, args, status="Planned", owner="")
    return f"planned {task_id}"


def require_finished_dependencies(
    task: dict[str, str],
    rows: list[dict[str, str]],
) -> None:
    rows_by_id = {row.get("Task ID", ""): row for row in rows}
    unfinished = [
        dependency
        for dependency in dependency_ids(task.get("Dependencies", ""))
        if dependency in rows_by_id
        and rows_by_id[dependency].get("Status") != "Done"
    ]
    if unfinished:
        raise TaskError("unfinished dependencies: " + ", ".join(unfinished))


def start_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    owner = thread_owner(args.owner)
    if args.task_id:
        supplied_definition = [
            field for field in DEFINITION_FIELDS if getattr(args, field) is not None
        ]
        if supplied_definition:
            raise TaskError(
                "starting an existing task accepts only TASK-ID and --owner; "
                "use update first"
            )
        task = find_task(rows, args.task_id)
        if task.get("Status") != "Planned" or task.get("Owner"):
            raise TaskError(f"{args.task_id} must be unowned and Planned")
        require_finished_dependencies(task, rows)
        task["Status"] = "In Progress"
        task["Owner"] = owner
        return f"started {args.task_id} for owner {owner}"

    task_id = new_task(rows, args, status="In Progress", owner=owner)
    require_finished_dependencies(find_task(rows, task_id), rows)
    return f"started {task_id} for owner {owner}"


def require_owner(task: dict[str, str], supplied: str) -> str:
    allow_bootstrap = task.get("Context") == "Bootstrap"
    owner = thread_owner(supplied, allow_bootstrap=allow_bootstrap)
    actual = task.get("Owner", "")
    if actual != owner:
        raise TaskError(
            f"{task.get('Task ID', 'task')} belongs to owner {actual or '<none>'}, "
            f"not {owner}"
        )
    return owner


def update_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    status = task.get("Status")
    if status == "In Progress":
        if not args.owner:
            raise TaskError("--owner is required for an In Progress task")
        require_owner(task, args.owner)
    elif status == "Planned":
        if task.get("Owner"):
            raise TaskError(f"{args.task_id} is Planned but already owned")
        if args.owner:
            thread_owner(args.owner)
    else:
        raise TaskError(f"{args.task_id} is Done and cannot be updated")

    changes = {
        "Title": args.title,
        "Context": args.context,
        "Dependencies": args.dependencies,
        "Acceptance Criteria": args.acceptance,
        "Proof": args.proof,
    }
    supplied = {column: value for column, value in changes.items() if value is not None}
    if not supplied:
        raise TaskError("update requires at least one changed field")
    for column, value in supplied.items():
        task[column] = value.strip() if column == "Dependencies" else clean(value, column)
    return f"updated {args.task_id}"


def close_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    if task.get("Status") != "In Progress":
        raise TaskError(f"{args.task_id} must be In Progress before it can close")

    require_finished_dependencies(task, rows)

    supplied_owner = thread_owner(
        args.owner,
        allow_bootstrap=task.get("Context") == "Bootstrap",
    )
    actual_owner = task.get("Owner", "")
    if actual_owner != supplied_owner:
        if not args.user_override:
            require_owner(task, supplied_owner)
        reason = clean(args.override_reason or "", "Override reason")
        evidence = (
            f"{clean(args.evidence, 'Evidence')} "
            f"[Direct user override: {reason}]"
        )
    else:
        if args.user_override:
            raise TaskError("--user-override is unnecessary for the task owner")
        if args.override_reason:
            raise TaskError("--override-reason requires --user-override")
        evidence = clean(args.evidence, "Evidence")

    task["Status"] = "Done"
    task["Evidence"] = evidence
    return f"closed {args.task_id}"


def dependency_closure(
    rows: list[dict[str, str]],
    task_id: str,
) -> list[dict[str, str]]:
    rows_by_id = {row.get("Task ID", ""): row for row in rows}
    selected = find_task(rows, task_id)
    ordered: list[dict[str, str]] = []
    visited: set[str] = set()

    def visit(task: dict[str, str]) -> None:
        current_id = task.get("Task ID", "")
        if current_id in visited:
            return
        visited.add(current_id)
        ordered.append(task)
        for dependency in dependency_ids(task.get("Dependencies", "")):
            visit(rows_by_id[dependency])

    visit(selected)
    return ordered


def emit_rows(rows: list[dict[str, str]]) -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=TASK_COLUMNS,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)


def authorize_upgrade(
    rows: list[dict[str, str]],
    task_id: str,
    owner: str,
) -> None:
    task = find_task(rows, task_id)
    if task.get("Status") != "In Progress":
        raise TaskError(f"{task_id} must be In Progress before upgrade")
    if task.get("Owner") != clean(owner, "Owner"):
        raise TaskError(f"{task_id} is not owned by {owner}")


def upgrade_ledger(root: Path, args: argparse.Namespace) -> str:
    destination = task_path(root)
    legacy = legacy_task_path(root)
    legacy_exists = legacy.is_file()

    with directory_lock(root / ".tasks.lock"):
        if legacy_exists:
            with directory_lock(legacy.parent / ".tasks.lock"):
                message = _upgrade_locked(destination, legacy, args)
        else:
            message = _upgrade_locked(destination, legacy, args)

    if legacy.parent.is_dir():
        try:
            legacy.parent.rmdir()
        except OSError:
            pass
    return message


def _upgrade_locked(
    destination: Path,
    legacy: Path,
    args: argparse.Namespace,
) -> str:
    sources = [path for path in (destination, legacy) if path.is_file()]
    if not sources:
        raise TaskError("no tasks.csv ledger exists to upgrade")

    loaded: list[tuple[Path, list[str], list[dict[str, str]]]] = []
    for source in sources:
        columns, rows = read_ledger(source, allow_legacy=True)
        loaded.append((source, columns, current_rows(columns, rows)))

    authorize_upgrade(loaded[0][2], args.task, args.owner)
    require_integrity(loaded[0][2])

    if len(loaded) == 2 and loaded[0][2] != loaded[1][2]:
        raise TaskError(
            "tasks.csv and planning/tasks.csv differ; reconcile them before upgrade"
        )

    source, columns, rows = loaded[0]
    changed = source != destination or columns != list(TASK_COLUMNS) or legacy.is_file()
    if not changed:
        return "task ledger already uses root tasks.csv"

    write_ledger(destination, rows)
    if legacy.is_file():
        legacy.unlink()
        try:
            directory = os.open(legacy.parent, os.O_RDONLY)
        except OSError:
            pass
        else:
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    return "upgraded task ledger to root tasks.csv"


def main() -> int:
    args = parser().parse_args()
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(
            f"Task operation failed: repository directory does not exist: {root}",
            file=sys.stderr,
        )
        return 1

    message: str | None = None
    try:
        if args.command == "upgrade":
            message = upgrade_ledger(root, args)
        elif args.command in {"open", "show"}:
            columns, rows = read_ledger(task_path(root))
            if columns != list(TASK_COLUMNS):
                raise TaskError("run tasks.py upgrade before reading tasks")
            require_integrity(rows)
            if args.command == "open":
                emit_rows(
                    [
                        row
                        for row in rows
                        if row.get("Status") in {"Planned", "In Progress"}
                    ]
                )
            else:
                emit_rows(dependency_closure(rows, args.task_id))
        else:
            path = task_path(root)
            with ledger_lock(root):
                columns, rows = read_ledger(path)
                if columns != list(TASK_COLUMNS):
                    raise TaskError("run tasks.py upgrade before changing tasks")
                if args.command == "plan":
                    message = plan_task(args, rows)
                elif args.command == "start":
                    message = start_task(args, rows)
                elif args.command == "update":
                    message = update_task(args, rows)
                else:
                    message = close_task(args, rows)
                require_integrity(rows)
                write_ledger(path, rows)
    except (TaskError, OSError) as exc:
        print(f"Task operation failed: {exc}", file=sys.stderr)
        return 1

    if message is not None:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
