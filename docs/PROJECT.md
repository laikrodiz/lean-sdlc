# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- One canonical lifecycle from intent through owned work, proof, and closeout.
- Architect is a workflow role independent of the selected model. Each work item is Routine or Critical with a short reason; risk classification is separate from execution ownership.
- Helper tests check evaluation code behavior. Document tests check required contract wording.
- `tests/evaluation_runner.py` grades saved JSON answers against scenario assertions. By default, it reads `tests/evaluation_observations_fixture.json`; it does not execute an agent or verify actions.
- `tests/live_evaluation.py` optionally runs fresh Codex sessions, collects final structured JSON answers, and validates their structure. Its output needs separate grading by `tests/evaluation_runner.py`. It does not grade decision correctness or verify tool actions, file edits, or real workflow reliability.
- One portable release gate for local and CI checks.
- One consistent task, direct-path, and proof contract.
- Visible ambiguous repository discovery and durability warnings.
- One Git-free, task-scoped checkpoint helper.
- A complete `why -> what -> how -> proof` intent gate before changes.
- Three required repository files: `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- An atomic, human-readable task ledger with one task per independently accepted repository state. Dependencies must be `Done` before a task starts.
- Task planning preserves complete outcomes with cohesive tests and documentation. It splits only at independent acceptance boundaries, not arbitrary file, function, or line boundaries. Foundations are accepted before dependent work, and combined integration has an assigned check.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Architect ownership of intent, architecture, interfaces, task boundaries, acceptance, integration, evidence, and closeout.
- A visible pre-handoff design brief with bounded child decisions and no exposed chain-of-thought.
- Clear contracts communicate outcome, interfaces, invariants, failure behavior, mandatory decisions versus suggestions, freedom, proof, and stop conditions.
- Four standard roles with stage-aware routing: Engineer for approved implementation, Maintainer for shared documents and recorded operations, Verifier for independent checks, and Scout for map-before-read bounded cited evidence.
- One role-routing precedence chain, layered targeted, acceptance, and regression proof, and bounded full-suite use. One command may satisfy several proof purposes. Reuse proof and artifacts only when relevant source, dependencies, configuration, environment, toolchain, and target inputs match.
- Assisted mode is the default. The Architect normally handles eligible Routine Quick Fixes. Luna Max handles routine non-Quick-Fix work and may handle Critical work under precise design. A rare bounded Critical implementation may remain with the Architect when design/implementation coupling makes delegation risk substantial misunderstanding or repeated redesign; independent review remains mandatory. Solo mode remains lead-only, and Critical work cannot self-certify without independent evidence.
- Delegation preserves the selected model and effort. Neither mode silently lowers them.
- Engineers own complete atomic outcomes, including permitted corrections, tests, and mechanical consistency.
- A running child lifecycle state remains available despite wait expiry or silence. The Engineer visibly restates its understanding and completes routine targeted proof.
- Routine child progress, including the start restatement, stays in the child thread. Explicit parent messages are only for events that require immediate Architect action. Completion produces one final return. The Architect does not repeat unchanged child facts.
- Small settled tasks keep routine progress in child threads. Larger or uncertain work uses specific decision or risk checkpoints. Material blockers and conflicts escalate.
- One preauthorized read-only Verifier may be nested for a qualifying single task. Combined checkpoints use one Architect-started Verifier. The Architect gives one final visible alignment signoff. Verification is risk-based and not duplicated.
- Useful concurrency is constrained by native runtime capacity and independent mutable ownership, not a fixed workflow-agent or Engineer-count limit. Shared resources remain serial. Child work stays in one shared worktree without new worktrees.
- Substantial external-tool work keeps decisions with the Architect. Delegate when expected benefit exceeds handoff and verification costs; external-tool call count and discovery are cues only. Preserve permissions and one mutable-target owner.
- The Architect reviews actual changes and evidence, chooses Accept, Revise, or Redesign, returns actionable findings together, and does not repair delegated routine work.
- Revise keeps the same team when the contract remains settled. Redesign corrects the contract before work resumes.
- Bounded read-only evidence work stays limited to its defined question, groups independent discovery, and preserves complete authoritative reads.
- Repeated repository mechanics can yield transient automation candidates without adding new durable state. Retain a maintained deterministic command only when later reuse justifies it.
- Readable checkpoint reports retain exact machine proof. Stable independent boundaries may verify and draft separate documentation concurrently. Shared documentation and common regression checks batch across atomic tasks while each task keeps its own acceptance set. Final release stops relevant writers before release checks.
- Inline Quick Fix classification during Plan for trivial settled edits, with immediate narrow proof and deferred shared review.
- `docs/PROJECT.md` is the only mandatory shared project document.
- Optional document families use concrete triggers and semantic sizing.
- Each numbered family gets a small `INDEX.md` with its first document.
- The Maintainer owns shared narrative truth and indexes.
- The Architect approves document meaning and splits.
- Root `archive/` requires an explicit user request and remains inert.

## Constraints

- Keep durable planning in root `tasks.csv`. Use bundled task commands for ledger changes.
- Keep discussion read-only until the user gives implementation authority.
- Keep shared truth in its owning document. Keep code-local truth with the Engineer.
- Use shell and Python standard library only. Keep repository state readable and recoverable.
- Preserve task ownership, dependency order, acceptance, and proof across resume and compaction.

## Deferred

- Hosted task services or issue-tracker replacement.
- Mandatory feature, decision, architecture, state-machine, interface, data, operations, security, glossary, or verification documents.
- A repository-wide documentation archive policy.
- Dashboards, telemetry, cache accounting, and project-specific operational recipes.

## Success

- Users can invoke Lean-SDLC explicitly or through repository rules.
- A new repository can start with the three required files and a root ledger.
- The plan view mirrors each unresolved ledger task ID and title during implementation. Brainstorming creates no task view.
- Tasks remain atomic, owner-aware, permission-preserving, dependency-valid, and cycle-free.
- Broad work is split only when each result remains a complete, independently acceptable outcome. Useful concurrency also needs separate mutable ownership, native capacity, and benefit beyond handoff and verification costs.
- The Architect retains decisions. Delegated work preserves ownership and permission boundaries. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
- Routine and Critical work use risk-aware execution ownership. Critical work has independent evidence and cannot self-certify.
- Routine progress stays in child threads. Action-required events reach the Architect immediately. Completion produces one final return without duplicate Architect commentary.
- Read-only evidence work maps the evidence space before bounded, question-specific reads. It returns evidence without mutation authority and preserves authoritative reads.
- Transient automation candidates add no new durable state. A maintained deterministic command needs a later reuse case and maintenance evidence.
- Release checks use one portable gate in local and CI contexts.
- Evaluation evidence separates helper code-behavior tests from document contract-wording tests.
- Saved-fixture checks grade repository-owned JSON answers with deterministic assertions.
- Optional live collection starts fresh sessions, collects final structured JSON answers, and validates their structure. A separate runner grades those answers.
- Evaluation evidence does not measure real workflow execution reliability.
- Task, direct-path, and proof inputs follow one consistent contract.
- Ambiguous repository discovery is visible, and durability warnings identify risks before they persist.
- Task-scoped checkpoints can run without Git access.
- Eligible Quick Fixes receive narrow proof immediately and broad review in a later Standard or final batch checkpoint.
- Checkpoint reports stay readable, exact machine proof remains available, and serial closeout uses repository truth.

## Current promise

- Stage: Evolution
- Version: 1.26.0
- Version goal: Adopt risk-based Architect delegation and complete outcomes. Classify every work item as Routine or Critical with a short reason, keep risk separate from execution ownership, route delegation when expected benefit exceeds handoff and verification costs, and preserve independent evidence for Critical work. Treat external-tool call count and discovery as cues only. Label helper and document tests, saved-fixture grading, and live final-answer collection separately. Preserve permission, ownership, atomic acceptance, ledger, and bytecode boundaries.
- Exit evidence: Helper code-behavior tests, document contract-wording tests, saved-fixture assertion checks, optional live final-answer collection and structure checks, separate grading of supplied live output, skill and plugin validation, local installation, portable release-gate checks, accepted checkpoints, repository checks, tagged commit, and successful push. Evaluation checks do not measure real workflow execution reliability.
