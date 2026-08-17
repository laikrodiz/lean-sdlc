#!/usr/bin/env python3
"""Validate the small Lean-SDLC repository contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from task_ledger import (
    CONTEXT_PATTERN,
    SPECIAL_CONTEXTS,
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
DOCUMENT_FAMILIES = (
    ("features", "FEAT"),
    ("decisions", "DEC"),
    ("architecture", "ARCH"),
    ("state-machines", "STATE"),
    ("interfaces", "IFACE"),
    ("data", "DATA"),
    ("operations", "OPS"),
)
INDEX_HEADER = "| ID | Title | Status | Owns | Related |"
ARCHIVE_INDEX_HEADER = (
    "| Capability | Snapshot | Archived | Reason | Replacement | Link |"
)
ARCHIVE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


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


def context_document_exists(root: Path, context: str) -> bool:
    folder = "features" if context.startswith("FEAT-") else "decisions"
    directory = root / "docs" / folder
    if not directory.is_dir():
        return False
    return any(
        path.is_file()
        and (path.stem == context or path.name.startswith(f"{context}-"))
        for path in directory.iterdir()
    )


def markdown_targets(path: Path, errors: list[str]) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
        return []

    targets: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        else:
            target = target.split(maxsplit=1)[0]
        targets.append(target.split("#", 1)[0])
    return targets


def relative_target(base: Path, target: str) -> Path | None:
    if not target or target.startswith(("/", "#")) or "://" in target:
        return None
    if ".." in Path(target).parts:
        return None
    resolved = (base / target).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        return None
    return resolved


def document_collection_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for folder, prefix in DOCUMENT_FAMILIES:
        directory = root / "docs" / folder
        if not directory.exists():
            continue
        if not directory.is_dir():
            errors.append(f"docs/{folder}: expected a directory")
            continue

        pattern = re.compile(
            rf"{re.escape(prefix)}-(\d{{3}})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z"
        )
        documents: list[Path] = []
        ids: dict[str, list[str]] = {}
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.suffix.casefold() != ".md":
                continue
            if not path.name.startswith(f"{prefix}-"):
                continue
            match = pattern.fullmatch(path.name)
            if match is None:
                errors.append(
                    f"docs/{folder}: malformed document name {path.name}; "
                    f"expected {prefix}-NNN-lowercase-slug.md"
                )
                continue
            document_id = f"{prefix}-{match.group(1)}"
            ids.setdefault(document_id, []).append(path.name)
            documents.append(path)

        for document_id, names in ids.items():
            if len(names) > 1:
                errors.append(
                    f"docs/{folder}: duplicate id {document_id}: " + ", ".join(names)
                )

        if not documents:
            continue
        index = directory / "INDEX.md"
        if not index.is_file():
            errors.append(f"docs/{folder}: missing INDEX.md")
            continue
        try:
            lines = index.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            errors.append(f"docs/{folder}/INDEX.md: cannot read file: {exc}")
            continue
        if INDEX_HEADER not in {line.strip() for line in lines}:
            errors.append(
                f"docs/{folder}/INDEX.md: expected header {INDEX_HEADER}"
            )

        linked_names: list[str] = []
        for target in markdown_targets(index, errors):
            if Path(target).name.startswith(f"{prefix}-"):
                resolved = relative_target(directory, target)
                if resolved is None or resolved.parent != directory.resolve():
                    errors.append(
                        f"docs/{folder}/INDEX.md: invalid family link {target}"
                    )
                    continue
                if not resolved.is_file():
                    errors.append(
                        f"docs/{folder}/INDEX.md: linked file does not exist: {target}"
                    )
                    continue
                linked_names.append(resolved.name)

        for document in documents:
            count = linked_names.count(document.name)
            if count == 0:
                errors.append(
                    f"docs/{folder}/INDEX.md: missing link to {document.name}"
                )
            elif count > 1:
                errors.append(
                    f"docs/{folder}/INDEX.md: duplicate link to {document.name}"
                )
    return errors


def source_archive_errors(root: Path) -> list[str]:
    archive = root / "archive"
    if not archive.exists():
        return []
    if not archive.is_dir():
        return ["archive: expected a directory"]

    errors: list[str] = []
    index = archive / "INDEX.md"
    if not index.is_file():
        errors.append("archive: missing INDEX.md")

    manifests: list[Path] = []
    for capability in sorted(archive.iterdir()):
        if capability.name == "INDEX.md":
            continue
        if not capability.is_dir():
            errors.append(f"archive: unexpected file {capability.name}")
            continue
        if ARCHIVE_NAME.fullmatch(capability.name) is None:
            errors.append(f"archive: malformed capability name {capability.name}")
        for snapshot in sorted(capability.iterdir()):
            if not snapshot.is_dir():
                errors.append(
                    f"archive/{capability.name}: unexpected file {snapshot.name}"
                )
                continue
            if ARCHIVE_NAME.fullmatch(snapshot.name) is None:
                errors.append(
                    f"archive/{capability.name}: malformed snapshot name {snapshot.name}"
                )
            manifest = snapshot / "ARCHIVE.md"
            if not manifest.is_file():
                errors.append(
                    f"archive/{capability.name}/{snapshot.name}: missing ARCHIVE.md"
                )
                continue
            manifests.append(manifest.resolve())

    if not manifests:
        errors.append("archive: no source snapshots")
    if not index.is_file():
        return errors

    try:
        lines = index.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"archive/INDEX.md: cannot read file: {exc}")
        return errors
    if ARCHIVE_INDEX_HEADER not in {line.strip() for line in lines}:
        errors.append(
            f"archive/INDEX.md: expected header {ARCHIVE_INDEX_HEADER}"
        )

    linked_manifests: list[Path] = []
    for target in markdown_targets(index, errors):
        if Path(target).name != "ARCHIVE.md":
            continue
        resolved = relative_target(archive, target)
        if resolved is None:
            errors.append(f"archive/INDEX.md: invalid snapshot link {target}")
            continue
        try:
            relative = resolved.relative_to(archive.resolve())
        except ValueError:
            errors.append(f"archive/INDEX.md: invalid snapshot link {target}")
            continue
        if len(relative.parts) != 3:
            errors.append(f"archive/INDEX.md: invalid snapshot link {target}")
            continue
        if not resolved.is_file():
            errors.append(
                f"archive/INDEX.md: linked manifest does not exist: {target}"
            )
            continue
        linked_manifests.append(resolved)

    for manifest in manifests:
        count = linked_manifests.count(manifest)
        relative = manifest.relative_to(root.resolve())
        if count == 0:
            errors.append(f"archive/INDEX.md: missing link to {relative}")
        elif count > 1:
            errors.append(f"archive/INDEX.md: duplicate link to {relative}")
    return errors


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

    if not args.before_write:
        errors.extend(document_collection_errors(root))
        errors.extend(source_archive_errors(root))

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
                "expected Backlog, Planned, In Progress, or Done"
            )

        context = task.get("Context", "")
        if context == "Bootstrap":
            bootstrap_tasks += 1
        if not context:
            errors.append(f"tasks.csv:{number}: {task_id} has no context")
        elif context not in SPECIAL_CONTEXTS and not CONTEXT_PATTERN.fullmatch(context):
            errors.append(f"tasks.csv:{number}: {task_id} has invalid context {context}")
        elif (
            CONTEXT_PATTERN.fullmatch(context)
            and status != "In Progress"
            and not context_document_exists(root, context)
        ):
            errors.append(
                f"tasks.csv:{number}: {task_id} has no document for context {context}"
            )

        owner = task.get("Owner", "")
        if status == "Planned" and owner:
            errors.append(f"tasks.csv:{number}: {task_id} is Planned but already owned")
        if status == "In Progress":
            valid_bootstrap = context == "Bootstrap" and owner == "bootstrap"
            if not valid_bootstrap and not THREAD_OWNER_PATTERN.fullmatch(owner):
                errors.append(
                    f"tasks.csv:{number}: {task_id} has invalid active owner "
                    f"{owner or '<empty>'}"
                )
        if status == "Done" and not owner:
            errors.append(f"tasks.csv:{number}: {task_id} has empty owner")

        if status != "Backlog":
            if not task.get("Acceptance Criteria"):
                errors.append(f"tasks.csv:{number}: {task_id} has empty acceptance")
            if not task.get("Proof"):
                errors.append(f"tasks.csv:{number}: {task_id} has empty proof")
        if status == "Done" and not task.get("Evidence"):
            errors.append(f"tasks.csv:{number}: {task_id} is Done without evidence")

    if bootstrap_tasks > 1:
        errors.append("tasks.csv: more than one Bootstrap task exists")

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
