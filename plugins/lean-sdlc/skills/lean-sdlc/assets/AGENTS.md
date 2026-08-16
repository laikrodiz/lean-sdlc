# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work. Read-only inspection may use the direct path.

Read `docs/PROJECT.md` and relevant feature, decision, or operations documents. Use `tasks.py open` for current work and `tasks.py show TASK-ID` for one task plus recursive dependencies instead of loading full Done history. The human-readable `tasks.csv` remains authoritative. Read affected code and tests after the task boundary is clear. Use `references/repository-contracts.md` only for initialization, legacy migration, or document ownership. Resolve contradictions before closeout.

## Task gate

- Task commands are control transactions. Never edit `tasks.csv` directly.
- Discussion and proposal requests remain read-only. Explicit implementation authority permits Plan and Deliver. If authority is ambiguous, remain read-only.
- Shape owns the complete natural intent gate: why -> what -> how -> proof. Material assumptions that affect behavior, scope, or architecture require user confirmation.
- Brainstorming and rephrasing remain read-only.
- Before any other repository mutation, use the installed `tasks.py start` command to create immediate work or claim planned work.
- Before task creation or implementation, apply the canonical Plan contract. Show natural intent confirmation and a concise visible plan with observable completion conditions and proof.
- Keep `tasks.csv` as the only durable task plan. Map each durable plan item to one task. Keep implementation steps transient.
- Use `Planned`, `In Progress`, and `Done`. Planned work is unowned. In Progress and Done retain the stable 8-digit task owner supplied by the plugin hook.
- Only the owner closes a task. A direct user request may override closure with a recorded reason.
- Use `Project`, `FEAT-*`, `DEC-*`, or `Bootstrap` in `Context`.
- Each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.
- Split independently accepted and independently proved work. Keep inseparable coding steps transient.
- Size ledger work as one Engineer checkpoint under the Plan contract; keep tests and attached Maintainer or Verifier work with it unless independently deliverable.
- Assisted mode and Standard children are the defaults. Persist mode and the Fast-children preference until the user changes them.
- Lifecycle restoration covers startup, resume, clear, and compaction. It restores owner, mode, and child tier; reload `references/subagents.md` before Deliver.
- Dependencies must be `Done` before a task starts. The ledger lock is not a source lock.
- Assisted parallel work permits at most two children only after the resource gate passes. One Architect writer group owns the worktree.
- During implementation, after task creation or start, split, merge, or material plan change, project unresolved `tasks.csv` rows into `update_plan` with exact `TASK-NNN — Title` rows and matching `Planned`/`In Progress` states.
- Before or with ledger close, mark the row completed. After startup, resume, clear, or compaction, rebuild only unresolved rows from `tasks.py open`; do not load Done history.
- Brainstorming remains read-only and creates no task view. A qualified pair uses one combined active row while `tasks.csv` remains authoritative.

## Child gate

Read `references/subagents.md` before Deliver or the first delegated read-only operation. Solo planning does not load child policy. Assisted delegation loads it before child use.

The Architect owns architecture, interfaces, task state, acceptance, integration, and closeout. The Architect assigns each child a valid lowercase role prefix and one Greek suffix, such as `task_name=engineer_beta`. Read the canonical child policy for bounded delegation, handoff facts, checkpoints, and sidecar limits.
