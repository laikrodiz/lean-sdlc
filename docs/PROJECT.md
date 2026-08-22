# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- One canonical lifecycle from intent through owned work, proof, and closeout.
- Executable assertions over recorded behavioral observations, with optional live fresh sessions.
- One portable release gate for local and CI checks.
- One consistent task, direct-path, and proof contract.
- Visible ambiguous repository discovery and durability warnings.
- One Git-free, task-scoped checkpoint helper.
- A complete `why -> what -> how -> proof` intent gate before changes.
- Three required repository files: `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- An atomic, human-readable task ledger with one task per independently accepted repository state. Dependencies must be `Done` before a task starts.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Architect ownership of intent, architecture, interfaces, task boundaries, acceptance, integration, evidence, and closeout.
- A visible pre-handoff design brief with bounded child decisions and no exposed chain-of-thought.
- Four standard roles with stage-aware routing: Engineer for approved implementation, Maintainer for shared documents and recorded operations, Verifier for independent checks, and Scout for map-before-read bounded cited evidence.
- One role-routing precedence chain, layered targeted, acceptance, and regression proof, and bounded full-suite use.
- Assisted mode as the default and Solo mode as the lead-only alternative. Both modes use the same task and proof rules.
- A running child lifecycle state remains available despite wait expiry or silence. The Engineer visibly restates its understanding and completes routine targeted proof.
- One preauthorized read-only Verifier may be nested for a qualifying single task. Combined checkpoints use one Architect-started Verifier. The Architect gives one final visible alignment signoff. Verification is risk-based and not duplicated.
- Conservative parallel work for separate scopes and resources. Shared files, changing interfaces, migrations, generated output, and external targets remain serial. Child work stays in one shared worktree.
- Substantial external-tool work keeps decisions with the Architect. The matching role handles bounded discovery, approved mutation, repeated operations, or independent checking. One agent owns each mutable external target.
- Bounded read-only evidence work stays limited to its defined question, groups independent discovery, and preserves complete authoritative reads.
- Repeated repository mechanics can yield transient automation candidates without adding new durable state. Retain a maintained deterministic command only when later reuse justifies it.
- Readable checkpoint reports with exact machine proof retained for verification. Integration, documentation synchronization, verification, operations, and closeout run serially.
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
- Tasks remain atomic, owner-aware, dependency-valid, and cycle-free.
- The Architect retains decisions. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
- Read-only evidence work maps the evidence space before bounded, question-specific reads. It returns evidence without mutation authority and preserves authoritative reads.
- Transient automation candidates add no new durable state. A maintained deterministic command needs a later reuse case and maintenance evidence.
- Release checks use one portable gate in local and CI contexts.
- Recorded observations use deterministic assertions; optional live sessions collect new observations.
- Task, direct-path, and proof inputs follow one consistent contract.
- Ambiguous repository discovery is visible, and durability warnings identify risks before they persist.
- Task-scoped checkpoints can run without Git access.
- Eligible Quick Fixes receive narrow proof immediately and broad review in a later Standard or final batch checkpoint.
- Checkpoint reports stay readable, exact machine proof remains available, and serial closeout uses repository truth.

## Current promise

- Stage: Evolution
- Version: 1.23.0
- Version goal: Executable behavioral evaluation, optional live fresh sessions, one portable release gate, one task/direct-path/proof contract, visible discovery and durability warnings, and a Git-free task-scoped checkpoint helper.
- Exit evidence: Tests, behavioral evaluation, skill and plugin validation, local installation, portable release-gate checks, accepted checkpoints, repository checks, tagged commit, and successful push.
