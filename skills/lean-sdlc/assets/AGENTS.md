# Lean-SDLC Repository Rules

For any request that may change a repository file, investigate a failure, or close work, invoke `$lean-sdlc` first and let it select one primary lane. Only read-only explanation and inspection may use a fast path.

## Authority and Reading Order

1. `docs/PROJECT_BRIEF.md` — why and success
2. `docs/SCOPE.md` — current boundary, stage, and version
3. relevant feature and decision files — behavior and durable choices
4. triggered technical docs — shared architecture, interfaces, or mappings
5. `planning/tasks.csv` — execution ledger
6. code and tests — implemented reality and evidence

If these disagree, flag the conflict and route through traceability before closeout.

## Required Gates

1. No repository file mutation without one `In Progress` task owned by the writer. Inserting that authorizing row into `planning/tasks.csv` is the only routine pre-task write.
2. Use a feature or decision parent for delivery work, `REPO` for maintenance, and `BOOTSTRAP` only during initialization.
3. No implementation without measurable acceptance and a proof path.
4. Unknown failure cause enters debugging before implementation.
5. No task moves to `Done` without evidence, promised diagnostics, and document parity.
6. State every task status transition explicitly.

## Change Ownership

- project value or success → `docs/PROJECT_BRIEF.md`
- temporary boundary, deferred scope, stage, or version → `docs/SCOPE.md`
- actor-facing behavior → one feature file
- durable costly-to-reverse choice → one decision file
- shared system shape → `docs/ARCHITECTURE.md`
- mappings, commands, file layouts, or protocol fields → `docs/INTERFACES.md` or `docs/maps/*.md`
- local mechanism → code, tests, or comments

Split a statement until one owner wins. Keep one independently valuable outcome per feature and one intentional change per task.

## Models and Agents

- Explicit user model and reasoning requests override automatic routing.
- Treat Max as single-model work unless the user permits delegation; Ultra permits multi-agent work.
- Default to no subagents and at most two workers with separate tasks and paths.
- Reuse a worker only while task, role, ownership, and assumptions remain stable.
- Workers return to the main agent; workers do not hand off directly or close tasks.
- Keep shared instructions stable, send task deltas, and never create work merely to warm a cache.

## Routing Boundaries

- New or unclear behavior → refine before planning.
- Stable behavior needing technical choices → architecture.
- Unknown failure cause → debugging; known cause and approved task → implementation.
- Uncertain source of truth or broken links → traceability.
- Approved cleanup with settled meaning → documentation maintenance.
- Stage or version meaning → versioning; maintenance only propagates an approved change.
- Claimed completion → verification.

Prefer the smallest defensible solution. Create optional docs only when repeated shared pressure justifies them. Do not invent undocumented scope or preserve compatibility without an explicit requirement.
