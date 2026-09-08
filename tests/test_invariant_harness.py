"""Instruction ownership checks; these are not live behavioral evidence."""
from __future__ import annotations

import re
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/lean-sdlc/skills/lean-sdlc"


@dataclass(frozen=True)
class FrozenInvariant:
    name: str
    source: str
    required_terms: tuple[str, ...]


FROZEN_INVARIANTS = (
    FrozenInvariant("request routing", "SKILL.md", ("Interpret the request", "Read-only requests create no tasks", "Read only what applies")),
    FrozenInvariant("conversation authority", "references/conversation.md", ("A detailed idea is not implementation authority", "Make a plan", "then stop", "Do not print that entire checklist")),
    FrozenInvariant("five-field plan", "references/plan.md", ("Outcome:", "Work:", "Acceptance:", "Checks:", "Limits:")),
    FrozenInvariant("atomic task boundaries", "references/plan.md", ("independently accepted outcome", "proof cluster", "close decision", "Local implementation steps remain transient")),
    FrozenInvariant("transient grades", "references/plan.md", ("Simple, Normal, or Complex", "not a CSV column or new state file")),
    FrozenInvariant("visible task state", "references/plan.md", ("| Task ID | Short description | Grade | Status |", "TASK-NNN — Title", "ledger remains authoritative", "native view is optional")),
    FrozenInvariant("deferred Simple review", "references/plan.md", ("existing `Quick Fix` context", "Verifier runs the immediate essential check", "user can test", "before release", "--review-through")),
    FrozenInvariant("owned write prerequisites", "protocols/lead.md", ("Before writing, confirm", "successful before-write gate", "A dispatched request is not proof")),
    FrozenInvariant("Lead implementation and diagnosis", "protocols/lead.md", ("Lead implements all code and domain changes", "Trace callers", "stop the patch loop", "Verifier runs it")),
    FrozenInvariant("original acceptance", "protocols/lead.md", ("Compare the original request", "Task text alone cannot replace", "Never force stopped")),
    FrozenInvariant("asynchronous failure response", "protocols/lead.md", ("finish only the current coherent edit", "Stop affected work immediately", "invalidate affected evidence")),
    FrozenInvariant("assignment envelope", "protocols/common.md", ("Action:", "Target:", "Result:", "Limits:")),
    FrozenInvariant("role authority", "protocols/common.md", ("Only Lead assigns", "Support agents cannot spawn", "one final return", "Lead does not repeat")),
    FrozenInvariant("resource isolation", "protocols/common.md", ("One writer owns each mutable", "A ledger lock protects only", "generated outputs, caches, fixtures, services, ports, and devices")),
    FrozenInvariant("cancellation and reuse", "protocols/common.md", ("timeout or silence is not failure", "underlying command or process", "Late results cannot restore canceled authority")),
    FrozenInvariant("model profile", "protocols/common.md", ("user-selected Lead model", "model=gpt-5.6-luna", "reasoning_effort=max", "gpt-5.6-terra", "Never silently reduce")),
    FrozenInvariant("complete bounded evidence", "protocols/scout.md", ("complete reading map", "Downstream consumers", "configuration", "missing coverage", "authoritative source links")),
    FrozenInvariant("Maintainer ledger priority", "protocols/maintainer.md", ("only routine ledger writer", "Lead-assigned owner", "Prioritize ledger transactions", "Report a transaction failure immediately")),
    FrozenInvariant("documentation review continuity", "protocols/maintainer.md", ("Record full consistency-review scope", "After compaction", "A new Maintainer always performs a full consistency review")),
    FrozenInvariant("independent proof", "protocols/verifier.md", ("Verifier runs all tests", "original requirements", "targeted checks", "acceptance checks", "regression checks")),
    FrozenInvariant("stable proof inputs", "protocols/verifier.md", ("services, databases, devices", "before and after proof", "even if a later fingerprint matches", "does not identify external state")),
    FrozenInvariant("honest evidence", "protocols/verifier.md", ("not a live behavioral test", "Never report an unexecuted command as passed", "remaining risks or unavailable checks")),
    FrozenInvariant("ledger integrity", "references/ledger.md", ("only durable task plan", "locks, rereads, validates, and atomically replaces", "cycle-free", "not a security boundary")),
    FrozenInvariant("Backlog authority", "references/ledger.md", ("only under direct user authority", "Backlog rows remain sparse", "Backlog is not execution authority")),
    FrozenInvariant("compatible upgrade", "references/ledger.md", ("before Lead requests startup context", "v1.24.3", "earlier ledger conversions", "Conflicting root and planning ledgers stop", "--upgrade-contract", "custom rules")),
    FrozenInvariant("required and optional docs", "references/documentation.md", ("only mandatory shared project document", "Assessment for every change", "Optional families and triggers", "specific no-change reason")),
    FrozenInvariant("document preservation", "references/documentation.md", ("Never reuse IDs", "INDEX.md", "One document holds one cohesive subject", "Preserve v1.24.3 document IDs")),
    FrozenInvariant("archives and diagrams", "references/documentation.md", ("only on explicit user request", "Snapshots remain inert", "small Mermaid", "Do not use ASCII")),
    FrozenInvariant("recorded operation authority", "references/operations.md", ("An operation record or script never grants permission", "standing authority", "stale procedure", "already-authorized recovery")),
    FrozenInvariant("routine discovery removed", "references/operations.md", ("Automatic routine discovery", "not part of this workflow", "only when the user explicitly requests")),
    FrozenInvariant("operation safety", "references/operations.md", ("target validation", "stable exit status", "noninteractive", "atomic output", "Redact tokens")),
)


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


class FrozenInvariantHarnessTests(unittest.TestCase):
    def test_every_invariant_has_one_existing_owner(self) -> None:
        names = [item.name for item in FROZEN_INVARIANTS]
        self.assertEqual(len(names), len(set(names)))
        for item in FROZEN_INVARIANTS:
            with self.subTest(invariant=item.name):
                source = normalized((SKILL / item.source).read_text(encoding="utf-8"))
                for term in item.required_terms:
                    self.assertIn(normalized(term), source)

    def test_entry_routes_all_instructions_without_obsolete_paths(self) -> None:
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        paths = [SKILL / "SKILL.md", *sorted((SKILL / "protocols").glob("*.md")), *sorted((SKILL / "references").glob("*.md"))]
        self.assertEqual(len(paths), 11)
        for path in paths[1:]:
            self.assertIn(path.relative_to(SKILL).as_posix(), entry)
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for retired in ("subagents.md", "shape.md", "decide.md", "diagnose.md", "deliver.md", "verify.md", "repository-contracts.md", "--mode"):
            self.assertNotIn(retired, combined)
        # A generous regression ceiling, not a target for padding instruction files.
        self.assertLessEqual(len(combined.split()), 6000)
        self.assertLessEqual(len(entry.split()), 350)

    def test_plan_and_handoff_fields_have_visible_order(self) -> None:
        for name, terms in (
            ("references/plan.md", ("- Outcome:", "- Work:", "- Acceptance:", "- Checks:", "- Limits:")),
            ("protocols/common.md", ("- Action:", "- Target:", "- Result:", "- Limits:")),
        ):
            text = (SKILL / name).read_text(encoding="utf-8")
            positions = [text.index(term) for term in terms]
            self.assertEqual(positions, sorted(positions))

    def test_technical_english_and_no_implicit_profile_changes(self) -> None:
        common = (SKILL / "protocols/common.md").read_text(encoding="utf-8")
        for term in ("American English", "20 words", "25 words", "ASD-STE100", "user opt-in", "non-full-history", "role-prefixed Greek"):
            self.assertIn(term, common)
        self.assertNotRegex(common, r"reasoning_effort=(?:low|minimal)")


if __name__ == "__main__":
    unittest.main()
