# Lean-SDLC Repository Rules

For any request that may change project truth or code, investigate a failure, or close work, invoke `$lean-sdlc` first and let it select one primary lane. Read-only explanations and trivial non-behavior maintenance may use a fast path.

## Authority and Reading Order

1. `docs/PROJECT_BRIEF.md` — why and success
2. `docs/SCOPE.md` — current boundary, stage, and version
3. relevant feature and decision files — behavior and durable choices
4. triggered technical docs — shared architecture, interfaces, or mappings
5. `planning/tasks.csv` — execution ledger
6. code and tests — implemented reality and evidence

If these disagree, flag the conflict and route through traceability before closeout.

## Required Gates

1. No behavior or code change without one exact feature or decision parent.
2. No implementation without an active task, measurable acceptance, and a proof path.
3. Unknown failure cause enters debugging before implementation.
4. No task moves to `done` without evidence, promised diagnostics, and document parity.
5. State every task status transition explicitly.

## Change Ownership

- project value or success → `docs/PROJECT_BRIEF.md`
- temporary boundary, deferred scope, stage, or version → `docs/SCOPE.md`
- actor-facing behavior → one feature file
- durable costly-to-reverse choice → one decision file
- shared system shape → `docs/ARCHITECTURE.md`
- mappings, commands, file layouts, or protocol fields → `docs/INTERFACES.md` or `docs/maps/*.md`
- local mechanism → code, tests, or comments

Split a statement until one owner wins. Keep one independently valuable outcome per feature and one intentional change per task.

## Routing Boundaries

- New or unclear behavior → refine before planning.
- Stable behavior needing technical choices → architecture.
- Unknown failure cause → debugging; known cause and approved task → implementation.
- Uncertain source of truth or broken links → traceability.
- Approved cleanup with settled meaning → documentation maintenance.
- Stage or version meaning → versioning; maintenance only propagates an approved change.
- Claimed completion → verification.

Prefer the smallest defensible solution. Create optional docs only when repeated shared pressure justifies them. Do not invent undocumented scope or preserve compatibility without an explicit requirement.
