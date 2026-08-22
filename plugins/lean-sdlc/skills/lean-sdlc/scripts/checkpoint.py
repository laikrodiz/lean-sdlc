#!/usr/bin/env python3
"""Compute a stable task-scoped checkpoint identity without changing the repository."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True


class CheckpointError(ValueError):
    """A checkpoint input cannot identify a task-owned path."""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="repository root")
    parser.add_argument(
        "paths",
        nargs="+",
        metavar="PATH",
        help="one or more task-owned files or directories relative to the repository",
    )
    return parser


def _repository_root(value: str) -> Path:
    supplied = Path(value)
    if supplied.is_symlink():
        raise CheckpointError("repository root must not be a symbolic link")
    try:
        root = supplied.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise CheckpointError(f"repository root is not available: {value}") from exc
    if not root.is_dir():
        raise CheckpointError("repository root must be a directory")
    return root


def _candidate(root: Path, value: str) -> tuple[Path, Path]:
    supplied = Path(value)
    joined = supplied if supplied.is_absolute() else root / supplied
    normalized = Path(os.path.normpath(str(joined)))
    try:
        relative = normalized.relative_to(root)
    except ValueError as exc:
        raise CheckpointError(f"path escapes repository: {value}") from exc
    if relative == Path("."):
        raise CheckpointError("repository root is not a task-owned path")
    if any(part == ".git" for part in relative.parts):
        raise CheckpointError(".git is not a task-owned path")
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise CheckpointError(f"symbolic links are not allowed: {value}")
    if not normalized.exists():
        raise CheckpointError(f"path does not exist: {value}")
    return normalized, relative


def _collect(
    path: Path,
    relative: Path,
    files: dict[str, Path],
) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise CheckpointError(f"cannot inspect path: {relative.as_posix()}") from exc
    if stat.S_ISLNK(mode):
        raise CheckpointError(
            f"symbolic links are not allowed: {relative.as_posix()}"
        )
    if stat.S_ISREG(mode):
        files[relative.as_posix()] = path
        return
    if not stat.S_ISDIR(mode):
        raise CheckpointError(
            f"path is not a regular file or directory: {relative.as_posix()}"
        )
    try:
        children = sorted(path.iterdir(), key=lambda child: child.name)
    except OSError as exc:
        raise CheckpointError(f"cannot read directory: {relative.as_posix()}") from exc
    for child in children:
        child_relative = relative / child.name
        if child.name == ".git":
            raise CheckpointError(".git is not a task-owned path")
        _collect(child, child_relative, files)


def _digest(files: dict[str, Path]) -> str:
    digest = hashlib.sha256()
    for relative_text in sorted(files):
        encoded = relative_text.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        try:
            with files[relative_text].open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        except OSError as exc:
            raise CheckpointError(f"cannot read file: {relative_text}") from exc
    return digest.hexdigest()


def checkpoint(repository: str, values: list[str]) -> str:
    root = _repository_root(repository)
    files: dict[str, Path] = {}
    for value in values:
        path, relative = _candidate(root, value)
        _collect(path, relative, files)
    return _digest(files)


def main(arguments: list[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    try:
        print(checkpoint(args.repo, args.paths))
    except CheckpointError as exc:
        print(f"Checkpoint failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
