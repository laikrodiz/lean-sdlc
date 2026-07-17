---
name: lean-execution
description: Choose execution mode for ready Lean-SDLC tasks and dispatch work locally, to subagents, or in checkpointed batches with token-aware model settings. Use when task truth is approved and the next question is how to execute the queue efficiently without losing parity.
---

# Lean Execution

## Purpose

Use this skill after tasks are ready and before code starts.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for required sequence, delegation policy, and proof-first rules.

## What This Skill Owns

1. Choosing execution mode: local, delegated, or batch.
2. Deciding when workers are mandatory.
3. Assigning token-aware delegate models and reasoning effort.
4. Setting worker ownership boundaries.
5. Defining review checkpoints before closeout.

## Execution Modes

1. Local execution:
   Use for one ready task that blocks the next critical step.
2. Delegated execution:
   Use for two or more ready tasks with disjoint write scope.
3. Batch execution:
   Use for larger disjoint queues where the main agent should checkpoint after a batch instead of micromanaging each task one by one.

## Dispatch Rules

1. If one ready task blocks the next main step, keep it local.
2. If two or more ready tasks are disjoint in write scope, spawn workers in parallel.
3. If the work is diagnosis and still unbounded, spawn an explorer first and do not send a worker yet.
4. If the ready queue is larger than three disjoint tasks, use a checkpointed batch.
5. Do not delegate vague work or overlapping write scopes.

## Delegate Profiles

Use `gpt-5.4-mini` by default and choose the lowest effort that still fits:

1. `medium` for mechanical scan work, file inventory, and short summaries.
2. `high` for ordinary analysis, bounded triage, and routine scoped edits.
3. `xhigh` for subtle failures, risky bounded edits, architecture tradeoffs, and cross-artifact contradictions.

## Worker Prompt Rules

Every worker assignment must include:

1. the exact task id and acceptance target,
2. the owned files or boundary,
3. proof expectations,
4. a reminder not to touch unrelated work,
5. a reminder not to revert concurrent changes.

## Review Checkpoints

After worker output:

1. review acceptance fit,
2. review obvious scope creep,
3. review proof existence,
4. route to `lean-verification`,
5. route to `lean-traceability` or `lean-doc-maintenance` if drift risk exists.

## Refusal Rules

1. Do not dispatch before tasks are clean.
2. Do not dispatch when parent truth is still fuzzy.
3. Do not keep everything local by habit when the queue is clearly parallel.
4. Do not burn `xhigh` on grep-grade work.

## Outcome

Success means the task queue is executed with the right mix of local work and subagents, token spend stays disciplined, and review still happens before closeout.
