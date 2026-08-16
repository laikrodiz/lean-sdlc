# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work.

## Repository gate

Read `docs/PROJECT.md` and work with `tasks.py open`. Use `tasks.py show TASK-ID` for one task. Do not load full `Done` history. Keep root `tasks.csv` authoritative; change it only through `tasks.py`. Read `references/repository-contracts.md` only for initialization, legacy migration, or document ownership.

Discussion and proposal requests remain read-only. Require explicit implementation authority before Shape and Plan. If ambiguous, remain read-only. Shape owns `why -> what -> how -> proof`; assumptions affecting behavior, scope, or architecture require confirmation. Show a visible plan before task creation. Each durable plan item maps to one task.

## Task gate

Before any other repository mutation, use `tasks.py start` to create immediate work or claim planned work. Require an owned `In Progress` task, observable acceptance, explicit proof, and a matching visible plan. Run `lean_check.py --before-write` before the first non-control write. Dependencies must be `Done` before start. Only the owner closes; a direct user request may override closure with a recorded reason.

During Plan, Quick Fix is inline, not a mode, lane, task type, or prompt. Use it only for an exact reversible outcome, no unresolved product, design, architecture, interface, schema, migration, dependency, security, generated-file, or external-state choice, and one immediate narrow proof. Use Standard when uncertain. Record Context `Quick Fix`; all write gates apply. Architect executes directly, reviews the diff, and runs narrow proof; closure defers broad review.

## Plan view and lifecycle

After task creation or start, split, merge, or material plan change, project unresolved IDs and titles into `update_plan` as exact `TASK-NNN — Title` rows. Before or with `tasks.py close`, mark closing row completed. Startup, resume, clear, or compaction: rebuild only unresolved rows from `tasks.py open`; do not load `Done` history. Brainstorming remains read-only and creates no task view. Ledger authoritative.

Assisted mode and Standard children are defaults. Lifecycle restoration restores owner, mode, and tier. Run `scripts/session_state.py --owner OWNER --mode assisted|solo`, `--fast-children`, or `--no-fast-children` for changes. Read `references/subagents.md` before delegation. The Architect owns architecture, interfaces, tasks, acceptance, integration, and closeout. The plugin hook supplies a stable 8-digit task owner.
