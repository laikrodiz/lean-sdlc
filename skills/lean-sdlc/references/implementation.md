# Implementation Workflow

Use only when the cause and scope are known and an approved task has measurable acceptance and a proof path. Return to debugging when the cause is uncertain and to refinement when intended behavior is uncertain.

Use Terra at `high` for ordinary engineering. Use Luna at `low` or `medium` for exact mechanical edits with strong automated proof. Use Sol at `high` or `xhigh` for complex or risky implementation.

## Workflow

1. Read the active task and trace it to one feature or decision.
2. Confirm the parent still fits the intended change exactly.
3. Re-read acceptance, verification approach, and diagnostics.
4. Move the task to `in_progress` explicitly when work starts.
5. Declare touched boundaries.
6. Implement only the approved slice.
7. Keep tests, diagnostics, and changed documentation in parity.
8. Avoid opportunistic refactors and additional behavior.
9. Hand off to verification with explicit evidence.

Stop when there is no task, acceptance is vague, proof is undefined, the feature is too broad, or implementation reveals a new durable choice. Repair the appropriate parent truth before continuing.

Success means the change is small, scoped, test-backed, diagnosable, and traceable to the written why.
