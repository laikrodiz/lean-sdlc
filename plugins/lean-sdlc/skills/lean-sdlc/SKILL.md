---
name: lean-sdlc
description: Run Lean-SDLC when the user explicitly invokes Lean-SDLC or `$lean-sdlc`, or when repository AGENTS.md requires Lean-SDLC. Require explicit implementation authority, the visible Plan contract, an owned task before writes, and evidence-based completion. Do not invoke implicitly for read-only work outside a Lean-SDLC repository.
---

# Lean-SDLC

Keep intent, work, implementation, and proof coherent with the smallest useful process.

## Start and route

1. Read `AGENTS.md`, `docs/PROJECT.md`, and current work with `tasks.py open`. Use `tasks.py show TASK-ID` for one task and dependencies. Follow [Plan view projection](references/plan.md).
2. Assisted mode is the default. Restore owner, mode, and tier after lifecycle events. Missing state restores Assisted with Standard children. Fast children require opt-in. Reload [subagents.md](references/subagents.md) before Deliver.
3. Require explicit implementation authority before task creation or changes. Discussion and proposals remain read-only. If ambiguous, remain read-only.
4. Apply [Shape](references/shape.md), then [Plan](references/plan.md), before task creation. Confirm `why -> what -> how -> proof`; show a concise plan; define acceptance and proof.
5. Read [repository-contracts.md](references/repository-contracts.md) only for initialization, legacy migration, or document ownership.
6. Read [subagents.md](references/subagents.md) before delegation. Solo planning does not load child policy. Assisted delegation loads it before child use.
7. During Plan, classify eligible trivial settled edits inline as Quick Fix; see [Plan](references/plan.md) for eligibility. Record Context `Quick Fix`.

| Lane | Use when |
| --- | --- |
| Shape | Problem, user, behavior, scope, stage, or promise is unclear. |
| Decide | Stable intent needs a durable technical choice or boundary. |
| Plan | Approved work needs a task, dependency, or owner. |
| Diagnose | A failure exists and its cause or boundary is uncertain. |
| Deliver | Cause, scope, acceptance, proof, and owned task are ready. |
| Verify | Completion is claimed, truth conflicts, or a task may close. |

Read only the active lane reference: [shape.md](references/shape.md), [decide.md](references/decide.md), [diagnose.md](references/diagnose.md), [deliver.md](references/deliver.md), [verify.md](references/verify.md), or [operations.md](references/operations.md).

## Hard gates

Treat ledger commands as control transactions. Confirm `why -> what -> how -> proof` before mutation. Before any other repository mutation, run `tasks.py start` or claim planned work; `tasks.py` is the only ledger mutation path. Require an owned `In Progress` task, acceptance, proof, and a visible plan. Follow [Plan view projection](references/plan.md) for `update_plan`. Run `lean_check.py --before-write` before the first non-control write. Diagnose unknown causes before fixes. Verify acceptance and docs parity. Only the owner closes; direct-user override requires a recorded reason.

One ledger task is one Engineer checkpoint. Mode: `scripts/session_state.py --owner OWNER --mode assisted|solo`. Tier: `scripts/session_state.py --owner OWNER --fast-children` or `--no-fast-children`.

## Child boundary

The canonical [subagent policy](references/subagents.md) is the sole authority for roles, triggers, spawns, handoffs, reuse, and failures. The Architect owns architecture, interfaces, tasks, integration, acceptance, and closeout. Assisted delegates; Solo keeps execution.

## Engineering and technical English

Build smallest cohesive units and readable orchestrator. Avoid project-size tiers, speculative interfaces, and pass-through modules. Classify plausible edge cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Use small Mermaid diagrams. Never use ASCII pseudographics.

Apply ASD-STE100 Issue 9: active voice, one term for one meaning, conditions before actions, and American English spelling. Avoid idioms, unnecessary synonyms, and vague pronouns. Keep procedural sentences to 20 words or fewer and descriptive sentences to 25 words or fewer. Preserve code, commands, paths, identifiers, protocol fields, quotations. Do not claim certified or full controlled-dictionary compliance.
