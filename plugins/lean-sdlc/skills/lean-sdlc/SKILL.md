---
name: lean-sdlc
description: Run Lean-SDLC when the user explicitly invokes Lean-SDLC or `$lean-sdlc`, or when repository AGENTS.md requires Lean-SDLC. Require explicit implementation authority, the visible Plan contract, an owned task before writes, and evidence-based completion. Do not invoke implicitly for read-only work outside a Lean-SDLC repository.
---

# Lean-SDLC

Keep intent, work, implementation, and proof coherent with the smallest useful process.

At lifecycle startup, use the reported `Repository root` and `Skill root` exactly. The Architect invokes packaged helpers with these roots:

- `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" <command>` for ledger commands.
- `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" <options>` for repository checks.
- `python3 "<skill-root>/scripts/session_state.py" --owner OWNER <options>` for session state.

Children receive task facts, assigned paths, acceptance, proof, and both roots. Children do not locate or run ledger, checker, or session-state helpers.

## Start and route

1. Read `AGENTS.md`, `docs/PROJECT.md`, and current work with `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" open`. Use `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" show TASK-ID` for one task and dependencies. Follow [Plan view projection](references/plan.md).
2. Assisted mode is the default. Restore owner, mode, and tier after lifecycle events. Missing state restores Assisted with Standard children. Fast children require opt-in. Reload [subagents.md](references/subagents.md) before Deliver.
3. Require explicit implementation authority before task creation or changes. Discussion and proposals remain read-only. If ambiguous, remain read-only.
4. Apply [Shape](references/shape.md), then [Plan](references/plan.md), before task creation. Confirm `why -> what -> how -> proof`; show a concise plan; define acceptance and proof.
5. Read [repository-contracts.md](references/repository-contracts.md) only for initialization, legacy migration, or document ownership. It is also canonical for optional-document triggers, semantic sizing, indexes, and source-archive boundaries.
6. Read [subagents.md](references/subagents.md) before delegation. Solo planning does not load child policy. Assisted delegation loads it before child use.
7. During Plan, classify eligible trivial settled edits inline as Quick Fix; see [Plan](references/plan.md) for eligibility. Record Context `Quick Fix`.

Backlog is parked work. `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" backlog` is its compact view. Only a direct user request may add or promote Backlog work. An Architect may propose placement only for a substantial reason and must wait for approval. Backlog never authorizes planning or implementation. Before new Standard work, read the compact view and check duplicates, broader items, or related ideas. Do not load Backlog on startup, resume, brainstorming, or Quick Fix work.

| Lane | Use when |
| --- | --- |
| Shape | Problem, user, behavior, scope, stage, or promise is unclear. |
| Decide | Stable intent needs a durable technical choice or boundary. |
| Plan | Approved work needs a task, dependency, or owner. |
| Diagnose | A failure exists and its cause or boundary is uncertain. |
| Deliver | Cause, scope, acceptance, proof, and owned task are ready. |
| Verify | Completion is claimed, truth conflicts, or a task may close. |

Read only the active lane reference: [shape.md](references/shape.md), [decide.md](references/decide.md), [diagnose.md](references/diagnose.md), [deliver.md](references/deliver.md), [verify.md](references/verify.md), or [operations.md](references/operations.md).

## Canonical lifecycle

Start at the earliest unresolved lane and skip settled lanes. Use the six lanes in this order:

1. Shape confirms authority, Why, What, constraints, exclusions, and any material ambiguity.
2. Decide settles technical choices that need durable agreement.
3. Plan shows the visible plan, owned task, observable acceptance, and proof.
4. Diagnose runs only when the cause or fault boundary is unknown, then returns to Deliver.
5. Deliver claims the task, runs the before-write gate, posts the pre-handoff design brief, and routes work by stage-aware precedence.
6. Verify checks observable acceptance and affected-boundary regression risk, reconciles scope, interfaces, invariants, and documentation, and closes the task.

Read-only discussion stops before task creation. The Architect reports decisions and relevant grounds, never private chain-of-thought.

## Hard gates

Treat ledger commands as control transactions. Confirm `why -> what -> how -> proof` before mutation. Before any other repository mutation, run `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" start` or claim planned work; the packaged `tasks.py` helper is the only ledger mutation path. Require an owned `In Progress` task, acceptance, proof, and a visible plan. Follow [Plan view projection](references/plan.md) for `update_plan`. Run `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" --before-write` before the first non-control write. Diagnose unknown causes before fixes. Verify acceptance and docs parity. Only the owner closes; direct-user override requires a recorded reason.

One ledger task is one Engineer checkpoint. Mode: `python3 "<skill-root>/scripts/session_state.py" --owner OWNER --mode assisted|solo`. Tier: `python3 "<skill-root>/scripts/session_state.py" --owner OWNER --fast-children` or `--no-fast-children`.

## Child boundary

The canonical [subagent policy](references/subagents.md) is the sole authority for roles, triggers, spawns, handoffs, reuse, and failures. The Architect owns architecture, interfaces, tasks, integration, acceptance, and closeout. Assisted delegates; Solo keeps execution.

## Engineering and technical English

Build smallest cohesive units and readable orchestrator. Avoid project-size tiers, speculative interfaces, and pass-through modules. Classify plausible edge cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Use small Mermaid diagrams. Never use ASCII pseudographics.

Apply ASD-STE100 Issue 9: active voice, one term for one meaning, conditions before actions, and American English spelling. Avoid idioms, unnecessary synonyms, and vague pronouns. Keep procedural sentences to 20 words or fewer and descriptive sentences to 25 words or fewer. Preserve code, commands, paths, identifiers, protocol fields, quotations. Do not claim certified or full controlled-dictionary compliance.
