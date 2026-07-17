---
name: lean-execution
description: Choose execution mode for ready Lean-SDLC tasks and dispatch work locally, to subagents, or in checkpointed batches with token-aware model settings. Use when task truth is approved and the next question is how to execute the queue efficiently without losing parity.
---

# Lean Execution

## Purpose

Use this skill after tasks are ready and before code starts.

Follow the repository's `AGENTS.md`. Read the shared [delegation policy](../lean-sdlc-core/references/delegation.md) before dispatching work. Open the core only when recovering context or resolving a shared contract.

## Execution Modes

1. Local execution:
   Use for one ready task that blocks the next critical step.
2. Delegated execution:
   Use for two or more ready tasks with disjoint write scope.
3. Batch execution:
   Use for larger disjoint queues where the main agent should checkpoint after a batch instead of micromanaging each task one by one.

## Dispatch Rules

1. If one ready task blocks the next main step, keep it local.
2. If two or more substantial tasks have disjoint write scope, consider workers in parallel.
3. If the work is diagnosis and still unbounded, spawn an explorer first and do not send a worker yet.
4. Use a checkpointed batch only when it saves meaningful time or main-agent context.
5. Keep quick tasks local and never delegate vague or overlapping work.

## Delegate Profiles

Use the profiles and availability fallback in the shared delegation policy. Sol owns decisions. Luna executes bounded implementation. Keep `low` as the minimum effort.

## Worker Prompt Rules

Every worker assignment must include:

1. the exact task id and acceptance target,
2. the owned files or boundary,
3. proof expectations,
4. a reminder not to touch unrelated work,
5. a reminder not to revert concurrent changes,
6. the smallest useful context and a concise return contract.

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
3. Do not spawn when delegation overhead is likely to exceed the work.
4. Do not give delegates full history without a demonstrated need.

## Outcome

Success means the task queue is executed with the right mix of local work and subagents, token spend stays disciplined, and review still happens before closeout.
