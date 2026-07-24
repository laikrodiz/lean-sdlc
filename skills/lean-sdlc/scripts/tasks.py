#!/usr/bin/env python3
"""Safely mutate the Lean-SDLC task ledger."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


TASK_COLUMNS = (
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
LEGACY_COLUMNS = (
    "task_id",
    "title",
    "status",
    "parent_ref",
    "depends_on",
    "owner",
    "acceptance",
    "proof",
    "evidence",
)
LEGACY_TO_CURRENT = dict(zip(LEGACY_COLUMNS, TASK_COLUMNS))
TASK_ID_PATTERN = re.compile(r"TASK-(\d+)$")
THREAD_OWNER_PATTERN = re.compile(r"\d{8}$")
LOCK_TIMEOUT_SECONDS = 10
STALE_LOCK_SECONDS = 60


class TaskError(Exception):
    """A user-correctable task ledger error."""


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Create, claim, update, close, or migrate Lean-SDLC tasks safely."
    )
    result.add_argument(
        "--repo",
        default=".",
        help="Repository root (default: current directory)",
    )
    subparsers = result.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a Planned or In Progress task")
    create.add_argument("--title", required=True)
    create.add_argument("--parent", required=True)
    create.add_argument("--dependencies", default="")
    create.add_argument("--acceptance", required=True)
    create.add_argument("--proof", required=True)
    create.add_argument(
        "--status",
        choices=("Planned", "In Progress"),
        default="Planned",
    )
    create.add_argument("--owner", default="")

    claim = subparsers.add_parser("claim", help="Claim a Planned task")
    claim.add_argument("task_id")
    claim.add_argument("--owner", required=True)

    update = subparsers.add_parser("update", help="Update an owned In Progress task")
    update.add_argument("task_id")
    update.add_argument("--owner", required=True)
    update.add_argument("--title")
    update.add_argument("--parent")
    update.add_argument("--dependencies")
    update.add_argument("--acceptance")
    update.add_argument("--proof")

    close = subparsers.add_parser("close", help="Close a task with evidence")
    close.add_argument("task_id")
    close.add_argument("--owner", required=True)
    close.add_argument("--evidence", required=True)
    close.add_argument(
        "--user-override",
        action="store_true",
        help="Close a task owned by another thread after a direct user request",
    )
    close.add_argument("--override-reason")

    migrate = subparsers.add_parser(
        "migrate",
        help="Atomically migrate the legacy lowercase header",
    )
    migrate.add_argument("--task", required=True)
    migrate.add_argument("--owner", required=True)

    return result


def clean(value: str, label: str) -> str:
    result = value.strip()
    if not result:
        raise TaskError(f"{label} cannot be empty")
    if "\n" in result or "\r" in result:
        raise TaskError(f"{label} must fit on one line")
    return result


def thread_owner(value: str) -> str:
    result = clean(value, "Owner")
    if not THREAD_OWNER_PATTERN.fullmatch(result):
        raise TaskError("Owner must be the 8-digit value supplied by the lifecycle hook")
    return result


def lock_is_stale(lock_path: Path) -> bool:
    try:
        age = time.time() - lock_path.stat().st_mtime
    except FileNotFoundError:
        return False
    if age < STALE_LOCK_SECONDS:
        return False

    owner_path = lock_path / "owner.json"
    try:
        owner = json.loads(owner_path.read_text(encoding="utf-8"))
        pid = int(owner["pid"])
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return True

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    except (PermissionError, OSError):
        return False
    return False


@contextmanager
def ledger_lock(planning_dir: Path) -> Iterator[None]:
    planning_dir.mkdir(parents=True, exist_ok=True)
    lock_path = planning_dir / ".tasks.lock"
    deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS

    while True:
        try:
            lock_path.mkdir()
            try:
                (lock_path / "owner.json").write_text(
                    json.dumps({"pid": os.getpid(), "created": time.time()}),
                    encoding="utf-8",
                )
            except OSError:
                shutil.rmtree(lock_path, ignore_errors=True)
                raise
            break
        except FileExistsError:
            if lock_is_stale(lock_path):
                try:
                    shutil.rmtree(lock_path)
                except FileNotFoundError:
                    pass
                continue
            if time.monotonic() >= deadline:
                raise TaskError(
                    "task ledger is busy; retry after the other task operation finishes"
                )
            time.sleep(0.05)

    try:
        yield
    finally:
        shutil.rmtree(lock_path, ignore_errors=True)


def read_ledger(path: Path, *, allow_legacy: bool = False) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise TaskError(
            "planning/tasks.csv does not exist; initialize the repository first"
        )
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            accepted = [list(TASK_COLUMNS)]
            if allow_legacy:
                accepted.append(list(LEGACY_COLUMNS))
            if columns not in accepted:
                expected = ", ".join(TASK_COLUMNS)
                raise TaskError(f"unexpected task header; expected: {expected}")
            rows = [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
                if any((value or "").strip() for value in row.values())
            ]
    except (OSError, csv.Error) as exc:
        raise TaskError(f"cannot read planning/tasks.csv: {exc}") from exc
    return columns, rows


def write_ledger(path: Path, rows: list[dict[str, str]]) -> None:
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    temporary: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".tasks.",
            suffix=".csv",
            dir=path.parent,
            text=True,
        )
        temporary = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=TASK_COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        temporary = None
        try:
            directory = os.open(path.parent, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def find_task(rows: list[dict[str, str]], task_id: str) -> dict[str, str]:
    wanted = clean(task_id, "Task ID")
    matches = [row for row in rows if row.get("Task ID") == wanted]
    if not matches:
        raise TaskError(f"task does not exist: {wanted}")
    if len(matches) > 1:
        raise TaskError(f"duplicate task id: {wanted}")
    return matches[0]


def next_task_id(rows: list[dict[str, str]]) -> str:
    highest = -1
    for row in rows:
        match = TASK_ID_PATTERN.fullmatch(row.get("Task ID", ""))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"TASK-{highest + 1:03d}"


def require_owner(task: dict[str, str], owner: str) -> str:
    supplied = clean(owner, "Owner")
    actual = task.get("Owner", "")
    if actual != supplied:
        raise TaskError(
            f"{task.get('Task ID', 'task')} belongs to owner {actual or '<none>'}, "
            f"not {supplied}"
        )
    return supplied


def create_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    owner = args.owner.strip()
    if args.status == "In Progress":
        owner = thread_owner(owner)
    elif owner:
        raise TaskError("a Planned task cannot have an owner; claim it when work starts")

    task_id = next_task_id(rows)
    rows.insert(
        0,
        {
            "Task ID": task_id,
            "Title": clean(args.title, "Title"),
            "Status": args.status,
            "Parent": clean(args.parent, "Parent"),
            "Dependencies": args.dependencies.strip(),
            "Owner": owner,
            "Acceptance Criteria": clean(args.acceptance, "Acceptance Criteria"),
            "Proof": clean(args.proof, "Proof"),
            "Evidence": "",
        },
    )
    return f"created {task_id} ({args.status})"


def claim_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    if task.get("Status") != "Planned":
        raise TaskError(f"{args.task_id} must be Planned before it can be claimed")
    if task.get("Owner"):
        raise TaskError(f"{args.task_id} is already owned")
    task["Owner"] = thread_owner(args.owner)
    task["Status"] = "In Progress"
    return f"claimed {args.task_id} for owner {task['Owner']}"


def update_task(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    task = find_task(rows, args.task_id)
    if task.get("Status") != "In Progress":
        raise TaskError(f"{args.task_id} must be In Progress before it can be updated")
    require_owner(task, args.owner)

    changes = {
        "Title": args.title,
        "Parent": args.parent,
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
        raise TaskError(f"{args.task_id} must be In Progress before it can be closed")

    supplied_owner = clean(args.owner, "Owner")
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


def migrate_ledger(
    args: argparse.Namespace,
    columns: list[str],
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], str, bool]:
    if columns == list(TASK_COLUMNS):
        return rows, "task ledger already uses the current header", False
    legacy_task = next(
        (row for row in rows if row.get("task_id") == args.task),
        None,
    )
    if legacy_task is None:
        raise TaskError(f"task does not exist: {args.task}")
    if legacy_task.get("status") != "In Progress":
        raise TaskError(f"{args.task} must be In Progress before migration")
    if legacy_task.get("owner") != clean(args.owner, "Owner"):
        raise TaskError(f"{args.task} is not owned by {args.owner}")
    migrated = [
        {new: row.get(old, "") for old, new in LEGACY_TO_CURRENT.items()}
        for row in rows
    ]
    return migrated, "migrated task ledger to the human-readable header", True


def main() -> int:
    args = parser().parse_args()
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(
            f"Task operation failed: repository directory does not exist: {root}",
            file=sys.stderr,
        )
        return 1

    path = root / "planning/tasks.csv"
    try:
        with ledger_lock(path.parent):
            columns, rows = read_ledger(
                path,
                allow_legacy=args.command == "migrate",
            )
            if args.command == "create":
                message = create_task(args, rows)
            elif args.command == "claim":
                message = claim_task(args, rows)
            elif args.command == "update":
                message = update_task(args, rows)
            elif args.command == "close":
                message = close_task(args, rows)
            else:
                rows, message, changed = migrate_ledger(args, columns, rows)
                if not changed:
                    print(message)
                    return 0
            write_ledger(path, rows)
    except (TaskError, OSError) as exc:
        print(f"Task operation failed: {exc}", file=sys.stderr)
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
