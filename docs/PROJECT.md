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
- Four standard roles: Engineer for approved implementation, Maintainer for shared documents and recorded operations, Verifier for independent checks, and Scout for bounded cited evidence.
- Assisted mode as the default and Solo mode as the lead-only alternative. Both modes use the same task and proof rules.
- Conservative parallel work for separate scopes and resources. Shared files, changing interfaces, migrations, generated output, and external targets remain serial. Child work stays in one shared worktree.
- Substantial external-tool work keeps decisions with the Architect. The matching role handles bounded discovery, approved mutation, repeated operations, or independent checking. One agent owns each mutable external target.
- Readable checkpoint reports with exact machine proof retained for verification. Integration, documentation synchronization, verification, operations, and closeout run serially.

## Constraints

- Keep durable planning in root `tasks.csv`. Use bundled task commands for ledger changes.
- Keep discussion read-only until the user gives implementation authority.
- Keep shared truth in its owning document. Keep code-local truth with the Engineer.
- Use shell and Python standard library only. Keep repository state readable and recoverable.
- Preserve task ownership, dependency order, acceptance, and proof across resume and compaction.

## Deferred

- Hosted task services or issue-tracker replacement.
- Mandatory feature, decision, architecture, or operations documents.
- CI enforcement, dashboards, telemetry, cache accounting, and project-specific operational recipes.

## Success

- Users can invoke Lean-SDLC explicitly or through repository rules.
- A new repository can start with the three required files and a root ledger.
- The plan view mirrors each unresolved ledger task ID and title during implementation. Brainstorming creates no task view.
- Tasks remain atomic, owner-aware, dependency-valid, and cycle-free.
- The Architect retains decisions. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
- Checkpoint reports stay readable, exact machine proof remains available, and serial closeout uses repository truth.

## Current promise

- Stage: Evolution
- Version: 1.15.0
- Version goal: Release the compact runtime contract, abstract output fact patterns, and human product narrative.
- Exit evidence: Tests, skill and plugin validation, local installation, accepted checkpoints, repository checks, tagged commit, and successful push.
