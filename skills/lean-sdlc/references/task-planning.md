# Task Planning Workflow

Use when approved feature or decision truth is ready to become executable work.

Use Sol at `medium`; raise to `high` for cross-cutting dependencies. Luna may write an already-agreed CSV mechanically.

## Workflow

1. Create or select a task before every repository file mutation, including documentation, configuration, tests, generated files, and maintenance.
2. Use a feature parent for behavior, a decision parent for durable technical choices, `REPO` for non-behavior maintenance, and `BOOTSTRAP` only for initialization. A task creating a feature or decision may reserve its future `FEAT-*` or `DEC-*` id, which must exist before closeout.
3. Keep one intentional change and one writer per task.
4. Record owner, concise observable acceptance, proof command or method, and evidence at closeout.
5. Add dependencies only when sequencing truly matters.
6. Put requirements and design detail in their authoritative docs rather than the task ledger.
7. Insert new tasks directly below the CSV header.
8. Move the selected task to `in_progress` before its first write.
9. State task creation and status transitions explicitly.
10. Stop if a task would hide new scope, an architecture choice, or several independent outcomes.

After planning, use execution routing when several ready tasks or delegation choices exist. For one obvious critical-path task, proceed to implementation.

Success means the task ledger is a small execution index rather than a duplicate requirements system.
