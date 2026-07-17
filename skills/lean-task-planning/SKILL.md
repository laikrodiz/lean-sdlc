---
name: lean-task-planning
description: Convert approved Lean-SDLC feature or decision work into atomic, traceable tasks without turning the task ledger into a second requirements system. Use when scoped work is ready for execution and `planning/tasks.csv` must be created, expanded, or cleaned up.
---

# Lean Task Planning

## Purpose

Use this skill after feature truth and architecture truth are stable enough for execution planning.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for the task contract and non-negotiables.

## What This Skill Owns

1. Converting approved feature or decision work into atomic tasks.
2. Keeping `planning/tasks.csv` lean and parseable.
3. Enforcing `parent_ref` linkage to `FEAT-xxx` or `DEC-xxx`.
4. Writing clear, measurable one-line acceptance criteria for each task.

## Planning Rules

1. Every implementation task must link to a feature or decision.
2. Insert new tasks at the top of `planning/tasks.csv`, directly below the header.
3. Keep one intentional change per task.
4. Every plan item must include clear, measurable acceptance criteria.
5. Keep acceptance concise, observable, and measurable.
6. Put detail in docs, not in the CSV.
7. Use dependencies only when sequencing truly matters.
8. Use decision-linked tasks for durable system-shape work, not for product behavior that belongs under a feature.
9. When a task is added or its status changes, state that transition explicitly to the user.
10. Check feature fit before creating the task; if the change does not fit one feature exactly, split or create the feature first.
11. Run a level check before parent selection so mapping or implementation detail does not get forced into a feature or decision parent.
12. If upcoming work would change code and no task exists yet, create the task first and only then allow implementation.

This is the required path before code.

After planning, route through [../lean-execution/SKILL.md](../lean-execution/SKILL.md) to choose local, delegated, or batch execution.

## What A Good Task Looks Like

1. One clear outcome.
2. One parent feature or decision.
3. One short, clear, measurable acceptance line.
4. Minimal dependency surface.
5. No hidden extra scope.
6. A clearly stated status when it enters the ledger or changes state.
7. One intentional change only.
8. A parent feature or decision that matches the exact behavior or chosen path being changed.
9. No parent abuse just because the right doc has not been cleaned up yet.

## What A Bad Task Looks Like

1. It bundles multiple features.
2. It reads like a mini-spec.
3. It has vague or unmeasurable acceptance such as "works better".
4. It hides architecture work that should be a decision.
5. It depends on half the board.
6. It mixes several code changes that should be tracked separately.
7. It is attached to a macro-feature that should have been split first.
8. It attaches implementation detail to a decision or feature that does not really own it.

## Outcome

Success means `planning/tasks.csv` is a small execution ledger that an agent can parse quickly and execute safely without re-inventing the requirements system.
