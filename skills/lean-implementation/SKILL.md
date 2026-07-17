---
name: lean-implementation
description: Execute scoped Lean-SDLC tasks while staying inside feature, decision, test, diagnostics, and documentation boundaries. Use when coding against approved tasks and the work must stay aligned with repository truth instead of drifting into opportunistic implementation.
---

# Lean Implementation

## Purpose

Use this skill only after `planning/tasks.csv` exists, the active task is linked to a feature or decision, and the task already has clear, measurable acceptance.

Follow the repository's `AGENTS.md`. Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) only when recovering context or resolving a shared contract.

If the queue has several ready disjoint tasks, use [../lean-execution/SKILL.md](../lean-execution/SKILL.md) first instead of defaulting to local execution.

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

Follow the chosen execution mode and shared [delegation policy](../lean-sdlc-core/references/delegation.md):

1. Keep critical-path or overlapping work local.
2. Use the Luna execution profile for delegated edits only when acceptance, owned files, and proof are exact.
3. Keep scope decisions, ambiguous implementation choices, integration, and closeout with the main agent.
4. Keep docs, tests, and diagnostics in parity after integration.

## Refusal Rules

1. Do not start if there is no task.
2. Do not start if the task lacks clear, measurable acceptance.
3. Do not start if the linked feature lacks proof or diagnostics notes.
4. Do not start if proof is still vague when the behavior is testable or otherwise provable.
5. Do not silently add behavior outside the task.
6. Do not bundle several intentional changes under one task.
7. Do not keep coding under an over-broad feature when the behavior clearly deserves a split.
8. Do not turn feature or decision files into debug notes, implementation recipes, or hardware maps.
9. Do not leave task status changes or documentation updates implicit.
10. Do not keep piling into a mixed-responsibility file when a split is cleaner.
11. Do not stop at "fix applied"; hand off to verification and reconcile likely drift.

## Outcome

Success means the code change is small, scoped, test-backed, diagnosable, and still traceable to the written why.
