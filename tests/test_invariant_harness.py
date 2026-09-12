"""Critical instruction contracts; prose checks are not live behavioral evidence."""
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
    # Keep authority, ownership, prerequisites, and user-required output contracts.
    # Generic advice and incidental wording belong in focused review, not this list.
    FrozenInvariant("read-only authority", "SKILL.md", ("Read-only requests create no tasks",)),
    FrozenInvariant("conversation authority", "references/conversation.md", ("A detailed idea is not implementation authority",)),
    FrozenInvariant("visible plan", "references/plan.md", ("always show all five fields", "every explicit user requirement", "plan-only request stops")),
    FrozenInvariant("visible task state", "references/plan.md", ("| Task ID | Short description | Grade | Status |", "ledger remains authoritative")),
    FrozenInvariant("task display lifecycle", "references/plan.md", ("Starting <real task ID>: <exact title>", "Optimal process:", "For one task", "for multiple tasks", "actual final states after ledger reconciliation")),
    FrozenInvariant("confirmed direct closure", "references/plan.md", ("close the task directly through the helper, confirm success", "never bypass dependencies")),
    FrozenInvariant("owned write prerequisites", "protocols/lead.md", ("Before writing, confirm", "successful before-write gate", "A pending or failed transaction is not proof")),
    FrozenInvariant("implementation ownership", "protocols/lead.md", ("Lead implements all code and domain changes", "Run immediate builds, focused tests")),
    FrozenInvariant("original acceptance", "protocols/lead.md", ("Compare the original request", "Task text alone cannot replace")),
    FrozenInvariant("role authority", "protocols/common.md", ("Only Lead assigns", "Support agents cannot spawn")),
    FrozenInvariant("resource isolation", "protocols/common.md", ("One writer owns each mutable", "A ledger lock protects only")),
    FrozenInvariant("cancellation", "protocols/common.md", ("underlying command or process", "Late results cannot restore canceled authority")),
    FrozenInvariant("model profile", "protocols/common.md", ("user-selected Lead model", "model=gpt-5.6-luna", "reasoning_effort=max", "gpt-5.6-terra")),
    FrozenInvariant("ledger ownership", "references/ledger.md", ("Lead performs all task writes directly", "using the Lead owner", "helper validates records, not whether the original request was fulfilled")),
    FrozenInvariant("proof ownership", "protocols/verifier.md", ("Verifier owns assigned independent acceptance", "You do not change tracked source")),
    FrozenInvariant("stable proof inputs", "protocols/verifier.md", ("before and after proof", "even if a later fingerprint matches")),
    FrozenInvariant("honest evidence", "protocols/verifier.md", ("not a live behavioral test", "Never report an unexecuted command as passed")),
    FrozenInvariant("Backlog authority", "references/ledger.md", ("only under direct user authority", "Backlog is not execution authority")),
    FrozenInvariant("document preservation", "references/documentation.md", ("Never reuse IDs", "Preserve v1.24.3 document IDs")),
    FrozenInvariant("recorded operation authority", "references/operations.md", ("An operation record or script never grants permission", "already-authorized recovery")),
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
