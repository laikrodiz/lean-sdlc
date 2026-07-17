# Debugging Workflow

Use whenever failing behavior exists and the cause, fault boundary, or correct owner is uncertain. This lane still owns the work when a fix request exists but the diagnosis is only a guess.

Use Luna at `low` or `medium` for exact log and test collection, Terra at `high` for ordinary reproduction and tracing, and Sol at `high` or `xhigh` for subtle root-cause classification.

## Workflow

1. Start from the symptom, failing test, runtime signal, or user complaint.
2. Reproduce it or state why reproduction is currently impossible.
3. Narrow the path until the likely fault surface is small.
4. Classify the cause as behavior, decision, mapping, boundary, or implementation detail.
5. Check whether an active task already covers the fix.
6. Read-only diagnosis may continue without a task. Before changing any repository file, activate the task or return to refinement or task planning.
7. Update durable truth only when the diagnosis changes it and the active task covers that update.
8. Keep transient findings in tests, logs, comments, or lower technical docs.
9. Hand off to implementation only when cause, scope, acceptance, and proof are settled.

Prefer a failing test as reproduction when practical. A confident explanation without reproduction or equivalent evidence remains a hypothesis.

Success means the failure is reproduced or bounded, the root cause has the correct owner, and the implementation task no longer contains diagnostic ambiguity.
