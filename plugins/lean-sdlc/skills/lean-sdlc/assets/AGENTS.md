# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work. Read-only inspection may use the direct path.

Read `docs/PROJECT.md`, relevant feature, decision, or operations documents, `tasks.csv`, then affected code and tests. Use `references/repository-contracts.md` only for initialization, legacy migration, or document ownership. Resolve contradictions before closeout.

## Task gate

- Task commands are control transactions. Never edit `tasks.csv` directly.
- Discussion and proposal requests remain read-only. Explicit implementation authority permits Plan and Deliver. If authority is ambiguous, remain read-only.
- Before any other repository mutation, use the installed `tasks.py start` command to create immediate work or claim planned work.
- Before task creation or implementation, apply the canonical Plan contract. Show natural intent confirmation and a concise visible plan with observable completion conditions and proof.
- Keep `tasks.csv` as the only durable task plan. Map each durable plan item to one task. Keep implementation steps transient.
- Use `Planned`, `In Progress`, and `Done`. Planned work is unowned. In Progress and Done retain the stable 8-digit task owner supplied by the plugin hook.
- Only the owner closes a task. A direct user request may override closure with a recorded reason.
- Use `Project`, `FEAT-*`, `DEC-*`, or `Bootstrap` in `Context`.
- Each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.
- Split independently accepted and independently proved work. Keep inseparable coding steps transient.

## Child gate

Read `references/subagents.md` before Deliver or the first delegated read-only operation. Solo planning does not load child policy. Assisted delegation loads it before child use.

The Architect owns architecture, interfaces, task state, acceptance, integration, and closeout. Read the canonical child policy for roles, communication, profiles, and checkpoints.
