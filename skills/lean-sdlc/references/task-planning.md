# Task Planning Workflow

Use when approved feature or decision truth is ready to become executable work.

Use Sol at `medium`; raise to `high` for cross-cutting dependencies. Luna may write an already-agreed CSV mechanically.

## Workflow

1. Create or select a task before every repository file mutation, including documentation, configuration, tests, generated files, and maintenance.
2. Use a feature parent for behavior, a decision parent for durable technical choices, `REPO` for non-behavior maintenance, and `BOOTSTRAP` only for initialization. A task creating a feature or decision may reserve its future `FEAT-*` or `DEC-*` id, which must exist before closeout.
3. Keep one intentional change and one owning thread per task. Use the stable numeric `Owner` supplied by the Lean-SDLC lifecycle hook; subagents share the parent thread owner.
4. Record concise observable acceptance and a proof command or method before work. Evidence is added only at closeout.
5. Add dependencies only when sequencing truly matters.
6. Put requirements and design detail in their authoritative docs rather than the task ledger.
7. Use `scripts/tasks.py create` for new work and `scripts/tasks.py claim` to move Planned work to `In Progress`. The command locks the ledger, reads the latest state, applies one targeted change, and replaces the CSV atomically.
8. Use `scripts/tasks.py update` for corrections. Never edit `planning/tasks.csv` directly.
9. State task creation and status transitions explicitly.
10. Stop if a task would hide new scope, an architecture choice, or several independent outcomes.

After planning, use execution routing when several ready tasks or delegation choices exist. For one obvious critical-path task, proceed to implementation.

Success means the task ledger is a small execution index rather than a duplicate requirements system.
