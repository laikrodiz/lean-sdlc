---
name: lean-task-planning
description: Convert approved Lean-SDLC feature or decision work into atomic, traceable tasks without turning the task ledger into a second requirements system. Use when scoped work is ready for execution and `planning/tasks.csv` must be created, expanded, or cleaned up.
---

# Lean Task Planning

## Purpose

Use this skill after feature truth and architecture truth are stable enough for execution planning.

Follow the repository's `AGENTS.md`. Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) only when recovering context or resolving a shared contract.

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

## Task Quality Gate

1. One clear outcome.
2. One parent feature or decision.
3. One short, clear, measurable acceptance line.
4. Minimal dependency surface.
5. No hidden extra scope.
6. A clearly stated status when it enters the ledger or changes state.
7. No architecture work hidden under a behavior task.
8. No macro-feature or wrong-level parent used for convenience.

Use the Sol decision profile from the shared [delegation policy](../lean-sdlc-core/references/delegation.md) when task slicing requires judgment.

## Outcome

Success means `planning/tasks.csv` is a small execution ledger that an agent can parse quickly and execute safely without re-inventing the requirements system.
