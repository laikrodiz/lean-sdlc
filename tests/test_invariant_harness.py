from __future__ import annotations

import re
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class FrozenInvariant:
    """One frozen behavior and the source terms that define its contract."""

    name: str
    sources: tuple[str, ...]
    required_terms: tuple[str, ...]
    check: str = "terms"


FROZEN_INVARIANTS = (
    FrozenInvariant(
        "six lanes",
        ("README.md", "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"),
        (
            "## lanes",
            "| lane | purpose |",
            "| shape |",
            "| decide |",
            "| plan |",
            "| diagnose |",
            "| deliver |",
            "| verify |",
        ),
        check="lanes",
    ),
    FrozenInvariant(
        "explicit implementation authority",
        (
            "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/shape.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
        ),
        (
            "explicit implementation authority",
            "discussion or proposal requests remain read-only",
            "if authority is ambiguous, remain read-only",
            "natural intent confirmation",
            "concise visible plan",
        ),
    ),
    FrozenInvariant(
        "owned task before writes",
        ("AGENTS.md", "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"),
        (
            "before any other repository mutation",
            "create immediate work or claim planned work",
            "require an owned `in progress` task",
            "run `lean_check.py --before-write",
        ),
    ),
    FrozenInvariant(
        "atomic tasks.csv transactions",
        (
            "docs/PROJECT.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ),
        (
            "atomic private task-ledger transactions",
            "task transactions remain atomic",
            "command serializes writers",
            "replaces the file atomically",
        ),
    ),
    FrozenInvariant(
        "stable owner after compaction",
        (
            "AGENTS.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
        ),
        (
            "retain the stable 8-digit task owner supplied by the plugin hook",
            "remains resumable from repository truth and its ledger row after compaction",
            "rehydrate an allowed replacement from its role",
            "relevant procedure, checkpoint, and latest unresolved result",
        ),
    ),
    FrozenInvariant(
        "owner-only close",
        (
            "AGENTS.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md",
        ),
        (
            "only the owner closes a task",
            "`close` belongs to the owner after verification",
            "owning lead alone decide task disposition",
            "direct user request",
        ),
    ),
    FrozenInvariant(
        "assisted and solo only",
        (
            "README.md",
            "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
        ),
        (
            "assisted mode",
            "solo mode",
            "assisted and solo are the only orchestration modes",
        ),
    ),
    FrozenInvariant(
        "architect owns decisions",
        (
            "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md",
        ),
        (
            "the user-selected lead acts as principal engineer and owns product intent",
            "the architect supplies the question and source boundary",
            "keep architecture, task setting, integration, and other consequential decisions with the architect",
            "the user-selected lead makes the final accept",
        ),
    ),
    FrozenInvariant(
        "engineer, maintainer, verifier, and researcher roles",
        (
            "README.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
        ),
        (
            "| engineer |",
            "| maintainer |",
            "| verifier |",
            "| researcher |",
            "the standard four-role hierarchy",
        ),
    ),
    FrozenInvariant(
        "luna max primary and terra xhigh fallback",
        (
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
            "plugins/lean-sdlc/skills/lean-sdlc/assets/lean_sdlc_luna.toml",
        ),
        (
            "gpt-5.6-luna",
            "max",
            "agent_type=lean_sdlc_luna",
            "service_tier=priority",
            "non-full-history `fork_turns`",
            "retry luna max",
            "gpt-5.6-terra",
            "terra `xhigh`",
            "directly spawn `gpt-5.6-terra` at `xhigh`",
            "without `service_tier` or `agent_type`",
        ),
    ),
    FrozenInvariant(
        "one reusable child per role",
        ("plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",),
        (
            "at most one child thread for each role during one lead codex task",
            "reuse that role thread through follow-up handoffs",
            "keep one reachable child per role",
            "reuse the existing engineer role thread",
        ),
    ),
    FrozenInvariant(
        "exact checkpoint barrier",
        ("plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",),
        (
            "## checkpoint barrier",
            "identify the checkpoint by commit or exact working-tree fingerprint",
            "require the sidecar to confirm the identity before acting",
            "invalidate the result after any relevant source change",
        ),
    ),
    FrozenInvariant(
        "learned operations",
        ("plugins/lean-sdlc/skills/lean-sdlc/references/operations.md",),
        (
            "unknown -> guided success -> recorded -> verified -> repeatable -> stale",
            "after success, the maintainer returns a short procedure draft",
            "the lead records it in optional `docs/operations.md`",
            "later maintainer runs replay the recorded procedure exactly",
        ),
    ),
    FrozenInvariant(
        "legacy ledger migration",
        (
            "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ),
        (
            "for an older ledger",
            "run [scripts/tasks.py](scripts/tasks.py) `upgrade`",
            "accepts the previous `parent` header and older planning header",
            "maps `repo` to `project` and `bootstrap` to `bootstrap`",
            "atomically writes one root csv under the existing lock",
        ),
    ),
    FrozenInvariant(
        "applicable asd-ste100 guidance",
        ("AGENTS.md", "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"),
        (
            "asd-ste100 issue 9",
            "active voice",
            "20 words or fewer",
            "25 words or fewer",
            "one term for one meaning",
            "conditions before actions",
            "american english spelling",
            "preserve code, commands, paths, identifiers, protocol fields, quotations",
            "do not claim certified or full controlled-dictionary compliance",
        ),
    ),
    FrozenInvariant(
        "modularity, edge cases, and mermaid diagrams",
        (
            "AGENTS.md",
            "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/trigger-evals.md",
        ),
        (
            "smallest cohesive units",
            "avoid project-size tiers, speculative interfaces, and pass-through modules",
            "plausible edge cases",
            "classify plausible edge cases as `handle`, `reject`, `defer`, or `impossible by invariant`",
            "prefer small mermaid diagrams",
            "never use ascii pseudographics",
        ),
    ),
    FrozenInvariant(
        "task sizing and compaction resume",
        (
            "AGENTS.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
            "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ),
        (
            "one durable task represents one independently accepted repository state",
            "one observable outcome, one coherent change boundary, one acceptance set",
            "the task must resume from repository truth and its ledger row after compaction",
            "split a task when a part can fail, ship, revert, resume, or close independently",
            "avoid fixed limits based on time, lines, or file count",
        ),
    ),
)


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _source_texts(invariant: FrozenInvariant) -> tuple[str, ...]:
    texts: list[str] = []
    for source in invariant.sources:
        path = ROOT / source
        if not path.is_file():
            raise AssertionError(f"missing contract source: {source}")
        texts.append(_normalized(path.read_text(encoding="utf-8")))
    return tuple(texts)


def _lane_names(text: str) -> tuple[str, ...]:
    expected = {"shape", "decide", "plan", "diagnose", "deliver", "verify"}
    names = []
    for line in text.casefold().splitlines():
        match = re.match(r"\|\s*([^|]+?)\s*\|", line)
        if match and match.group(1).strip() in expected:
            names.append(match.group(1).strip())
    return tuple(names)


class FrozenInvariantHarnessTests(unittest.TestCase):
    def test_every_frozen_invariant_maps_to_a_current_contract(self) -> None:
        names = [invariant.name for invariant in FROZEN_INVARIANTS]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(FROZEN_INVARIANTS), 17)

        for invariant in FROZEN_INVARIANTS:
            with self.subTest(invariant=invariant.name):
                self.assertIn(invariant.check, {"terms", "lanes"})
                sources = _source_texts(invariant)
                combined = "\n".join(sources)
                self.assertTrue(invariant.required_terms)
                for term in invariant.required_terms:
                    self.assertIn(_normalized(term), combined, term)

                if invariant.check == "lanes":
                    readme = (ROOT / "README.md").read_text(encoding="utf-8")
                    self.assertEqual(
                        _lane_names(readme),
                        ("shape", "decide", "plan", "diagnose", "deliver", "verify"),
                    )

    def test_policy_loading_is_conditional_on_delegation(self) -> None:
        dispatcher = _normalized(
            (ROOT / "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("solo planning does not load child policy", dispatcher)
        self.assertIn("assisted delegation loads it before child use", dispatcher)
        self.assertIn(
            "references/repository-contracts.md) only for initialization, legacy migration, or document ownership",
            dispatcher,
        )


if __name__ == "__main__":
    unittest.main()
