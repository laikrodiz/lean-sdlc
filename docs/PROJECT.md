# Project

## Problem and outcome

Codex repository work can drift from user intent, lose ownership, or claim completion without useful proof. Lean-SDLC is one shareable plugin that routes work through the smallest relevant lane, keeps a readable task ledger, uses bounded child roles, and closes work with evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- Minimal initialization, legacy migration, atomic private task-ledger transactions, and bounded read-only task views.
- Human-readable `Context` values and one durable task per independently accepted state.
- Architect ownership of intent, architecture, interfaces, invariants, acceptance, integration, proof, and closeout. The primary agent is Architect. Use Architect in visible commentary, handoffs, returns, and decision requests; the Architect speaks as I.
- Engineer, Maintainer, Verifier, and Scout roles under one canonical policy. Custom roles require direct user authority.
- One universal independence gate permits at most two active children with separate scopes, settled contracts, no dependency, and useful time reduction. It bounds Engineer/Engineer, Engineer/Scout, and Scout/Scout pairs. A Scout may overlap one Verifier or Maintainer only for future work with separate resources. Keep one reusable Verifier and one reusable Maintainer.
- Named `lean_sdlc_luna` profile for Luna Max children with Terra XHigh fallback.
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
- Use `tasks.py open` for current work and `tasks.py show TASK-ID` for one task plus recursive dependencies instead of loading full `Done` history.
- Keep child authority, routing, reuse, checkpoint, and communication rules in the canonical subagent policy.
- Record repeatable operations in `docs/OPERATIONS.md` after a guided success.

## Success

- Explicit invocation or repository rules trigger Lean-SDLC.
- A new repository needs only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- Agents use bounded `tasks.py open` and `tasks.py show TASK-ID` reads while the human-readable `tasks.csv` remains authoritative.
- Task transactions remain atomic, owner-aware, dependency-valid, and cycle-free.
- One root `tasks.csv` remains authoritative for qualified parallel groups, and the Architect alone starts, updates, and closes both tasks.
- Assisted delegation loads child policy before child use. Solo planning stays lead-only.
- Parallel work uses one independence gate and at most two active children. It permits Engineer/Engineer, Engineer/Scout, and Scout/Scout pairs under separate primary scopes, settled contracts, no dependency, and useful time reduction. A future-work Scout may overlap one Verifier or Maintainer with separate resources. Shared files, changing interfaces, migrations, manifests, lock files, generated output, and exclusive targets remain serial. If qualification fails or scopes overlap, use serial execution.
- The Architect reviews each returned checkpoint, and Verifier checks each accepted task or qualified group before later dependent work starts.
- Handoffs carry outcome, boundary, contract, proof, and stop conditions in concise natural prose. Custom roles require direct user authority.
- Luna children use the named profile and priority tier. Terra XHigh is the only fallback. Technical prose follows applicable ASD-STE100 guidance without unsupported certification claims.

## Current promise

- Stage: Evolution
- Version: 1.11.0
- Version goal: Release bounded task-ledger reads and simplified child orchestration with shared-document stewardship and combined checkpoint proof.
- Exit evidence: Tests, skill and plugin validation, local installation, accepted checkpoints, repository checks, tagged commit, and successful push.
