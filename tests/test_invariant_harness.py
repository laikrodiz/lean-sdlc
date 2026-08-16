from __future__ import annotations

import re
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class FrozenInvariant:
    """One frozen behavior owned by one contract source."""

    name: str
    source: str
    required_terms: tuple[str, ...]
    ordered_terms: tuple[str, ...] = ()


SUBAGENTS = "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md"


FROZEN_INVARIANTS = (
    FrozenInvariant(
        "six lanes",
        "README.md",
        ("## Lanes", "| Lane | Purpose |", "| Shape |", "| Decide |", "| Plan |", "| Diagnose |", "| Deliver |", "| Verify |"),
    ),
    FrozenInvariant(
        "explicit implementation authority",
        "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
        ("explicit implementation authority", "discussion and proposal requests remain read-only", "if authority is ambiguous, remain read-only", "natural intent confirmation", "concise visible plan"),
    ),
    FrozenInvariant(
        "natural intent gate",
        "plugins/lean-sdlc/skills/lean-sdlc/references/shape.md",
        ("shape owns the complete intent gate", "why -> what -> how -> proof", "shape settles why and what", "decide and plan add how and proof", "present problem or opportunity and affected user or business value", "smallest observable outcome plus constraints and non-goals", "technical approach and task shape after why and what are stable", "proof: acceptance and verification", "material assumption affects behavior, scope, or architecture", "stop for user confirmation", "intent is clear and implementation authority is explicit", "brainstorming and rephrasing remain read-only"),
    ),
    FrozenInvariant(
        "owned task before writes",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("before any other repository mutation", "run `tasks.py start` or claim planned work", "require an owned `in progress` task", "run `lean_check.py --before-write"),
    ),
    FrozenInvariant(
        "atomic tasks.csv transactions",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("serializes writers with a short root lock", "replaces the file atomically", "under the existing lock", "one root `tasks.csv` remains authoritative"),
    ),
    FrozenInvariant(
        "durable intent owners",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("project purpose, value, behavior boundary, scope, stage, and version promise", "durable behavior detail", "technical rationale and durable costly choice", "local corrections -> outcome-focused task truth", "keep durable intent in these existing owners", "do not add a file or task column for intent"),
    ),
    FrozenInvariant(
        "stable owner after compaction",
        "AGENTS.md",
        ("stable 8-digit task owner supplied by the plugin hook", "remains resumable from repository truth and its ledger row after compaction"),
    ),
    FrozenInvariant(
        "owner-only close",
        "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md",
        ("owning lead alone decide task disposition", "close the accepted task through `tasks.py close`", "direct-user override requires an explicit request and recorded reason"),
    ),
    FrozenInvariant(
        "assisted and solo only",
        SUBAGENTS,
        ("assisted mode is the default", "solo mode is lead-only", "assisted and solo are the only orchestration modes"),
    ),
    FrozenInvariant(
        "architect owns decisions",
        SUBAGENTS,
        ("the architect is the sole authority for product intent", "the architect always owns intent, public behavior, architecture, tasks, acceptance, integration, and closeout", "never sends unresolved user input to a child", "writes inside an active child boundary", "accepts unreviewed output", "replaces independent proof with confidence", "the architect supplies a question and source boundary", "keep architecture, task setting, integration, and other consequential decisions with the architect"),
    ),
    FrozenInvariant(
        "engineer, maintainer, verifier, and scout roles",
        SUBAGENTS,
        ("| engineer |", "| maintainer |", "| verifier |", "| scout |", "the standard child roles are"),
    ),
    FrozenInvariant(
        "luna max primary and terra xhigh fallback",
        SUBAGENTS,
        ("model=gpt-5.6-luna", "reasoning_effort=max", "non-full-history `fork_turns`", "omit `agent_type`", "luna max uses standard service by default", "normal spawns omit `service_tier`", "service_tier=priority", "retry luna max", "gpt-5.6-terra", "terra `xhigh`", "directly spawn `gpt-5.6-terra` at `xhigh`", "without `service_tier` or `agent_type`"),
    ),
    FrozenInvariant(
        "one reusable child per role",
        SUBAGENTS,
        ("keep one reachable child thread for each role", "reuse or start engineer, verifier, maintainer, or read-only scout", "send a follow-up to a reachable role thread", "at most one reusable verifier", "at most one reusable maintainer"),
    ),
    FrozenInvariant(
        "stable child label and update start",
        SUBAGENTS,
        ("the architect owns each child name at spawn time", "valid name uses one lowercase role prefix", "allocates the next never-used label", "exact `task_name`", "a replacement takes the next label", "recycle the earliest label from an unreachable thread", "every child update starts with work or current state"),
    ),
    FrozenInvariant(
        "exact checkpoint barrier",
        SUBAGENTS,
        ("## checkpoint barrier", "identify the checkpoint by commit or exact working-tree fingerprint", "require the sidecar to confirm the identity before acting", "invalidate the result after any relevant source change"),
        ordered_terms=(
            "require all active work children to stop before integration",
            "architect reviews the combined implementation and scopes",
            "run any shared source-changing formatter or generator serially",
            "architect reviews resulting changes",
            "maintainer synchronizes affected shared docs",
            "pause all writers and identify the checkpoint by commit or exact working-tree fingerprint",
            "verifier checks both acceptance sets",
            "maintainer runs required build, package, deploy, flash, runtime, or smoke operations serially",
        ),
    ),
    FrozenInvariant(
        "learned operations",
        "plugins/lean-sdlc/skills/lean-sdlc/references/operations.md",
        ("unknown -> guided success -> recorded -> verified -> repeatable -> stale", "after success, the maintainer returns a short procedure draft", "the lead records it in optional `docs/OPERATIONS.md`", "later maintainer runs replay the recorded procedure exactly"),
    ),
    FrozenInvariant(
        "legacy ledger migration",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("tasks.py upgrade", "accepts the previous `parent` header and older planning header", "maps `repo` to `project` and `bootstrap` to `bootstrap`", "atomically writes one root csv under the existing lock"),
    ),
    FrozenInvariant(
        "applicable asd-ste100 guidance",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("asd-ste100 issue 9", "active voice", "20 words or fewer", "25 words or fewer", "one term for one meaning", "conditions before actions", "american english spelling", "preserve code, commands, paths, identifiers, protocol fields, quotations", "do not claim certified or full controlled-dictionary compliance"),
    ),
    FrozenInvariant(
        "modularity, edge cases, and mermaid diagrams",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("smallest cohesive units", "avoid project-size tiers, speculative interfaces, and pass-through modules", "plausible edge cases", "classify plausible edge cases as `handle`, `reject`, `defer`, or `impossible by invariant`", "small mermaid diagrams", "never use ascii pseudographics"),
    ),
    FrozenInvariant(
        "task sizing and compaction resume",
        "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
        ("one ledger task represents one engineer checkpoint", "require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review", "keep one task resumable from repository truth and its ledger row after compaction", "split a task for independent behavior, module outcome, proof, or work that needs an architect checkpoint", "do not use time or line-count limits"),
    ),
    FrozenInvariant(
        "qualified parallel writing and shared documentation",
        SUBAGENTS,
        ("at most two active children", "universal independence gate", "resource gate passes", "all dependencies are `done`", "separate mutable code and test paths", "stable read paths", "incidental outputs or caches", "public interface, schema, manifest, lockfile, generator, migration, or mutable fixture", "independent acceptance and proof", "engineer/engineer", "engineer/scout", "scout/scout", "a scout may overlap one verifier or maintainer only for future work with separate resources", "implementation writers stop before integration", "no writer overlaps documentation synchronization, verification, or stateful operations", "shared tests, docs, generators, and operations run serially", "named architect decision requires distinct source sets or enough material, data, or logs to pollute lead context", "maintainer synchronizes affected shared narrative documents", "engineer edits only assigned implementation paths", "maintainer edits only assigned shared-document paths", "verifier and scout are read-only", "no child edits `tasks.csv`", "stop before the shared resource and report the collision and checkpoint", "invalidate read findings after a source change", "a child never integrates sibling work"),
    ),
)


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _read(path: str) -> str:
    file = ROOT / path
    if not file.is_file():
        raise AssertionError(f"missing contract source: {path}")
    return file.read_text(encoding="utf-8")


def _lane_names(text: str) -> tuple[str, ...]:
    expected = {"shape", "decide", "plan", "diagnose", "deliver", "verify"}
    names = []
    for line in text.casefold().splitlines():
        match = re.match(r"\|\s*([^|]+?)\s*\|", line)
        if match and match.group(1).strip() in expected:
            names.append(match.group(1).strip())
    return tuple(names)


class FrozenInvariantHarnessTests(unittest.TestCase):
    def test_every_invariant_has_one_canonical_source(self) -> None:
        names = [invariant.name for invariant in FROZEN_INVARIANTS]
        self.assertEqual(len(FROZEN_INVARIANTS), 21)
        self.assertEqual(len(names), len(set(names)))
        for invariant in FROZEN_INVARIANTS:
            with self.subTest(invariant=invariant.name):
                self.assertIsInstance(invariant.source, str)
                self.assertTrue(invariant.source)
                self.assertTrue((ROOT / invariant.source).is_file())

    def test_every_invariant_terms_match_its_owner(self) -> None:
        for invariant in FROZEN_INVARIANTS:
            with self.subTest(invariant=invariant.name):
                source = _normalized(_read(invariant.source))
                for term in invariant.required_terms:
                    self.assertIn(_normalized(term), source, term)
                if invariant.ordered_terms:
                    positions = [source.index(_normalized(term)) for term in invariant.ordered_terms]
                    self.assertEqual(positions, sorted(positions))

    def test_lane_order_is_frozen(self) -> None:
        self.assertEqual(
            _lane_names(_read("README.md")),
            ("shape", "decide", "plan", "diagnose", "deliver", "verify"),
        )

    def test_policy_loading_is_conditional_on_delegation(self) -> None:
        dispatcher = _normalized(_read("plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"))
        self.assertIn("solo planning does not load child policy", dispatcher)
        self.assertIn("assisted delegation loads it before child use", dispatcher)
        self.assertIn("references/repository-contracts.md) only for initialization, legacy migration, or document ownership", dispatcher)

    def test_child_label_pool_is_ordered_unique_and_recycles_unreachable_labels(self) -> None:
        policy = _read(SUBAGENTS)
        match = re.search(r"allocates the next never-used label from `([^`]+)`", policy, re.I)
        self.assertIsNotNone(match)
        labels = tuple(label.strip() for label in match.group(1).split(","))
        expected = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega")
        self.assertEqual(labels, expected)
        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(policy.count(match.group(1)), 1)
        self.assertIn("a replacement takes the next label", policy.lower())
        self.assertIn("recycle the earliest label from an unreachable thread", policy.lower())

    def test_handoffs_require_facts_without_fixed_labels(self) -> None:
        policy = _read(SUBAGENTS)
        self.assertIn("outcome, boundary, contract, proof, and stop conditions", policy)
        self.assertIn("concise natural prose", policy)
        self.assertNotIn("Architecture alignment:", policy)
        self.assertNotIn("Return labels remain explicit", policy)
        self.assertNotIn("labeled report", policy)


if __name__ == "__main__":
    unittest.main()
