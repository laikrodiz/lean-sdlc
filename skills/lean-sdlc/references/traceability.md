# Traceability Workflow

Use when sources disagree, links are broken, ownership is uncertain, or context loss makes repository truth unreliable. Traceability diagnoses and reconciles meaning; documentation maintenance only applies cleanup after meaning is settled.

Use Terra at `medium` for link inventory. Use Sol at `medium` or `high` to choose the authoritative truth and resolve contradictions.

## Workflow

1. Start from the active task or changed artifact.
2. Trace backward to one feature or decision, then to scope and project value.
3. Check that indexes point to existing authoritative files.
4. Classify changed truth as behavior, decision, boundary, mapping, or implementation detail.
5. Check whether the feature is exact or over-broad.
6. Identify undocumented durable choices.
7. Trace forward to code, tests, diagnostics, and evidence.
8. Flag broken, contradictory, over-broad, or misrouted links.
9. Decide which source owns the truth.
10. Repair the smallest set needed for one coherent chain.

Do not turn a trace audit into broad rewriting. Once ownership and meaning are settled, route remaining mechanical synchronization to documentation maintenance.

Success means the repository tells one coherent story from business why through evidence.
