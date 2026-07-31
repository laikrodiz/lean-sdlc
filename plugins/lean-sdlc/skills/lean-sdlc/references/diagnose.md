# Diagnose

Use Diagnose whenever failing behavior exists and the cause, fault boundary, or correct owner is uncertain.

Use Terra `high` for ordinary diagnosis. Use Sol `high` or `xhigh` for subtle, high-risk, security, concurrency, or migration failures. Delegate bounded reproduction or log collection only through [subagents.md](subagents.md).

1. Start from the observed symptom, failing test, runtime signal, or user report.
2. Reproduce it, or state the precise reason reproduction is unavailable.
3. Narrow the path until the likely fault surface is small.
4. Separate evidence from hypotheses.
5. Locate the owning contract or module and prefer one root-cause fix there over patches in its callers.
6. Classify the cause as behavior, durable decision, boundary, operation, or implementation.
7. Read-only diagnosis needs no task. Start or claim a task before changing any repository file.
8. Add the smallest failing test or equivalent evidence when practical.
9. Hand off to Deliver only after cause, scope, acceptance, and proof are settled.

A confident explanation without reproduction or equivalent evidence remains a hypothesis.

Ready means the root cause is reproduced or tightly bounded and the fix no longer contains diagnostic ambiguity.
