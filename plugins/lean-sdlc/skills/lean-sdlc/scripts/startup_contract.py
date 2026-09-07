#!/usr/bin/env python3
"""Read and update the managed Lean-SDLC startup block."""

from __future__ import annotations

import hashlib
from pathlib import Path


START_MARKER = "<!-- lean-sdlc:startup v1 -->"
END_MARKER = "<!-- /lean-sdlc:startup -->"
LEGACY_TEMPLATE_LENGTH = 6286
LEGACY_TEMPLATE_SHA256 = "38740988f9f1bfebcfa97f7b225828050c5c905a28cd68d75e223968f92e30a3"


class StartupContractError(Exception):
    """A managed startup block cannot be read or updated safely."""


def legacy_contract_error(text: str) -> str | None:
    """Accept the current contract prefix; require reconciliation of unknown cores."""
    if not text.startswith(template_path().read_text(encoding="utf-8")):
        return "legacy workflow routing or an unknown AGENTS.md contract requires explicit reconciliation"
    if any(rule in text for rule in (
        "Before each child handoff, use the design brief in `<skill-root>/references/subagents.md`.",
        "Read `references/subagents.md` before delegation.",
        "Assisted mode and Standard children are defaults.",
    )):
        return "legacy workflow routing requires an explicit AGENTS.md contract upgrade"
    return None


def upgrade_contract_text(text: str) -> str:
    """Replace only a recognized released template; preserve appended project rules."""
    replacement = template_path().read_text(encoding="utf-8")
    if text.startswith(replacement):
        return text
    prefix = text[:LEGACY_TEMPLATE_LENGTH]
    if hashlib.sha256(prefix.encode("utf-8")).hexdigest() != LEGACY_TEMPLATE_SHA256:
        raise StartupContractError(
            "unrecognized AGENTS.md contract; reconcile custom instructions explicitly"
        )
    return replacement + text[LEGACY_TEMPLATE_LENGTH:]


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
