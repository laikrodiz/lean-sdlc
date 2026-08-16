# Shape

Use Shape when the project problem, user, value, behavior, scope, stage, or current version promise is unclear.

Discussion or proposal requests remain read-only. Brainstorming requests use the same read-only path. Plan and Deliver require explicit implementation authority, explicit implementation wording, or clear confirmation to proceed against a recoverable agreed proposal. If authority is ambiguous, remain read-only.

Apply this intent contract, then the visible-plan contract in [Plan](plan.md), before creating a task. Keep implementation steps transient, and keep `tasks.csv` as the only durable task plan.

## Intent contract

Shape owns the complete intent gate. Before the Architect creates a task or mutates the repository, the Architect naturally confirms `why -> what -> how -> proof`. Shape settles Why and What. Decide and Plan add How and Proof before task creation or mutation:

- Why: the present problem or opportunity and affected user or business value.
- What: the smallest observable outcome plus constraints and non-goals.
- How: the technical approach and task shape after Why and What are stable.
- Proof: acceptance and verification that show the outcome.

Use natural prose. Do not require fixed headings. If a material assumption affects behavior, scope, or architecture, stop for user confirmation. If intent is clear and implementation authority is explicit, continue without another round trip. Brainstorming and rephrasing remain read-only.

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
10. Before recording changes, apply the Plan gate and start one task that owns its matching durable item.
11. Update `docs/PROJECT.md`; create an optional `docs/features/FEAT-*.md` only when behavior needs durable detail beyond the project file.

Do not choose a stack or create delivery tasks while behavior or implementation authority remains ambiguous.

## Project and Feature boundaries

Group the current outcome in the project promise.
Use an optional Feature document when one durable behavior spans tasks.
Split a Feature when a part has an independent promise, test, or change.
Merge Feature candidates when neither part has useful behavior alone.

Ready means the smallest useful outcome, boundary, acceptance, and current promise are clear enough to decide or plan.
