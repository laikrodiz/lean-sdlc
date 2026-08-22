# Diagnose

Use Diagnose whenever failing behavior exists and the cause, fault boundary, or correct owner is uncertain.

The user-selected Codex model is the Architect and owns causal reasoning and the repair decision. Lean-SDLC never replaces it. Delegate only bounded reproduction or evidence collection through [subagents.md](subagents.md).

1. Start from the observed symptom, failing test, runtime signal, or user report.
2. Reproduce it, or state the precise reason reproduction is unavailable.
3. Narrow the path until the likely fault surface is small.
4. Separate evidence from hypotheses.
5. Locate the owning contract or module and prefer one root-cause fix there over patches in its callers.
6. Classify the cause as behavior, durable decision, boundary, operation, or implementation.
7. Read-only diagnosis needs no task. Start or claim a task before changing any repository file.
8. Add the smallest failing test or equivalent evidence when practical.
9. When an equivalent failure repeats without new evidence, stop the patch loop. Reassess the hypothesis and fault boundary.
10. Hand off to Deliver only after cause, scope, acceptance, and proof are settled.

Maintainer stops unknown, ambiguous, source-changing, or new retry behavior and routes it to Diagnose, Scout, and Architect.

A confident explanation without reproduction or equivalent evidence remains a hypothesis.

Ready means the root cause is reproduced or tightly bounded and the fix no longer contains diagnostic ambiguity.
