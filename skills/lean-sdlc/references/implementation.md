# Implementation Workflow

Use only when the cause and scope are known and an approved task is `In Progress`, owned by the writer, and has measurable acceptance and a proof path. Return to debugging when the cause is uncertain and to refinement when intended behavior is uncertain.

Use Terra at `high` for ordinary engineering. Use Luna at `low` or `medium` for exact mechanical edits with strong automated proof. Use Sol at `high` or `xhigh` for complex or risky implementation.

## Workflow

1. Read the active task and confirm its owner.
2. Trace delivery work to one feature or decision; allow `REPO` only for non-behavior maintenance.
3. Confirm the parent still fits the intended change exactly.
4. Re-read acceptance, proof, verification approach, and diagnostics.
5. Run `lean_check.py --before-write --task TASK-ID --owner OWNER` when the standard ledger exists.
6. Declare touched boundaries.
7. Implement only the approved slice.
8. Keep tests, diagnostics, and changed documentation in parity.
9. Avoid opportunistic refactors and additional behavior.
10. Hand off to verification with explicit evidence.

Stop when there is no owned task, its status is not `In Progress`, acceptance is vague, proof is undefined, the feature is too broad, or implementation reveals a new durable choice. Repair the appropriate parent truth before continuing.

Success means the change is small, scoped, test-backed, diagnosable, and traceable to the written why.
