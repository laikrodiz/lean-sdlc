---
name: lean-implementation
description: Execute scoped Lean-SDLC tasks while staying inside feature, decision, test, diagnostics, and documentation boundaries. Use when coding against approved tasks and the work must stay aligned with repository truth instead of drifting into opportunistic implementation.
---

# Lean Implementation

## Purpose

Use this skill only after `planning/tasks.csv` exists, the active task is linked to a feature or decision, and the task already has clear, measurable acceptance.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for lifecycle, parity, and anti-bloat rules.

If the queue has several ready disjoint tasks, use [../lean-execution/SKILL.md](../lean-execution/SKILL.md) first instead of defaulting to local execution.

## What This Skill Owns

1. Executing approved tasks.
2. Staying within scoped feature and decision boundaries.
3. Updating docs when implementation changes truth.
4. Keeping tests and diagnostics aligned with the code.
5. Refusing undocumented feature invention.

## Required Workflow

1. Read the active task.
2. Stop immediately if no task exists for the intended code change; create the task first through planning.
3. Trace task to feature or decision.
4. Check that the linked feature still fits the intended behavior exactly; if not, stop and repair feature slicing before coding.
5. Run a level check so mappings, runtime commands, and implementation detail do not get pushed upward into feature or decision docs.
6. Re-read acceptance, verification approach, and diagnostics notes.
7. State explicitly when the task moves to `in_progress`, if that transition happens in the turn.
8. Declare touched boundaries before editing.
9. Implement only the single approved slice in the task.
10. Update only the docs whose truth changed, and push wrong-level detail down before finishing.
11. Hand off to verification with explicit evidence.

## Debug Path

When the active task is a fix or investigation:

1. Reproduce first.
2. Isolate the failing path.
3. Decide whether the root cause is behavior, decision, mapping, boundary, or implementation detail.
4. Update parent docs only if durable truth changed.
5. Keep transient debug detail in logs, tests, code comments, or lower technical docs instead of feature or decision files.

If this diagnosis work is still the main job, use [../lean-debugging/SKILL.md](../lean-debugging/SKILL.md) before continuing here.

## Execution Checkpoints

Follow the execution mode chosen earlier:

1. If execution is local, keep the task local and finish the scoped slice cleanly.
2. If execution is delegated, spawn the assigned `explorer` or `worker` with `gpt-5.4-mini`.
3. Use `medium` for mechanical scans, `high` for ordinary analysis or routine scoped edits, and `xhigh` only for subtle failures or risky bounded work.
4. Do not override the execution plan by habit; use local work only when the task is the immediate critical path or the write scope overlaps too heavily.
5. The main agent must still integrate results and keep docs, tests, and diagnostics in parity.

## Refusal Rules

1. Do not start if there is no task.
2. Do not start if the task lacks clear, measurable acceptance.
3. Do not start if the linked feature lacks proof or diagnostics notes.
4. Do not start if proof is still vague when the behavior is testable or otherwise provable.
5. Do not silently add behavior outside the task.
6. Do not bundle several intentional changes under one task.
7. Do not keep coding under an over-broad feature when the behavior clearly deserves a split.
8. Do not turn feature or decision files into debug notes, implementation recipes, or hardware maps.
9. Do not leave task status changes implicit; say them plainly.
10. Do not leave docs stale when implementation changed truth.
11. Do not keep piling into a god file when a split is the cleaner move.
12. Do not stop at "fix applied"; hand off to verification and then to traceability or doc maintenance if drift is likely.

## Outcome

Success means the code change is small, scoped, test-backed, diagnosable, and still traceable to the written why.
