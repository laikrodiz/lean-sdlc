# Decide

Use Decide after intent is stable and implementation needs a durable technical choice or boundary.

Use Sol `high`. Use `xhigh` for security, concurrency, migrations, irreversible data changes, or costly architecture.

1. Read `docs/PROJECT.md` and the behavior the choice serves.
2. Identify the exact decision, constraints, reversal cost, and failure cost.
3. Compare only viable options using maturity, testability, diagnostics, operator skill, and maintenance cost.
4. Choose the smallest defensible path.
5. Prefer a hard cut unless compatibility is an explicit requirement.
6. Start a task before recording the choice.
7. Create `docs/decisions/DEC-*.md` only when the decision is costly to reverse, easy to forget, or likely to be re-litigated.
8. Put commands, recipes, mappings, and volatile tuning in code, tests, technical docs, or `docs/OPERATIONS.md`.

Return to Shape when uncertainty concerns desired behavior or value.

Ready means delivery can proceed without hiding a consequential choice inside implementation.
