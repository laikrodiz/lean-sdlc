---
name: lean-sdlc
description: Run Lean-SDLC when the user explicitly invokes Lean-SDLC or `$lean-sdlc`, or when repository AGENTS.md requires Lean-SDLC. Require explicit implementation authority, the visible Plan contract, an owned task before writes, and evidence-based completion. Do not invoke implicitly for read-only work outside a Lean-SDLC repository.
---

# Lean-SDLC

Keep intent, work, implementation, and proof coherent with the smallest useful process.

## Start and route

1. Read `AGENTS.md` and `docs/PROJECT.md`. Use `tasks.py open` for current work and `tasks.py show TASK-ID` for one task plus recursive dependencies instead of loading full Done history. The human-readable `tasks.csv` remains authoritative. Identify outcome, repository truth, active task, and mode.
2. Assisted mode is the default and persists until the user selects Solo. Missing or invalid state restores Assisted with Standard children. Fast children require explicit user opt-in; normal Luna spawns omit `service_tier`. Lifecycle restoration restores owner, mode, and child tier after startup, resume, clear, or compaction; reload `references/subagents.md` before Deliver.
3. Before task creation or file changes, require explicit implementation authority. Discussion and proposal requests remain read-only. If authority is ambiguous, remain read-only.
4. Apply the complete [Shape intent gate](references/shape.md), then [Plan](references/plan.md): confirm intent with natural prose, show a concise visible plan, and define observable completion conditions and proof. A one-item plan is valid.
5. Read [repository-contracts.md](references/repository-contracts.md) only for initialization, legacy migration, or document ownership. For an older ledger, run [scripts/tasks.py](scripts/tasks.py) `upgrade`.
6. Read [subagents.md](references/subagents.md) only before actual delegation. Solo planning does not load child policy. Assisted delegation loads it before child use.

Use the earliest unresolved lane, then continue when later gates are ready.

| Lane | Use when |
| --- | --- |
| Shape | Problem, user, behavior, scope, stage, or promise is unclear. |
| Decide | Stable intent needs a durable technical choice or boundary. |
| Plan | Approved work needs a task, dependency, or owner. |
| Diagnose | A failure exists and its cause or boundary is uncertain. |
| Deliver | Cause, scope, acceptance, proof, and owned task are ready. |
| Verify | Completion is claimed, truth conflicts, or a task may close. |

Read the lane reference only when active: [shape.md](references/shape.md), [decide.md](references/decide.md), [diagnose.md](references/diagnose.md), [deliver.md](references/deliver.md), [verify.md](references/verify.md), or [operations.md](references/operations.md). Read [model-routing.md](references/model-routing.md) for substantial decisions.

## Hard gates

Treat task-ledger commands as control transactions. Before any task or repository mutation, the Architect confirms the natural `why -> what -> how -> proof` contract from Shape. Before any other repository mutation, run `tasks.py start` or claim planned work with `tasks.py start TASK-ID`; never edit `tasks.csv` directly. Read-only `tasks.py open` and `tasks.py show TASK-ID` views keep current work bounded while the human-readable CSV remains authoritative. Require an owned `In Progress` task, measurable acceptance, explicit proof, and a matching visible plan. Run `lean_check.py --before-write --task TASK-ID --owner OWNER` before the first non-control write. Diagnose an unknown cause before a fix. Keep one intentional change and one durable task normally; a qualified parallel group may hold two independently accepted tasks under one Architect owner. Each task is one independently accepted repository state; local implementation steps stay transient. Verify acceptance and documentation parity before closure. Only the owner closes a task; a direct user request may override with a recorded reason.

Size each ledger task as one Engineer checkpoint under the [Plan contract](references/plan.md); keep tests and attached sidecars with it unless independently deliverable.

When mode changes, the Architect runs `scripts/session_state.py --owner OWNER --mode assisted|solo` with the selected mode. When the child tier changes, the Architect runs `scripts/session_state.py --owner OWNER --fast-children` or `--no-fast-children`.

## Child boundary

The canonical [subagent policy](references/subagents.md) is the sole authority for child roles, triggers, profiles, spawn payloads, handoffs, reuse, visible communication, and failure conditions. The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, task boundaries, integration, acceptance, and closeout.

Children call the primary agent Architect; the Architect speaks as I. Assisted and Solo are the only orchestration modes. Assisted normally uses one Engineer; a qualified parallel group may use two under the canonical child policy. Keep one reusable child thread per sidecar role and normally one Engineer. The Architect assigns each child a valid lowercase role prefix and one Greek suffix at spawn, such as `task_name=engineer_beta` for Engineer beta.

## Engineering and technical English

Build the smallest cohesive units with narrow contracts and a readable orchestrator. Avoid project-size tiers, speculative interfaces, and pass-through modules. Classify plausible edge cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior. Use small Mermaid diagrams when they materially clarify flow, state, ownership, sequence, or dependencies. Never use ASCII pseudographics.

Apply applicable ASD-STE100 Issue 9 guidance. Use active voice, one term for one meaning, condition-first instructions, and American English spelling. State conditions before actions. Avoid idioms, unnecessary synonyms, and vague pronouns. Keep procedural sentences to 20 words or fewer and descriptive sentences to 25 words or fewer. Preserve code, commands, paths, identifiers, protocol fields, quotations, and required terms. Do not claim certified or full controlled-dictionary compliance without an ASD-STE100 checker.
