#!/usr/bin/env python3
"""Read and update the managed Lean-SDLC startup block."""

from __future__ import annotations

import hashlib
from pathlib import Path


START_MARKER = "<!-- lean-sdlc:startup v1 -->"
END_MARKER = "<!-- /lean-sdlc:startup -->"
RELEASED_CONTRACT_SHA256 = "03211c7f07b3829744aceafe8893ff6c8ae83414c85e036deac5e57b74937805"
RELEASED_SECTIONS = {
    "## Repository gate", "## Task gate", "## Assisted lifecycle and proof",
    "## Plan view and lifecycle",
}


class StartupContractError(Exception):
    """A managed startup block cannot be read or updated safely."""


def _marker_lines(text: str, marker: str) -> list[int]:
    return [
        number
        for number, line in enumerate(text.splitlines(keepends=True))
        if line.rstrip("\r\n") == marker
    ]


def extract_managed_block(text: str) -> str | None:
    """Return one complete managed block, or None when its boundary is invalid."""

    lines = text.splitlines(keepends=True)
    starts = _marker_lines(text, START_MARKER)
    ends = _marker_lines(text, END_MARKER)
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        return None
    return "".join(lines[starts[0] : ends[0] + 1])


def startup_block_error(text: str, expected: str) -> str | None:
    """Return a concise contract error, or None when the block matches."""

    starts = _marker_lines(text, START_MARKER)
    ends = _marker_lines(text, END_MARKER)
    if not starts and not ends:
        return "missing managed startup block"
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        return "invalid managed startup block"
    actual = extract_managed_block(text)
    if actual != expected:
        return "stale managed startup block"
    return None


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "AGENTS.md"


def read_template_block() -> str:
    path = template_path()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StartupContractError(f"cannot read startup template: {exc}") from exc
    block = extract_managed_block(text)
    if block is None:
        raise StartupContractError(
            f"startup template has an invalid managed startup block: {path}"
        )
    return block


def repair_text(text: str, replacement: str) -> str:
    """Replace one block or append a missing block while preserving other text."""

    if extract_managed_block(replacement) != replacement:
        raise StartupContractError("replacement has an invalid managed startup block")

    lines = text.splitlines(keepends=True)
    starts = _marker_lines(text, START_MARKER)
    ends = _marker_lines(text, END_MARKER)
    if not starts and not ends:
        separator = "" if not text or text.endswith(("\n", "\r")) else "\n"
        return text + separator + replacement
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise StartupContractError("cannot repair an invalid managed startup block")

    start_offset = sum(len(line) for line in lines[: starts[0]])
    end_offset = sum(len(line) for line in lines[: ends[0] + 1])
    return text[:start_offset] + replacement + text[end_offset:]


def upgrade_text(text: str, replacement: str) -> str:
    """Replace the exact released contract, never guess about modified rules."""
    expected = extract_managed_block(replacement)
    if expected is None:
        raise StartupContractError("replacement has an invalid managed startup block")
    if len(_marker_lines(text, "# Lean-SDLC Repository Rules")) > 1:
        raise StartupContractError("multiple Lean-SDLC contracts; review before upgrade")
    if (_marker_lines(text, START_MARKER) or _marker_lines(text, END_MARKER)) and extract_managed_block(text) is None:
        raise StartupContractError("cannot upgrade an invalid managed startup block")
    lines = text.splitlines(keepends=True)
    offset = 0
    for index, line in enumerate(lines):
        if line.rstrip("\r\n") == "# Lean-SDLC Repository Rules":
            digest = hashlib.sha256()
            end = offset
            for candidate in lines[index:]:
                digest.update(candidate.replace("\r\n", "\n").encode("utf-8"))
                end += len(candidate)
                if digest.hexdigest() == RELEASED_CONTRACT_SHA256:
                    return text[:offset] + replacement + text[end:]
        offset += len(line)

    if any(line.rstrip("\r\n") in RELEASED_SECTIONS for line in lines):
        raise StartupContractError(
            "modified or unsupported Lean-SDLC contract; review custom rules before upgrade"
        )
    if extract_managed_block(text) == expected:
        return text
    if "Lean-SDLC" in text or "$lean-sdlc" in text or START_MARKER in text or END_MARKER in text:
        raise StartupContractError(
            "modified or unsupported Lean-SDLC contract; review custom rules before upgrade"
        )
    separator = "" if not text or text.endswith(("\n", "\r")) else "\n"
    return text + separator + replacement
