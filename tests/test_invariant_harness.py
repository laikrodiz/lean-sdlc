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
CHILD = "plugins/lean-sdlc/skills/lean-sdlc/references/child.md"
OPERATIONS = "plugins/lean-sdlc/skills/lean-sdlc/references/operations.md"
VERIFY = "plugins/lean-sdlc/skills/lean-sdlc/references/verify.md"
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
        "exact startup context",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        (
            "exact startup fields from the lifecycle system message",
            "system message supplies `Repository root`, `Skill root`, `Tasks helper`, `Check helper`, `State helper`, `Owner`, `Mode`, and `Child tier`",
            "`repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, `mode`, and `tier`",
            "the `Skill root` is the parent of the loaded `SKILL.md`",
            "`python3 \"<directory containing the loaded SKILL.md>/scripts/session_state.py\" --context`",
            "existing `CODEX_SESSION_ID`",
            "never set, replace, or invent `CODEX_SESSION_ID`",
            "fallback fails when `CODEX_SESSION_ID` is absent",
            "only this fallback returns structured JSON with snake_case fields",
            "use returned fields, paths, and owner exactly",
            "never reconstruct paths",
            "shorten cache paths",
            "search for helpers",
            "placeholder owners",
        ),
    ),
    FrozenInvariant(
        "natural intent gate",
        "plugins/lean-sdlc/skills/lean-sdlc/references/shape.md",
        ("shape owns the complete intent gate", "why -> what -> how -> proof", "shape settles why and what", "decide and plan add how and proof", "present problem or opportunity and affected user or business value", "smallest observable outcome plus constraints and non-goals", "technical approach and task shape after why and what are stable", "proof: acceptance and verification", "material assumption affects behavior, scope, or architecture", "stop for user confirmation", "intent is clear and implementation authority is explicit", "brainstorming and rephrasing remain read-only"),
    ),
    FrozenInvariant(
        "owned task before writes",
        "plugins/lean-sdlc/skills/lean-sdlc/SKILL.md",
        ("before any other repository mutation", "run `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" start` or claim planned work", "require an owned `in progress` task", "run `python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write --task TASK-ID --owner OWNER"),
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
        VERIFY,
        ("only the owning architect closes through `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" close` with evidence", "direct-user override requires an explicit request and recorded reason"),
    ),
    FrozenInvariant(
        "assisted and solo only",
        SUBAGENTS,
        ("assisted is the default", "solo is lead-only", "these are the only modes"),
    ),
    FrozenInvariant(
        "assisted direct local exception",
        SUBAGENTS,
        (
            "one understood, settled local change with the architect",
            "handoff overhead exceeds the work",
            "bounded judgment-intensive implementation",
            "visible plan, owned task, before-write gate",
            "risk-based independent review",
            "delegate separable substantial execution",
            "not blanket permission",
        ),
    ),
    FrozenInvariant(
        "atomic engineer ownership",
        CHILD,
        (
            "complete one atomic outcome, including related tests and mechanical consistency inside assigned paths",
            "local corrections without new approval",
            "architecture, interfaces, behavior, acceptance, permissions, and ownership remain unchanged",
            "escalate repeated equivalent failures without new evidence",
            "only an exact architect-preauthorized verifier",
            "no other child spawning",
        ),
    ),
    FrozenInvariant(
        "bounded child capacity and resource isolation",
        SUBAGENTS,
        (
            "use at most two active work children",
            "a third child may be read-only when native capacity permits useful elapsed-time savings",
            "never exceed two concurrent engineers",
            "count all descendants",
            "writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap",
            "shared read-only contracts are stable",
            "two engineers may share stable read-only interfaces",
            "do not create branches or worktrees for parallelism",
            "maintainer may draft separate documents from approved facts during implementation",
            "a verifier can check a completed independent boundary while unrelated work continues",
            "final release checks freeze all inputs that enter the release",
        ),
    ),
    FrozenInvariant(
        "proof ownership and reuse",
        VERIFY,
        (
            "task proof is the acceptance anchor",
            "do not create a proof registry",
            "one command may satisfy multiple proof purposes",
            "reuse proof only while relevant source, dependencies, configuration, environment, toolchain, and target inputs remain valid",
            "a changed dependency invalidates proof",
            "repeat affected checks after relevant changes",
            "without a duplicate preliminary suite",
        ),
    ),
    FrozenInvariant(
        "proof aggregation",
        VERIFY,
        (
            "stop writers touching them, including dependencies",
            "verifier runs",
            "before and after proof",
            "compare returned sha-256 values locally",
            "block on mismatch",
            "collect independent safe failures together",
            "skip checks whose prerequisite failed",
            "run only missing or invalidated checks",
        ),
    ),
    FrozenInvariant(
        "artifact reuse",
        OPERATIONS,
        (
            "reuse it when source, dependencies, configuration, environment, toolchain, and target match",
            "build or package only missing or invalidated artifacts",
            "never repeat deployment or flashing merely because a later check needs the result",
            "a failed prerequisite blocks dependent operations, not unrelated safe checks",
        ),
    ),
    FrozenInvariant(
        "canonical child boundaries",
        CHILD,
        (
            "use this entry for an architect-assigned child",
            "common boundary",
            "supplied task facts",
            "work only within the assigned boundary",
            "no ledger edits, git mutations, or sibling integration",
            "follow [verify.md](verify.md)",
            "refresh relevant changed inputs",
        ),
    ),
    FrozenInvariant(
        "architect owns decisions",
        SUBAGENTS,
        (
            "the architect owns intent, public behavior, architecture, material assumptions, interfaces, permissions, task ownership, acceptance, conflict resolution, integration, and final signoff",
            "keep unresolved product, architecture, scope, permission, or acceptance decisions with the architect",
            "the architect owns target, permission, constraints, and decisions",
            "only the architect allocates children",
            "never let a child integrate sibling work",
            "never substitute confidence for required independent proof",
        ),
    ),
    FrozenInvariant(
        "lifecycle availability and controlled proof routing",
        CHILD,
        (
            "send one final return with outcome, focused changes or citations, proof, and remaining risks",
            "the thread can be reused later",
            "only an exact architect-preauthorized verifier",
            "pause its verified inputs during checks",
            "no child spawning",
            "if scope, authority, assumptions, or proof becomes unclear, stop affected work and report it",
        ),
    ),
    FrozenInvariant(
        "child evidence and scope reports",
        CHILD,
        (
            "short natural progress updates",
            "outcome, focused changes or citations, proof, and remaining risks",
            "no greetings, role repetition, rigid phrases, raw log dumps, or full fingerprints",
            "stop before the shared resource",
            "refresh evidence after relevant inputs change",
            "send one final return",
        ),
    ),
    FrozenInvariant(
        "engineer, maintainer, verifier, and scout roles",
        CHILD,
        (
            "### Engineer",
            "### Scout",
            "### Maintainer",
            "### Verifier",
            "complete one atomic outcome",
            "remain read-only",
            "follow [verify.md](verify.md)",
            "no child spawning",
        ),
    ),
    FrozenInvariant(
        "luna max primary and terra xhigh fallback",
        SUBAGENTS,
        ("model=gpt-5.6-luna", "reasoning_effort=max", "fork_turns=none` or a positive bounded history value", "omit `agent_type`", "standard luna omits `service_tier`", "user-enabled fast children", "service_tier=priority", "retry luna max", "gpt-5.6-terra", "reasoning_effort=xhigh", "no `service_tier` or `agent_type`"),
    ),
    FrozenInvariant(
        "one reusable child per role",
        SUBAGENTS,
        ("reuse a reachable child for the same role and relevant context before replacement", "keep one reusable maintainer and verifier", "use a second engineer or scout only for a qualified parallel assignment", "completed children remain reusable through `followup_task`"),
    ),
    FrozenInvariant(
        "stable child label and event-driven progress",
        SUBAGENTS,
        (
            "choose a lowercase role prefix and greek suffix",
            "allocate the next unused label",
            "keep the exact name with the reusable child",
            "recycle an unused role-label combination from an unreachable child",
        ),
    ),
    FrozenInvariant(
        "event-driven child progress",
        CHILD,
        (
            "short natural progress updates",
            "progress updates in the child thread",
            "send an explicit parent message only for immediate action",
            "a blocker, collision, scope change, proof mismatch, or decision",
            "one final return",
            "end the active turn",
            "the thread can be reused later",
        ),
        ordered_terms=(
            "progress updates in the child thread",
            "send an explicit parent message only for immediate action",
            "one final return",
        ),
    ),
    FrozenInvariant(
        "exact checkpoint barrier",
        VERIFY,
        (
            "stop writers touching them, including dependencies",
            "verifier runs `python3 \"<skill-root>/scripts/checkpoint.py\" --repo \"<repo-root>\" PATH [PATH ...]`",
            "before and after proof",
            "compare returned SHA-256 values locally",
            "block on mismatch",
            "collect independent safe failures together",
            "skip checks whose prerequisite failed",
            "stop after all required proof passes",
        ),
        ordered_terms=(
            "stop writers touching them, including dependencies",
            "verifier runs",
            "before and after proof",
            "compare returned sha-256 values locally",
            "collect independent safe failures together",
            "stop after all required proof passes",
        ),
    ),
    FrozenInvariant(
        "external-tool routing",
        SUBAGENTS,
        (
            "apply the same roles and routing precedence to plugins, mcp, connectors, cad, databases, and hardware",
            "expected time or context savings outweigh handoff and verification costs",
            "the architect owns target, permission, constraints, and decisions",
            "one bounded probe",
            "call count and tool discovery are cues, not mandatory delegation triggers",
            "group independent read-only calls",
            "return conclusions, evidence locations, errors, and unknowns",
            "direct calls for mutations, approvals, and judgment-sensitive steps",
            "never let two agents mutate the same external target",
            "reuse the same child for the same tool and project",
            "refresh only changed or unresolved boundaries",
        ),
    ),
    FrozenInvariant(
        "complete authoritative reads",
        SUBAGENTS,
        (
            "group independent read-only calls and reduce logs inside the assigned child",
            "read selected instructions, contracts, acceptance, patches, and decisive evidence completely",
            "reuse existing maps, build graphs, and cited source locations",
            "refresh only changed or unresolved boundaries",
        ),
    ),
    FrozenInvariant(
        "bounded probes and waits",
        SUBAGENTS,
        (
            "one bounded probe may settle the assignment",
            "bounded adaptive waits without rapid polling",
            "do not warm caches artificially",
            "never silently change the selected architect model or effort",
        ),
    ),
    FrozenInvariant(
        "delegation profile and capacity checks",
        SUBAGENTS,
        (
            "before spawning, confirm mode, capacity, profile, name, reachable children, scope, authority, and return route",
            "run one bounded profile smoke check after a relevant native model/tool change",
            "bounded adaptive waits without rapid polling",
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
        VERIFY,
        (
            "task proof is the acceptance anchor",
            "targeted proof checks changed behavior",
            "acceptance proof checks observable completion",
            "regression proof checks affected-boundary risk",
            "these are purposes, not three mandatory commands",
            "stop after all required proof passes",
        ),
        ordered_terms=(
            "task proof is the acceptance anchor",
            "targeted proof checks changed behavior",
            "acceptance proof checks observable completion",
            "regression proof checks affected-boundary risk",
            "stop after all required proof passes",
        ),
    ),
    FrozenInvariant(
        "learned operations",
        OPERATIONS,
        (
            "unknown -> guided success -> recorded -> verified -> repeatable -> stale",
            "after success, the maintainer returns a short procedure draft",
            "after architect approval, the maintainer records it",
            "later maintainer runs replay the recorded procedure exactly",
        ),
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
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write --task TASK-ID --owner OWNER",
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
            "use at most two active work children",
            "a third child may be read-only when native capacity permits useful elapsed-time savings",
            "never exceed two concurrent engineers",
            "count all descendants",
            "each task has independent acceptance and all ledger dependencies are `done`",
            "writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap",
            "shared read-only contracts are stable",
            "two engineers may share stable read-only interfaces",
            "do not create branches or worktrees for parallelism",
            "a verifier can check a completed independent boundary while unrelated work continues",
            "if separation or benefit is unclear, run serially",
            "maintainer may draft separate documents from approved facts during implementation",
            "never let a child integrate sibling work",
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
        self.assertTrue(FROZEN_INVARIANTS)
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

    def test_lane_contracts_preserve_ownership_and_proof_boundaries(self) -> None:
        lanes = {
            name: _read(f"plugins/lean-sdlc/skills/lean-sdlc/references/{name}.md")
            for name in ("shape", "plan", "deliver", "verify", "operations")
        }
        for term in [
            "shape owns the complete intent gate",
            "material assumption affects behavior, scope, or architecture",
        ]:
            self.assertIn(term, lanes["shape"].casefold())
        for term in ["tasks.py", "update_plan", "one engineer checkpoint"]:
            self.assertIn(term, lanes["plan"].casefold())
        for term in [
            "record the proof owner, purpose, and invalidation inputs",
            "use [verify.md](verify.md) for proof coverage, reuse, and invalidation",
        ]:
            self.assertIn(term, lanes["plan"].casefold())
        for term in [
            "task proof is the acceptance anchor",
            "proof purpose",
            "invalidation inputs",
            "one command may satisfy multiple proof purposes",
            "do not create a proof registry",
        ]:
            self.assertIn(term, lanes["verify"].casefold())
        self.assertIn("owned `in progress` task", lanes["deliver"].casefold())
        self.assertIn("architect reviews scope, architecture, contract alignment", lanes["deliver"].casefold())
        for term in [
            "acceptance proof",
            "documentation parity",
            "collect independent safe failures together",
            "only the owning architect closes through `python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" close`",
        ]:
            self.assertIn(term, lanes["verify"].casefold())
        self.assertIn(
            "reuse it when source, dependencies, configuration, environment, toolchain, and target match",
            lanes["operations"].casefold(),
        )

    def test_policy_loading_is_conditional_on_delegation(self) -> None:
        dispatcher = _normalized(_read("plugins/lean-sdlc/skills/lean-sdlc/SKILL.md"))
        agents = _normalized(_read("AGENTS.md"))
        self.assertIn("in assisted, load [subagents.md]", dispatcher)
        self.assertIn("solo does not need child orchestration", dispatcher)
        self.assertIn("references/repository-contracts.md) only for initialization, legacy migration, or document ownership", dispatcher)
        for phrase in [
            "[shape](references/shape.md)",
            "[plan](references/plan.md)",
            "tasks.py",
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write --task TASK-ID --owner OWNER",
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
        match = re.search(r"allocate the next unused label:\s*`([^`]+)`", policy, re.I | re.S)
        self.assertIsNotNone(match)
        labels = tuple(label.strip() for label in match.group(1).split(","))
        expected = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega")
        self.assertEqual(labels, expected)
        self.assertEqual(len(labels), len(set(labels)))
        self.assertIn("keep the exact name with the reusable child", policy.lower())
        self.assertIn("recycle an unused role-label combination from an unreachable child", policy.lower())

    def test_handoffs_require_facts_without_fixed_labels(self) -> None:
        policy = _read(SUBAGENTS)
        child = _read(CHILD)
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
        for term in (
            "give the child one atomic task or bounded inquiry",
            "writable paths",
            "stable reads",
            "acceptance",
            "planned proof",
            "stop conditions",
            "concise natural prose",
            "relevant refreshed evidence",
        ):
            self.assertIn(term.casefold(), policy.casefold())
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
            self.assertIn("replace slots with project facts and omit slot labels", document.casefold())
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
        self.assertIn("replace slots with project facts and omit slot labels", operations)
        self.assertIn("short natural progress updates", child)
        self.assertNotIn("Architecture alignment:", policy)
        self.assertNotIn("Return labels remain explicit", policy)
        self.assertNotIn("labeled report", policy)

    def test_child_communication_is_event_driven_without_policy_drift(self) -> None:
        policy = _normalized(_read(SUBAGENTS))
        child = _normalized(_read(CHILD))
        evaluations = _normalized(_read(TRIGGER_EVALS))
        self.assertIn("routine progress stays in the child thread", policy)
        self.assertIn("completion is one final return", policy)
        self.assertIn("ordinary progress stays local", child)
        self.assertIn("routine progress stays in the child thread", evaluations)
        for document in (child, evaluations):
            self.assertIn("explicit parent message", document)
            self.assertIn("immediate", document)
            self.assertIn("blocker", document)
            self.assertIn("collision", document)
            self.assertIn("scope change", document)
            self.assertIn("proof mismatch", document)
            self.assertIn("decision", document)
            self.assertIn("one final return", document)
        self.assertIn("architect does not echo unchanged child facts", evaluations)
        self.assertNotIn("after about two minutes of otherwise silent work", evaluations)


if __name__ == "__main__":
    unittest.main()
