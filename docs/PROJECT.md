# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- One canonical lifecycle from intent through owned work, proof, and closeout.
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
- Task planning first preserves independent acceptance boundaries, then classifies broad work as together, serial, or parallel. Runtime revalidates safety before parallel Engineer spawn.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Architect ownership of intent, architecture, interfaces, task boundaries, acceptance, integration, evidence, and closeout.
- A visible pre-handoff design brief with bounded child decisions and no exposed chain-of-thought.
- Four standard roles with stage-aware routing: Engineer for approved implementation, Maintainer for shared documents and recorded operations, Verifier for independent checks, and Scout for map-before-read bounded cited evidence.
- One role-routing precedence chain, layered targeted, acceptance, and regression proof, and bounded full-suite use. One command may satisfy several proof purposes. Reuse proof and artifacts only when relevant source, dependencies, configuration, environment, toolchain, and target inputs match.
- Assisted mode as the default and Solo mode as the lead-only alternative. Both modes use the same task and proof rules.
- Assisted mode may keep one bounded, settled local change with the Architect when handoff overhead exceeds the work. This includes judgment-intensive implementation when delegation would duplicate design effort or require extensive explanation or correction. Substantial separable execution and exploration stay with Luna Max. This does not change the selected Architect model or effort.
- Engineers own complete atomic outcomes, including permitted corrections, tests, and mechanical consistency.
- A running child lifecycle state remains available despite wait expiry or silence. The Engineer visibly restates its understanding and completes routine targeted proof.
- Routine child progress, including the start restatement, stays in the child thread. Explicit parent messages are only for events that require immediate Architect action. Completion produces one final return. The Architect does not repeat unchanged child facts.
- One preauthorized read-only Verifier may be nested for a qualifying single task. Combined checkpoints use one Architect-started Verifier. The Architect gives one final visible alignment signoff. Verification is risk-based and not duplicated.
- Resource-safe parallel work uses separate scopes and resources. At most two concurrent Engineers may run, with one optional third read-only child when native capacity gives meaningful elapsed-time savings. All descendants count. Child work stays in one shared worktree without new worktrees.
- Substantial external-tool work keeps decisions with the Architect. The matching role handles bounded discovery, approved mutation, repeated operations, or independent checking. One agent owns each mutable external target.
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
- Broad work is split only when each result remains independently acceptable; parallel execution also needs a favorable runtime risk-benefit check.
- The Architect retains decisions. Delegated work preserves ownership and permission boundaries. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
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
- Version: 1.25.1
- Version goal: Streamline approved work and release proof. Route delegation when its expected benefit exceeds handoff and verification cost; treat external-tool call count and discovery as cues only. Label helper and document tests, saved-fixture grading, and live final-answer collection separately. Preserve permission, ownership, atomic acceptance, ledger, and bytecode boundaries.
- Exit evidence: Helper code-behavior tests, document contract-wording tests, saved-fixture assertion checks, optional live final-answer collection and structure checks, separate grading of supplied live output, skill and plugin validation, local installation, portable release-gate checks, accepted checkpoints, repository checks, tagged commit, and successful push. Evaluation checks do not measure real workflow execution reliability.
