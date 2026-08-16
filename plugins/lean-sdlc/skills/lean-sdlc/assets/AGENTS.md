# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work.

## Repository gate

Read `docs/PROJECT.md` and current work with `tasks.py open`. Use `tasks.py show TASK-ID` for one task plus recursive dependencies. Do not load full `Done` history. Keep root `tasks.csv` authoritative and change it only through `tasks.py`. Read `references/repository-contracts.md` only for initialization, legacy migration, or document ownership.

Discussion and proposal requests remain read-only. Require explicit implementation authority before Shape and Plan. If authority is ambiguous, remain read-only. Shape owns `why -> what -> how -> proof`; material assumptions affecting behavior, scope, or architecture require user confirmation. Before task creation, show a concise visible plan. Each durable plan item maps to one task.

## Task gate

Before any other repository mutation, use the installed `tasks.py start` command to create immediate work or claim planned work. Require an owned `In Progress` task, observable acceptance, explicit proof, and a matching visible plan. Run `lean_check.py --before-write` before the first non-control write. Dependencies must be `Done` before start. Only the owner closes a task; a direct user request may override closure with a recorded reason.

Each task is one independently accepted Engineer checkpoint and remains resumable from repository truth and its ledger row after compaction. Split independently accepted and independently proved work. The plugin hook supplies a stable 8-digit task owner.

## Plan view and lifecycle

After task creation or start, split, merge, or material plan change, project unresolved rows into `update_plan` as exact `TASK-NNN — Title` rows with matching statuses. Before or with `tasks.py close`, mark a closing row completed. After startup, resume, clear, or compaction, rebuild only unresolved rows from `tasks.py open`; do not load `Done` history. Brainstorming remains read-only and creates no task view. The human-readable ledger remains authoritative.

Assisted mode and Standard children are defaults. Lifecycle restoration restores owner, mode, and child tier. Run `scripts/session_state.py --owner OWNER --mode assisted|solo`, `--fast-children`, or `--no-fast-children` for changes. Read `references/subagents.md` before delegation. The Architect owns architecture, interfaces, task state, acceptance, integration, and closeout.
