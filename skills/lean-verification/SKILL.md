---
name: lean-verification
description: Prove Lean-SDLC task completion against acceptance, tests, and diagnostics before work is closed. Use when implementation needs objective evidence, when tasks must move to done, or when the repo needs a disciplined decision on pass, fail, or reopen.
---

# Lean Verification

## Purpose

Use this skill after implementation and before task closeout.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for proof, diagnostics, and parity rules.

## What This Skill Owns

1. Checking acceptance against written feature truth.
2. Reviewing verification evidence.
3. Confirming diagnostics or failure signals behave as expected.
4. Deciding whether a task can close or must reopen.

## Verification Workflow

1. Read the active task and linked feature or decision.
2. Compare implemented behavior against acceptance criteria.
3. Check whether promised tests, smoke paths, or other proof actually exist and pass.
4. Check whether diagnostics or failure signals are present and useful.
5. Check whether the linked feature and decision docs still match the new reality at the right level of abstraction.
6. Check whether wrong-level detail is still trapped in feature or decision files instead of lower docs or code.
7. Keep the task open if any part of acceptance is still unmet.
8. Keep the task open if feature or decision docs still describe the old truth or hide the behavior inside a macro-feature.
9. Keep the task open if wrong-level detail still sits in feature or decision truth.
10. Move the task to `done` only when acceptance is fully met and evidence exists.
11. State explicitly whether the task remains `in_progress`, reverts for more work, or moves to `done`.
12. Record pass, fail, or reopen reasoning.
13. If implementation or debugging likely caused parent drift, route into `lean-traceability` or `lean-doc-maintenance` before closeout.

Proof should be test-first when practical. When that is not practical, the alternative proof path still must be explicit and real.

## Delegation Checkpoints

Use sub-agents when verification has independent sidecar questions:

1. Spawn an `explorer` with `gpt-5.4-mini` for bounded log review, test-failure summarization, or parallel drift checks.
2. Use `xhigh` when the evidence is ambiguous or the failure mode is subtle.
3. Use lower effort for short summaries or mechanical scan work.
4. Keep the final close, fail, or reopen decision in the main agent.

## Refusal Rules

1. Do not treat "it seems fine" as evidence.
2. Do not close a task if diagnostics are missing where they were promised.
3. Do not close a task if any acceptance point is still open.
4. Do not close a task while features or decisions still need sync.
5. Do not close a task while feature or decision docs still carry mapping or implementation detail that belongs lower.
6. Do not change closeout state silently; say the transition plainly.
7. Do not ignore doc drift discovered during verification.
8. Do not force close a task just because the code compiles.
9. Do not skip the post-implementation review path when drift risk is obvious.

## Outcome

Success means completion is based on evidence, not optimism, and the task status honestly matches reality.
