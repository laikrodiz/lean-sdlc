# Shape

Use Shape when the project problem, user, value, behavior, scope, stage, or current version promise is unclear.

Use Sol `high` for framing. Escalate to `xhigh` only when the business risk or ambiguity warrants it.

1. Read `docs/PROJECT.md` and any active behavior documents.
2. Identify the real problem, affected user, and smallest valuable outcome.
3. Separate observable behavior from technical choices.
4. Make in-scope, deferred, constrained, and non-goal boundaries explicit.
5. Split unrelated outcomes that can be delivered or deferred independently.
6. Surface plausible boundary and failure cases that affect visible behavior; propose `Handle`, `Reject`, `Defer`, or `Impossible by invariant` and put settled cases in acceptance.
7. Replace vague success with observable acceptance and failure signals.
8. Keep stage and version as honest current context, with a small promise and exit evidence.
9. Challenge stale assumptions and oversized promises.
10. Before recording changes, start one task that owns the shaping update.
11. Update `docs/PROJECT.md`; create an optional `docs/features/FEAT-*.md` only when behavior needs durable detail beyond the project file.

Do not choose a stack or create delivery tasks while behavior remains ambiguous.

## Project and Feature boundaries

Group the current outcome in the project promise.
Use an optional Feature document when one durable behavior spans tasks.
Split a Feature when a part has an independent promise, test, or change.
Merge Feature candidates when neither part has useful behavior alone.

Ready means the smallest useful outcome, boundary, acceptance, and current promise are clear enough to decide or plan.
