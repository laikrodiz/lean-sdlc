#!/usr/bin/env python3
"""Shared task-ledger primitives for Lean-SDLC."""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
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
PARENT_PATTERN = re.compile(r"(?:FEAT|DEC)-[A-Za-z0-9][A-Za-z0-9._-]*$")
TASK_STATUSES = {"Planned", "In Progress", "Done"}
SPECIAL_PARENTS = {"REPO", "BOOTSTRAP"}
LOCK_TIMEOUT_SECONDS = 10
STALE_LOCK_SECONDS = 60


class TaskError(Exception):
    """A user-correctable task-ledger error."""


def task_path(root: Path) -> Path:
    return root / "tasks.csv"


def legacy_task_path(root: Path) -> Path:
    return root / "planning" / "tasks.csv"


def clean(value: str, label: str) -> str:
    result = value.strip()
    if not result:
        raise TaskError(f"{label} cannot be empty")
    if "\n" in result or "\r" in result:
        raise TaskError(f"{label} must fit on one line")
    return result


def thread_owner(value: str, *, allow_bootstrap: bool = False) -> str:
    result = clean(value, "Owner")
    if allow_bootstrap and result == "bootstrap":
        return result
    if not THREAD_OWNER_PATTERN.fullmatch(result):
        raise TaskError("Owner must be the 8-digit value supplied by the lifecycle hook")
    return result


def _lock_is_stale(lock_path: Path) -> bool:
    try:
        age = time.time() - lock_path.stat().st_mtime
    except FileNotFoundError:
        return False
    if age < STALE_LOCK_SECONDS:
        return False

    try:
        owner = json.loads((lock_path / "owner.json").read_text(encoding="utf-8"))
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
def directory_lock(lock_path: Path) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
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
            if _lock_is_stale(lock_path):
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


@contextmanager
def ledger_lock(root: Path) -> Iterator[None]:
    with directory_lock(root / ".tasks.lock"):
        yield


def read_ledger(
    path: Path,
    *,
    allow_legacy: bool = False,
) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise TaskError(f"{path.name} does not exist; initialize the repository first")

    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            accepted = [list(TASK_COLUMNS)]
            if allow_legacy:
                accepted.append(list(LEGACY_COLUMNS))
            if columns not in accepted:
                raise TaskError(
                    "unexpected task header; expected: " + ", ".join(TASK_COLUMNS)
                )

            rows: list[dict[str, str]] = []
            for number, row in enumerate(reader, start=2):
                if None in row:
                    raise TaskError(f"{path.name}:{number}: too many CSV fields")
                normalized = {
                    key: (value or "").strip()
                    for key, value in row.items()
                    if key is not None
                }
                if any(normalized.values()):
                    rows.append(normalized)
    except (OSError, csv.Error) as exc:
        raise TaskError(f"cannot read {path}: {exc}") from exc
    return columns, rows


def current_rows(
    columns: list[str],
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    if columns == list(TASK_COLUMNS):
        return rows
    return [
        {new: row.get(old, "") for old, new in LEGACY_TO_CURRENT.items()}
        for row in rows
    ]


def write_ledger(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def dependency_ids(value: str) -> list[str]:
    if not value.strip():
        return []
    return [part for part in re.split(r"[,;\s]+", value.strip()) if part]


def integrity_errors(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    row_by_id: dict[str, dict[str, str]] = {}

    for row in rows:
        task_id = row.get("Task ID", "")
        if not TASK_ID_PATTERN.fullmatch(task_id):
            errors.append(f"invalid task id {task_id or '<empty>'}")
        elif task_id in seen:
            errors.append(f"duplicate task id {task_id}")
        else:
            seen.add(task_id)
            row_by_id[task_id] = row

    graph: dict[str, list[str]] = {}
    for task_id, row in row_by_id.items():
        dependencies = dependency_ids(row.get("Dependencies", ""))
        graph[task_id] = []
        local_seen: set[str] = set()
        for dependency in dependencies:
            if not TASK_ID_PATTERN.fullmatch(dependency):
                errors.append(f"{task_id} has invalid dependency {dependency}")
            elif dependency == task_id:
                errors.append(f"{task_id} depends on itself")
            elif dependency in local_seen:
                errors.append(f"{task_id} repeats dependency {dependency}")
            elif dependency not in row_by_id:
                errors.append(f"{task_id} depends on missing task {dependency}")
            else:
                graph[task_id].append(dependency)
            local_seen.add(dependency)

        if row.get("Status") == "Done":
            for dependency in graph[task_id]:
                if row_by_id[dependency].get("Status") != "Done":
                    errors.append(
                        f"{task_id} is Done before dependency {dependency}"
                    )

    state: dict[str, int] = {}
    stack: list[str] = []
    cycle_reported = False

    def visit(task_id: str) -> None:
        nonlocal cycle_reported
        state[task_id] = 1
        stack.append(task_id)
        for dependency in graph.get(task_id, []):
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1 and not cycle_reported:
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                errors.append("dependency cycle: " + " -> ".join(cycle))
                cycle_reported = True
        stack.pop()
        state[task_id] = 2

    for task_id in graph:
        if state.get(task_id, 0) == 0:
            visit(task_id)

    return errors


def require_integrity(rows: list[dict[str, str]]) -> None:
    errors = integrity_errors(rows)
    if errors:
        raise TaskError("; ".join(errors))
