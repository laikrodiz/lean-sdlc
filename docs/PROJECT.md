# Project

## Problem and outcome

Codex repository work can drift from user intent, lose ownership, or claim completion without useful proof. Lean-SDLC is one shareable plugin that routes work through the smallest relevant lane, keeps a readable task ledger, uses bounded child roles, and closes work with evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- Minimal initialization, legacy migration, atomic private task-ledger transactions, and bounded read-only task views.
- Human-readable `Context` values and one durable task per independently accepted state.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Checkpoint reporting stays readable while exact machine proof remains available for verification.
- Substantial external-tool work keeps decisions with the Architect. Scout handles bounded discovery, Engineer approved mutations, Maintainer repeated operations, and Verifier independent checks. One agent owns each mutable external target.
- Architect ownership of intent, architecture, interfaces, invariants, acceptance, integration, proof, and closeout. The primary agent is Architect. Use Architect in visible commentary, handoffs, returns, and decision requests; the Architect speaks as I.
- Before changes, the Architect confirms why -> what -> how -> proof. Why states user or business value. What states the observable outcome and boundaries. How states the technical approach. Proof states acceptance and verification.
- Engineer, Maintainer, Verifier, and Scout roles under one canonical policy. Custom roles require direct user authority.
- Assisted mode is the default and persists until the user selects Solo. Session state stores mode and the Fast-children preference. Missing or invalid state restores Assisted with Standard children.
- One universal resource gate permits at most two active children when each has an exclusive scope, a settled contract, all dependencies are `Done`, and useful time reduction. It bounds Engineer/Engineer, Engineer/Scout, and Scout/Scout pairs. A Scout may overlap one Verifier or Maintainer only for future work with separate resources. Keep one reusable Verifier and one reusable Maintainer.
- Standard child roles use native GPT-5.6 Luna `max` routing with Terra `xhigh` fallback.
- Luna Max uses Standard service by default. Explicit Fast children use the priority tier for new or normally replaced Luna children. Keep reachable child threads after tier changes. Terra XHigh fallback and the Architect remain Standard unless separately overridden.
- Scout work is read-only and bounded to cited repo, contract, research, reproduction, impact, edge-case, or task-shape evidence. The Architect retains the decision.
- Lifecycle restoration covers startup, resume, clear, and compaction. It restores owner, mode, and child tier. The Architect reloads child policy before Deliver after restoration.
- Handoffs carry outcome, boundary, contract, proof, and stop conditions in concise natural prose. Verifier runs acceptance proof and one planned regression command; run the full suite only when the task or repository contract requires it.
- Independent Verifier proof, Maintainer evidence, applicable ASD-STE100 Issue 9 guidance, minimal modular engineering, plausible edge-case treatment, and small Mermaid diagrams.
- Engineers own code-local truth. Maintainer synchronizes affected shared narrative documentation after Engineers stop and before the final checkpoint.

## Deferred

- Hosted task services or issue-tracker replacement.
- Mandatory feature, decision, architecture, or operations documents.
- CI enforcement, dashboards, telemetry, cache accounting, and project-specific operational recipes.

## Constraints

- Use shell and Python standard library only. Keep task state human-readable and safe for concurrent Codex tasks.
- Keep discussion read-only until explicit implementation authority exists.
- Keep `tasks.csv` as the only durable task plan. Map each durable plan item to one task.
- Ledger sizing follows the Plan contract: one Engineer checkpoint per task, with attached tests and sidecars unless independently deliverable.
- Use `tasks.py open` for current work and `tasks.py show TASK-ID` for one task plus recursive dependencies instead of loading full `Done` history.
- If a dependency is not `Done`, block task start.
- Keep child authority, routing, reuse, checkpoint, and communication rules in the canonical subagent policy.
- Keep child concurrency in one shared worktree. Do not create child branches or additional worktrees.
- Record repeatable operations in `docs/OPERATIONS.md` after a guided success.

## Success

- Explicit invocation or repository rules trigger Lean-SDLC.
- A new repository needs only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- Agents use bounded `tasks.py open` and `tasks.py show TASK-ID` reads while the human-readable `tasks.csv` remains authoritative.
- During implementation, Codex's plan view mirrors each unresolved ledger task ID and title. Brainstorming creates no task view.
- Checkpoint reports stay readable while exact machine proof remains available for verification.
- Substantial external-tool work keeps decisions with the Architect, routes bounded work to the matching role, and gives each mutable external target one owner.
- Task transactions remain atomic, owner-aware, dependency-valid, and cycle-free.
- If a dependency is unfinished, task start is blocked.
- One root `tasks.csv` remains authoritative for qualified parallel groups, and the Architect alone starts, updates, and closes both tasks.
- Assisted delegation loads child policy before child use. Solo planning stays lead-only.
- Parallel work uses one independence gate and at most two active children. It permits Engineer/Engineer, Engineer/Scout, and Scout/Scout pairs under separate primary scopes, settled contracts, all dependencies `Done`, and useful time reduction. A future-work Scout may overlap one Verifier or Maintainer with separate resources. Shared files, changing interfaces, migrations, manifests, lock files, generated output, and exclusive targets remain serial. If qualification fails or scopes overlap, use serial execution.
- The Architect reviews each returned checkpoint, and Verifier checks each accepted task or qualified group before later dependent work starts.
- Stop writers before integration. Run integration, documentation synchronization, verification, operations, and closeout serially.
- Handoffs carry outcome, boundary, contract, proof, and stop conditions in concise natural prose. Custom roles require direct user authority.
- Standard child routing follows native GPT-5.6 Luna `max` with Terra `xhigh` fallback under the canonical policy. Technical prose follows applicable ASD-STE100 guidance without unsupported certification claims.

## Current promise

- Stage: Evolution
- Version: 1.14.0
- Version goal: Release deterministic ledger plan views, readable checkpoint reporting, and bounded external-tool delegation.
- Exit evidence: Tests, skill and plugin validation, local installation, accepted checkpoints, repository checks, tagged commit, and successful push.
