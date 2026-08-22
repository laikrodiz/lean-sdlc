#!/usr/bin/env python3
"""Safely plan, start, update, close, and upgrade Lean-SDLC tasks."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    BACKLOG_FORBIDDEN_CONTEXTS,
    BACKLOG_STATUS,
    QUICK_FIX_CONTEXT,
    QUICK_FIX_PENDING_MARKER,
    TASK_COLUMNS,
    TaskError,
    append_evidence_marker,
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
    quick_fix_review_cursor,
    quick_fix_review_marker,
    unresolved_quick_fixes_through,
    task_path,
    task_context,
    thread_owner,
    sync_parent_directory,
    write_ledger,
)


DEFINITION_FIELDS = ("title", "context", "dependencies", "acceptance", "proof")
CONTEXT_HELP = "Valid context: Project, Bootstrap, Quick Fix, FEAT-*, or DEC-*."


def add_definition_arguments(
    command: argparse.ArgumentParser,
    *,
    required: bool,
) -> None:
    command.add_argument("--title", required=required)
    command.add_argument("--context", required=required, help=CONTEXT_HELP)
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

    backlog_add = subparsers.add_parser(
        "backlog-add",
        help="Create a sparse Backlog task",
    )
    backlog_add.add_argument("--title", required=True)
    backlog_add.add_argument("--context", default="Project", help=CONTEXT_HELP)

    update = subparsers.add_parser(
        "update",
        help="Correct a Backlog title/context, Planned task, "
        "or owned In Progress task",
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
    close.add_argument(
        "--review-through",
        help="Record shared review through one completed Quick Fix task",
    )

    subparsers.add_parser(
        "open",
        help="Print Planned and In Progress tasks",
    )

    subparsers.add_parser(
        "backlog",
        help="Print Backlog task titles and contexts",
    )

    subparsers.add_parser(
        "quick-fixes",
        help="Print completed Quick Fixes awaiting batch review",
    )

    promote = subparsers.add_parser(
        "promote",
        help="Promote one Backlog task to Planned or In Progress",
    )
    promote.add_argument("task_id")
    promote.add_argument("--to", choices=("planned", "in-progress"), required=True)
    promote.add_argument("--title")
    promote.add_argument("--context", help=CONTEXT_HELP)
    promote.add_argument("--dependencies")
    promote.add_argument("--owner")
    promote.add_argument("--acceptance", required=True)
    promote.add_argument("--proof", required=True)

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
            "Context": task_context(args.context or ""),
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


def backlog_context(value: str) -> str:
    context = task_context(value)
    if context in BACKLOG_FORBIDDEN_CONTEXTS:
        raise TaskError(
            f"Backlog tasks cannot use {context} context"
        )
    return context


def backlog_add_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task_id = next_task_id(rows)
    rows.insert(
        0,
        {
            "Task ID": task_id,
            "Title": clean(args.title, "Title"),
            "Status": BACKLOG_STATUS,
            "Context": backlog_context(args.context),
            "Dependencies": "",
            "Owner": "",
            "Acceptance Criteria": "",
            "Proof": "",
            "Evidence": "",
        },
    )
    return f"added {task_id} to Backlog"


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
        if task.get("Status") == BACKLOG_STATUS:
            raise TaskError(f"{args.task_id} is Backlog; promote it before start")
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
    if status == BACKLOG_STATUS:
        if args.owner:
            raise TaskError("Backlog update accepts only --title and --context")
        if any(
            getattr(args, field) is not None
            for field in ("dependencies", "acceptance", "proof")
        ):
            raise TaskError("Backlog update accepts only --title and --context")
        if args.title is None and args.context is None:
            raise TaskError("update requires at least one changed field")
        if args.title is not None:
            task["Title"] = clean(args.title, "Title")
        if args.context is not None:
            task["Context"] = backlog_context(args.context)
        return f"updated {args.task_id}"
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
    validated: dict[str, str] = {}
    for column, value in supplied.items():
        if column == "Context":
            validated[column] = task_context(value)
        elif column == "Dependencies":
            validated[column] = value.strip()
        else:
            validated[column] = clean(value, column)
    task.update(validated)
    return f"updated {args.task_id}"


def promote_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    if task.get("Status") != BACKLOG_STATUS:
        raise TaskError(f"{args.task_id} must be Backlog before promotion")

    context = (
        task_context(args.context)
        if args.context is not None
        else task_context(task.get("Context", ""))
    )
    if args.to == "planned":
        if args.owner is not None:
            raise TaskError("--owner is only required for --to in-progress")
        owner = ""
    else:
        if args.owner is None:
            raise TaskError("--owner is required for --to in-progress")
        owner = thread_owner(
            args.owner,
            allow_bootstrap=context == "Bootstrap",
        )

    task["Title"] = clean(
        args.title if args.title is not None else task.get("Title", ""),
        "Title",
    )
    task["Status"] = "Planned" if args.to == "planned" else "In Progress"
    task["Context"] = context
    task["Dependencies"] = (
        args.dependencies.strip()
        if args.dependencies is not None
        else ""
    )
    task["Owner"] = owner
    task["Acceptance Criteria"] = clean(args.acceptance, "Acceptance Criteria")
    task["Proof"] = clean(args.proof, "Proof")
    task["Evidence"] = ""

    if args.to == "in-progress":
        require_finished_dependencies(task, rows)
    return f"promoted {args.task_id} to {task['Status']}"


def close_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    if task.get("Status") != "In Progress":
        raise TaskError(f"{args.task_id} must be In Progress before it can close")

    require_finished_dependencies(task, rows)
    quick_fix_review_cursor(rows)

    review_target = None
    if args.review_through is not None:
        review_target = find_task(rows, args.review_through)
        if review_target.get("Context") != QUICK_FIX_CONTEXT:
            raise TaskError(
                f"review target {args.review_through} must have Quick Fix context"
            )
        is_self = review_target.get("Task ID") == task.get("Task ID")
        if not is_self and review_target.get("Status") != "Done":
            raise TaskError(
                f"review target {args.review_through} must be Done before review"
            )
        unresolved = unresolved_quick_fixes_through(
            rows,
            review_target.get("Task ID", ""),
            exempt_task_id=task.get("Task ID") if is_self else None,
        )
        if unresolved:
            raise TaskError(
                "review-through blocked by unresolved Quick Fix tasks: "
                + ", ".join(unresolved)
            )

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

    if task.get("Context") == QUICK_FIX_CONTEXT:
        evidence = append_evidence_marker(evidence, QUICK_FIX_PENDING_MARKER)
    if review_target is not None:
        evidence = append_evidence_marker(
            evidence,
            quick_fix_review_marker(review_target.get("Task ID", "")),
        )

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


def emit_backlog(rows: list[dict[str, str]]) -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=("Task ID", "Title", "Context"),
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)


def pending_quick_fixes(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cursor = quick_fix_review_cursor(rows)
    return [
        row
        for row in rows
        if row.get("Status") == "Done"
        and row.get("Context") == QUICK_FIX_CONTEXT
        and int(row.get("Task ID", "TASK--1").split("-", 1)[1]) > cursor
    ]


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
        sync_parent_directory(
            legacy.parent,
            success_message="legacy task ledger removal succeeded",
        )
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
        elif args.command in {"backlog", "open", "show", "quick-fixes"}:
            columns, rows = read_ledger(task_path(root))
            if columns != list(TASK_COLUMNS):
                raise TaskError("run tasks.py upgrade before reading tasks")
            require_integrity(rows)
            if args.command == "backlog":
                emit_backlog(
                    [row for row in rows if row.get("Status") == BACKLOG_STATUS]
                )
            elif args.command == "open":
                emit_rows(
                    [
                        row
                        for row in rows
                        if row.get("Status") in {"Planned", "In Progress"}
                    ]
                )
            elif args.command == "quick-fixes":
                emit_rows(pending_quick_fixes(rows))
            else:
                emit_rows(dependency_closure(rows, args.task_id))
        else:
            path = task_path(root)
            with ledger_lock(root):
                columns, rows = read_ledger(path)
                if columns != list(TASK_COLUMNS):
                    raise TaskError("run tasks.py upgrade before changing tasks")
                if args.command == "backlog-add":
                    message = backlog_add_task(args, rows)
                elif args.command == "promote":
                    message = promote_task(args, rows)
                elif args.command == "plan":
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
