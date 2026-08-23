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
OPERATIONS = "plugins/lean-sdlc/skills/lean-sdlc/references/operations.md"
TRIGGER_EVALS = "plugins/lean-sdlc/skills/lean-sdlc/references/trigger-evals.md"


FROZEN_INVARIANTS = (
    FrozenInvariant(
        "public workflow",
        "README.md",
        (
            "## How it works",
            "Understand the intent",
            "Choose the approach",
            "Create owned tasks",
            "Implement",
            "Verify the result",
            "Update repository truth",
        ),
        (
            "Understand the intent",
            "Choose the approach",
            "Create owned tasks",
            "Implement",
            "Verify the result",
            "Update repository truth",
        ),
    ),
    FrozenInvariant(
        "explicit implementation authority",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("require explicit implementation authority before task creation or changes", "discussion and proposals remain read-only", "if ambiguous, remain read-only"),
    ),
    FrozenInvariant(
        "natural intent gate",
        "plugins/lean-sdlc/skills/lean-sdlc/references/shape.md",
        ("shape owns the complete intent gate", "why -> what -> how -> proof", "shape settles why and what", "decide and plan add how and proof", "present problem or opportunity and affected user or business value", "smallest observable outcome plus constraints and non-goals", "technical approach and task shape after why and what are stable", "proof: acceptance and verification", "material assumption affects behavior, scope, or architecture", "stop for user confirmation", "intent is clear and implementation authority is explicit", "brainstorming and rephrasing remain read-only"),
    ),
    FrozenInvariant(
        "owned task before writes",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("before any other repository mutation", "run `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" start` or claim planned work", "require an owned `in progress` task", "run `python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write"),
    ),
    FrozenInvariant(
        "atomic tasks.csv transactions",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("serializes writers with a short root lock", "replaces the file atomically", "under the existing lock", "one root `tasks.csv` remains authoritative"),
    ),
    FrozenInvariant(
        "sparse user-controlled backlog",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        (
            "A Backlog row has Status `Backlog`",
            "carries values only for `Task ID`, `Title`, `Status`, and `Context`",
            "`Bootstrap` and `Quick Fix` are invalid Backlog contexts",
            "No task may depend on a Backlog task",
            "Only a direct user request may add or promote Backlog work",
            "matching an existing Backlog title is promotion authority without an exact ID",
            "Before creating new Standard work",
            "Do not load Backlog on startup, resume, brainstorming, or Quick Fix work",
            "Promotion adds proper title sizing, acceptance, proof, and dependencies",
            "Promotion to In Progress adds an owner",
            "Planned promotion is not implementation authority",
        ),
    ),
    FrozenInvariant(
        "durable intent owners",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("project purpose, value, behavior boundary, scope, stage, and version promise", "durable behavior detail", "technical rationale and durable costly choice", "local corrections -> outcome-focused task truth", "keep durable intent in these existing owners", "do not add a file or task column for intent"),
    ),
    FrozenInvariant(
        "stable owner after compaction",
        "AGENTS.md",
        ("plugin hook supplies a stable 8-digit task owner",),
    ),
    FrozenInvariant(
        "owner-only close",
        "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md",
        ("owning lead decides disposition", "close the accepted task through `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" close`", "direct-user override requires explicit request and recorded reason"),
    ),
    FrozenInvariant(
        "assisted and solo only",
        SUBAGENTS,
        ("assisted mode is the default", "solo mode is lead-only", "assisted and solo are the only orchestration modes"),
    ),
    FrozenInvariant(
        "architect owns decisions",
        SUBAGENTS,
        ("the architect is the sole authority for product intent", "the architect always owns intent, public behavior, architecture, tasks, acceptance, integration, and closeout", "never sends unresolved user input to a child", "writes inside an active child boundary", "accepts unreviewed output", "replaces independent proof with confidence", "the architect supplies a question and source boundary"),
    ),
    FrozenInvariant(
        "lifecycle availability and controlled proof routing",
        SUBAGENTS,
        (
            "running lifecycle state means available",
            "parent wait timeout, missed update, or silence is not failure",
            "the architect may request status and wait again",
            "a completed child sends one final return and ends its active turn",
            "the completed thread remains reachable for later `followup_task` reuse",
            "the architect allocates and preauthorizes the exact named verifier",
            "descendants count toward the limit",
            "short visible natural restatement",
            "short visible alignment signoff covering architecture, scope, and contract alignment",
            "stops writing while its nested read-only verifier checks",
            "permitted implementation corrections",
            "then reruns proof",
            "engineer may fix only implementation defects that preserve settled behavior",
            "same proof failure repeats",
        ),
    ),
    FrozenInvariant(
        "delegated evidence and checkpoint capture",
        SUBAGENTS,
        (
            "product intent, public behavior, architecture, assumptions, acceptance, permissions, task ownership, conflict resolution, and final signoff",
            "cross-boundary source and log evidence",
            "focused semantic changes and targeted check results",
            "contract-sensitive semantic changes",
            "before and after proof",
            "same explicit task-owned paths",
            "compares the returned SHA-256 values locally",
            "Verifier blocks if the local values differ",
            "does not persist values or expose full values in routine reports",
            "do not make the architect calculate them",
            "recorded operation failure signal",
            "already-authorized recorded recovery",
            "unknown, ambiguous, source-changing, or new retry behavior",
            "routes to Diagnose/Scout and Architect",
        ),
        ordered_terms=(
            "before and after proof",
            "same explicit task-owned paths",
            "compares the returned SHA-256 values locally",
            "Verifier blocks if the local values differ",
        ),
    ),
    FrozenInvariant(
        "engineer, maintainer, verifier, and scout roles",
        SUBAGENTS,
        (
            "the standard child roles are engineer, maintainer, verifier, and scout",
            "apply this stage-aware chain before the first command",
            "keep unresolved product, architecture, scope, permission, or acceptance decisions with the architect",
            "route broad, read-only, multi-platform, multi-version, or cross-boundary evidence inquiries to scout",
            "route settled mutable implementation with paths, interfaces, acceptance, proof, and no open decision to engineer",
            "route independent proof to verifier only at a proof checkpoint",
            "route shared documentation or recorded operations to maintainer only after accepted implementation",
        ),
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
        "stable child label and event-driven progress",
        SUBAGENTS,
        (
            "the architect owns each child name at spawn time",
            "valid name uses one lowercase role prefix",
            "allocates the next never-used label",
            "exact `task_name`",
            "a replacement takes the next label",
            "recycle the earliest label from an unreachable thread",
            "1–3 natural sentences",
            "current action, why it matters, observed result or next action",
            "routine progress stays in the child thread",
            "send an explicit parent message only when immediate architect action is required",
            "blocker, collision, scope change, proof mismatch, or decision",
            "at completion, send exactly one final return",
            "the architect does not echo unchanged child facts",
            "completed child sends one final return",
            "ends its active turn",
            "the completed thread remains reachable for later `followup_task` reuse",
            "no child update includes greetings, role repetition, raw logs, full fingerprints, or scripted phrases",
            "do not create rigid templates",
        ),
        ordered_terms=(
            "routine progress stays in the child thread",
            "send an explicit parent message only when immediate architect action is required",
            "at completion, send exactly one final return",
            "the architect does not echo unchanged child facts",
        ),
    ),
    FrozenInvariant(
        "exact checkpoint barrier",
        SUBAGENTS,
        ("## checkpoint barrier", "runs the packaged checkpoint helper before and after proof over the same explicit task-owned paths", "do not persist values or expose full values in routine reports", "blocks when the local checkpoint values differ", "do not make the architect calculate them", "release tag or short commit id", "invalidate the result after any relevant source change"),
        ordered_terms=(
            "require all active work children to stop before integration",
            "architect reviews the combined implementation and scopes",
            "run any shared source-changing formatter or generator serially",
            "architect reviews resulting changes",
            "maintainer synchronizes affected shared docs",
            "pause all writers for machine verification. the verifier runs the packaged checkpoint helper before and after proof over the same explicit task-owned paths, then compares values locally",
            "the verifier checks both acceptance sets, assigned-path separation",
            "the verifier checks both acceptance sets, assigned-path separation, semantic interaction, and documentation parity. it blocks when the local checkpoint values differ",
            "after commit, use the release tag or short commit id",
            "maintainer runs required build, package, deploy, flash, runtime, or smoke operations serially",
        ),
    ),
    FrozenInvariant(
        "external-tool routing",
        SUBAGENTS,
        (
            "## external tools",
            "external-tool routing starts before substantial",
            "target, permissions, constraints, architecture, decisions, and final acceptance",
            "one bounded probe",
            "more than three external calls",
            "large schemas/logs/inventories/search results",
            "one operation repeats across objects",
            "tool discovery is required",
            "error recovery needs several diagnostic calls",
            "output needs reduction before a decision",
            "read-heavy discovery and reduction to scout",
            "cross-boundary source and log evidence",
            "approved mutations to engineer",
            "repeated build/export/import/deploy/flash procedures to maintainer",
            "independent checks to verifier",
            "bounded programmatic tool calling",
            "direct calls for mutations, approvals, or judgment-sensitive steps",
            "inside the assigned child",
            "routine mutation calls belong to the assigned engineer or maintainer, not the architect",
            "one agent owns each mutable external target",
            "never let two agents mutate the same project, database, deployment, or hardware target",
            "not a raw transcript",
            "same tool and project",
            "material tool or target change",
            "compaction during tool work",
            "several direct routine calls",
            "repeated large output",
            "two failed tool attempts",
            "architect summarizing data instead of deciding",
            "reroute remaining work to luna max or bounded programmatic calls",
            "mention optimization only when routing changes",
        ),
    ),
    FrozenInvariant(
        "complete authoritative reads",
        SUBAGENTS,
        (
            "group independent read-only discovery into bounded calls",
            "follow-ups only for unresolved questions",
            "bound output only when shape or presence is enough",
            "complete reads for selected skill instructions, contracts, acceptance, proof, patches, and exact evidence",
        ),
    ),
    FrozenInvariant(
        "bounded probes and waits",
        SUBAGENTS,
        (
            "execution economy",
            "one grouped read-only environment probe before setup",
            "setup and installation require owned authority",
            "never install dependencies automatically",
            "bounded adaptive waits",
            "avoid rapid polling",
        ),
    ),
    FrozenInvariant(
        "diagnostic retry routing",
        "plugins/lean-sdlc/skills/lean-sdlc/references/diagnose.md",
        (
            "equivalent failure repeats without new evidence",
            "stop the patch loop",
            "reassess the hypothesis and fault boundary",
        ),
    ),
    FrozenInvariant(
        "proof anchor and justified forward checks",
        "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md",
        (
            "task proof as the acceptance anchor",
            "required acceptance, regression, structure, and documentation layers",
            "stop after all required proof passes",
            "add an always-on rule only for an observed failure",
            "smallest behavioral evaluation that fails before the rule and passes after it",
        ),
        ordered_terms=(
            "task proof as the acceptance anchor",
            "required acceptance, regression, structure, and documentation layers",
            "stop after all required proof passes",
        ),
    ),
    FrozenInvariant(
        "learned operations",
        OPERATIONS,
        ("unknown -> guided success -> recorded -> verified -> repeatable -> stale", "after success, the maintainer returns a short procedure draft", "the lead records it in optional `docs/OPERATIONS.md`", "later maintainer runs replay the recorded procedure exactly"),
    ),
    FrozenInvariant(
        "recorded automation catalog",
        OPERATIONS,
        (
            "reuse recorded operations as the only automation catalog",
            "any child that directly observes a second equivalent successful mechanic reports a transient automation candidate to the architect",
            "after accepted implementation, maintainer owns record/replay",
            "the report adds no scan, registry, backlog entry, automatic script, or state",
            "direct evidence that the mechanic will recur",
            "candidates do not enter durable docs automatically",
            "architect approves the contract before scripting",
            "existing project command or target",
            "existing script",
            "native or installed tool",
            "smallest new script",
            "stable repeated mechanic",
            "a script never grants authority",
        ),
    ),
    FrozenInvariant(
        "automation runtime and failure contract",
        OPERATIONS,
        (
            "explicit inputs and safe defaults",
            "validate the target",
            "stable exit status",
            "run noninteractive",
            "write output atomically when practical",
            "omit secrets and machine-specific paths",
            "bound default output",
            "detailed logs only on failure or explicit request",
            "dry-run only when mutation risk is meaningful",
            "transient signal may retry only under recorded recovery",
            "recorded failure follows authorized recovery",
            "script defect goes to engineer",
            "changed contract or unknown cause stops and returns to architect/diagnose",
        ),
    ),
    FrozenInvariant(
        "automation role routing",
        OPERATIONS,
        (
            "architect approves the contract before scripting",
            "engineer implements an approved script and one focused runnable check",
            "maintainer records and later replays the canonical command",
            "solo follows the same record",
            "maintainer marks an automation as stale",
            "architect approves meaning changes",
        ),
    ),
    FrozenInvariant(
        "automation trigger evaluations",
        TRIGGER_EVALS,
        (
            "these rows are scenarios and assertions",
            "they are not a second policy source",
            "proof and operation rules are in [verify.md](verify.md) and [operations.md](operations.md)",
            "automation lifecycle and stateful operation",
            "any child reports a transient candidate after directly observing a second equivalent success",
            "no scan, registry, backlog entry, or automatic script",
        ),
    ),
    FrozenInvariant(
        "legacy ledger migration",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        ("python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" upgrade", "accepts the previous `parent` header and older planning header", "maps `repo` to `project` and `bootstrap` to `bootstrap`", "atomically writes one root csv under the existing lock"),
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
       "single-area task sizing and compaction resume",
       "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
       (
           "before task creation",
           "one behavior, one contract boundary, one proof cluster, and one accept-or-reject decision",
           "split on any independent answer",
           "and` in a title as a review signal, not an automatic split",
           "one ledger task represents one engineer checkpoint",
           "one independently accepted behavior change",
           "one owning contract boundary",
           "one proof cluster",
           "one close decision",
           "may touch several files, tests, documentation, or migration steps",
           "only when all work is inseparable for that behavior",
           "split a task when a part can succeed, fail, defer, revert, release, or be accepted independently",
           "belongs to another behavior or contract area",
           "needs another architect decision",
           "keep a correction in the same task",
           "only satisfies unchanged acceptance",
           "a new behavior needs a new task",
           "never size by elapsed time, file count, line count, or command count",
           "require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review",
           "keep one task resumable from repository truth and its ledger row after compaction",
       ),
   ),
    FrozenInvariant(
        "deterministic ledger plan projection",
        "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
        ("## plan view projection", "`python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" open` supplies unresolved `planned` and `in progress` rows", "excludes backlog", "update_plan", "task-nnn — title", "planned` to `pending", "in progress` to `in_progress", "closing row `completed`", "before or with `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" close`", "active close transition", "only unresolved non-backlog rows", "do not load full `done` history", "startup, resume, clear, or compaction", "brainstorming and rephrasing remain read-only", "every unresolved task in its own exact row", "parallel work changes status or plan prose, never task identity", "`tasks.csv` remains authoritative"),
    ),
    FrozenInvariant(
        "quick fix plan classification",
        "plugins/lean-sdlc/skills/lean-sdlc/references/plan.md",
        (
            "Quick Fix is inline Plan classification",
            "not a mode, lane, task type, or prompt",
            "Record Context `Quick Fix`",
            "exact requested outcome",
            "local reversible scope",
            "no unresolved product, design, architecture, public interface, schema, migration, dependency, security, generated-file, or external-state choice",
            "one immediate narrow proof",
            "request to use Quick Fix never bypasses eligibility",
            "one visible plan item",
            "one owned task",
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write",
            "Architect may execute Quick Fix in Assisted or Solo",
            "Do not spawn Engineer, Maintainer, or Verifier per Quick Fix",
            "Shared batch may reuse or start Verifier when normal proof trigger applies",
            "Review diff and run narrow proof before close",
            "Quick-only multi-fix batch",
            "Standalone remains pending",
            "names exact",
            "`TASK-NNN — Title`",
        ),
    ),
    FrozenInvariant(
        "quick fix batch assurance",
        "plugins/lean-sdlc/skills/lean-sdlc/references/repository-contracts.md",
        (
            "Closing a Quick Fix records pending broad batch review",
            "`python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" quick-fixes` lists completed Quick Fixes that remain unreviewed",
            "Standard checkpoint reviews every pending Quick Fix",
            "`--review-through TASK-NNN`",
            "review prefix must contain only `Done` Quick Fix tasks through the target",
            "Invalid review references fail without ledger mutation",
            "several Quick Fixes may defer broad checks until one shared checkpoint",
            "A standalone Quick Fix may remain pending",
            "failed shared review creates a Standard correction task",
            "Deferred Quick Fix assurance is not automatic technical debt",
        ),
    ),
   FrozenInvariant(
       "qualified parallel writing and shared documentation",
        SUBAGENTS,
        (
            "at most two active children",
            "universal independence gate",
            "resource gate passes",
            "all dependencies are `done`",
            "separate mutable code and test paths",
            "stable read paths",
            "incidental outputs or caches",
            "public interface, schema, manifest, lockfile, generator, migration, or mutable fixture",
            "independent acceptance and proof",
            "engineer/engineer",
            "engineer/scout",
            "scout/scout",
            "a scout may overlap one verifier or maintainer only for future work with separate resources",
            "implementation writers stop before integration",
            "no writer overlaps documentation synchronization, verification, or stateful operations",
            "shared tests, docs, generators, and operations run serially",
            "route broad, read-only, multi-platform, multi-version, or cross-boundary evidence inquiries to scout",
            "for a broad inquiry, the architect names platform and version dimensions",
            "scout maps shared core, variants, affected coverage, cited evidence, and unknowns before broad reads",
            "architect reads decisive contracts and cited paths, expands one unresolved boundary at a time",
            "reuse existing build graphs, manifests, and maps before creating anything",
            "maintainer synchronizes affected shared narrative documents",
            "engineer edits only assigned implementation paths",
            "maintainer edits only assigned shared-document paths",
            "verifier and scout are read-only",
            "no child edits `tasks.csv`",
            "stop before the shared resource and report the collision and checkpoint",
            "invalidate read findings after a source change",
            "a child never integrates sibling work",
        ),
    ),
)


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _read(path: str) -> str:
    file = ROOT / path
    if not file.is_file():
        raise AssertionError(f"missing contract source: {path}")
    return file.read_text(encoding="utf-8")


class FrozenInvariantHarnessTests(unittest.TestCase):
    def test_every_invariant_has_one_canonical_source(self) -> None:
        names = [invariant.name for invariant in FROZEN_INVARIANTS]
        self.assertEqual(len(FROZEN_INVARIANTS), 36)
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

    def test_lane_contracts_keep_ownership_within_the_compact_word_cap(self) -> None:
        lanes = {
            name: _read(f"plugins/lean-sdlc/skills/lean-sdlc/references/{name}.md")
            for name in ("shape", "plan", "deliver", "verify")
        }
        self.assertLessEqual(sum(len(text.split()) for text in lanes.values()), 2100)
        for term in [
            "shape owns the complete intent gate",
            "material assumption affects behavior, scope, or architecture",
        ]:
            self.assertIn(term, lanes["shape"].casefold())
        for term in ["tasks.py", "update_plan", "one engineer checkpoint"]:
            self.assertIn(term, lanes["plan"].casefold())
        self.assertIn("owned `in progress` task", lanes["deliver"].casefold())
        self.assertIn("architect reviews scope, architecture, contract alignment", lanes["deliver"].casefold())
        for term in [
            "acceptance proof",
            "documentation parity",
            "close the accepted task through `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" close`",
        ]:
            self.assertIn(term, lanes["verify"].casefold())

    def test_policy_loading_is_conditional_on_delegation(self) -> None:
        dispatcher = _normalized(_read("plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"))
        agents = _normalized(_read("AGENTS.md"))
        self.assertIn("solo planning does not load child policy", dispatcher)
        self.assertIn("assisted delegation loads it before child use", dispatcher)
        self.assertIn("references/repository-contracts.md) only for initialization, legacy migration, or document ownership", dispatcher)
        for phrase in [
            "[shape](references/shape.md)",
            "[plan](references/plan.md)",
            "tasks.py",
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write",
            "update_plan",
            "python3 \"<skill-root>/scripts/session_state.py\" --owner owner --mode assisted|solo",
        ]:
            self.assertIn(_normalized(phrase), dispatcher)
        for phrase in [
            "tasks.py",
            "references/repository-contracts.md",
            "subagents.md",
            "dependencies must be `done` before start",
        ]:
            self.assertIn(_normalized(phrase), agents)
        self.assertNotIn("github.com/laikrodiz", agents)
        self.assertIn("references/repository-contracts.md", agents)
        self.assertIn("references/subagents.md", agents)

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
        shape = _read("plugins/lean-sdlc/skills/lean-sdlc/references/shape.md")
        verify = _read("plugins/lean-sdlc/skills/lean-sdlc/references/verify.md")
        operations = _read("plugins/lean-sdlc/skills/lean-sdlc/references/operations.md")
        evaluations = _read("plugins/lean-sdlc/skills/lean-sdlc/references/trigger-evals.md")

        self.assertIn(
            "Intent fact order: `<reason> -> <outcome> -> <boundary> -> <approach> -> <proof>`",
            shape,
        )
        self.assertIn(
            "Angle-bracket terms are abstract fact slots. Replace them with project facts; never copy the wording or show slot labels.",
            shape,
        )
        self.assertIn(
            "Arrow sequence is fact order, not output wording: `<task or inquiry> -> <outcome> -> <owned boundary> -> <contract> -> <proof> -> <stop>`",
            policy,
        )
        self.assertIn(
            "Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`",
            verify,
        )
        self.assertIn(
            "Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`",
            verify,
        )
        for document in (verify, operations):
            self.assertIn("Arrow sequence is fact order, not output wording", document)
            self.assertIn("replace slots with project facts and omit slot labels", document)
        self.assertIn(
            "Visible operation result order: `<status> -> <target> -> <artifact> -> <next Architect action>`",
            operations,
        )
        self.assertIn("internal machine handoff", operations)
        self.assertIn("Omit them from visible operation reports", operations)
        self.assertNotIn("Request these labeled fields", operations)
        self.assertNotIn("Return these labeled fields", operations)
        self.assertNotIn("```", operations)
        self.assertIn("Use natural prose and fact order", evaluations)
        self.assertIn("do not expose chain-of-thought or rigid scripts", evaluations)
        self.assertIn("replace slots with project facts and omit slot labels", policy)
        self.assertIn("concise natural prose", policy)
        self.assertNotIn("Architecture alignment:", policy)
        self.assertNotIn("Return labels remain explicit", policy)
        self.assertNotIn("labeled report", policy)

    def test_child_communication_is_event_driven_without_policy_drift(self) -> None:
        policy = _normalized(_read(SUBAGENTS))
        evaluations = _normalized(_read(TRIGGER_EVALS))
        for document in (policy, evaluations):
            self.assertIn("routine progress stays in the child thread", document)
            self.assertIn("explicit parent message", document)
            self.assertIn("immediate architect action", document)
            self.assertIn("blocker", document)
            self.assertIn("collision", document)
            self.assertIn("scope change", document)
            self.assertIn("proof mismatch", document)
            self.assertIn("decision", document)
            self.assertIn("one final return", document)
            self.assertIn("architect does not echo unchanged child facts", document)
        self.assertNotIn("after about two minutes of otherwise silent work", evaluations)


if __name__ == "__main__":
    unittest.main()
