# Decide

Use Decide after intent is stable and implementation needs a durable technical choice or boundary.

Use Sol `high`. Use `xhigh` for security, concurrency, migrations, irreversible data changes, or costly architecture.

1. Read `docs/PROJECT.md` and the behavior the choice serves.
2. Identify the exact decision, constraints, reversal cost, and failure cost.
3. Compare only viable options using maturity, testability, diagnostics, maintainer skill, and maintenance cost.
4. Choose boundaries from responsibility and observed pressure rather than project-size buckets.
5. Stop at the first boundary that holds: direct code, cohesive function, module, package or component, then a separate process or service only for operational isolation.
6. Strengthen a boundary for a distinct transformation, state, I/O or failure mode, separate change reason, useful contract test, or current replacement need.
7. Prefer concrete implementations. Add interfaces, factories, or configuration only for a present alternative, runtime seam, or test seam.
8. Define the narrow input, output, and failure contract plus the signal that would justify another architecture pass.
9. Choose the smallest defensible path and prefer a hard cut unless compatibility is an explicit requirement.
10. Start a task before recording the choice.
11. Create `docs/decisions/DEC-*.md` only when the decision is costly to reverse, easy to forget, or likely to be re-litigated.
12. Put commands, recipes, mappings, and volatile tuning in code, tests, technical docs, or `docs/OPERATIONS.md`.

Decide adds the technical approach to How after Why and What are stable. Tie each technical choice to the confirmed intent or constraint it serves. If a choice has no such link, return to Shape before recording it.

## Decision boundary

Record one Decision for one independent reversal boundary.
Keep a choice local when it is cheap to reverse and clear in code, tests, or technical documentation.

Return to Shape when uncertainty concerns desired behavior or value.

Ready means delivery can proceed without hiding a consequential choice inside implementation.
