# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- A complete `why -> what -> how -> proof` intent gate before changes.
- Three required repository files: `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- An atomic, human-readable task ledger with one task per independently accepted repository state. Dependencies must be `Done` before a task starts.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Architect ownership of intent, architecture, interfaces, task boundaries, acceptance, integration, evidence, and closeout.
- Four standard roles: Engineer for approved implementation, Maintainer for shared documents and recorded operations, Verifier for independent checks, and Scout for bounded cited evidence. Broad evidence reads go to Scout.
- Assisted mode as the default and Solo mode as the lead-only alternative. Both modes use the same task and proof rules.
- A running child lifecycle state remains available despite wait expiry or silence. The Engineer visibly restates its understanding and completes routine targeted proof.
- One preauthorized read-only Verifier may be nested for a qualifying single task. Combined checkpoints use one Architect-started Verifier. The Architect gives one final visible alignment signoff. Verification is risk-based and not duplicated.
- Conservative parallel work for separate scopes and resources. Shared files, changing interfaces, migrations, generated output, and external targets remain serial. Child work stays in one shared worktree.
- Substantial external-tool work keeps decisions with the Architect. The matching role handles bounded discovery, approved mutation, repeated operations, or independent checking. One agent owns each mutable external target.
- Bounded read-only evidence work stays limited to its defined question, groups independent discovery, and preserves complete authoritative reads.
- Stable repeated repository mechanics can become maintained, recorded deterministic automations with an owner, state, canonical command, and bounded output.
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
- CI enforcement, dashboards, telemetry, cache accounting, and project-specific operational recipes.

## Success

- Users can invoke Lean-SDLC explicitly or through repository rules.
- A new repository can start with the three required files and a root ledger.
- The plan view mirrors each unresolved ledger task ID and title during implementation. Brainstorming creates no task view.
- Tasks remain atomic, owner-aware, dependency-valid, and cycle-free.
- The Architect retains decisions. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
- Read-only evidence work returns bounded, question-specific evidence without mutation authority and preserves authoritative reads.
- Recorded deterministic automations retain an owner, state, canonical command, and maintenance evidence that later work can reuse.
- Eligible Quick Fixes receive narrow proof immediately and broad review in a later Standard or final batch checkpoint.
- Checkpoint reports stay readable, exact machine proof remains available, and serial closeout uses repository truth.

## Current promise

- Stage: Evolution
- Version: 1.20.0
- Version goal: Reduce orchestration duplication with risk-based verification, Scout evidence routing, and a startup-only daily advisory with no automatic updates.
- Exit evidence: Tests, skill and plugin validation, local installation, accepted checkpoints, repository checks, tagged commit, and successful push.
