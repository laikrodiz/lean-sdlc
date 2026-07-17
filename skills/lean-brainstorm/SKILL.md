---
name: lean-brainstorm
description: Turn a rough idea into the first Lean-SDLC project truth using Socratic questioning and Occam's razor. Use when the project is still vague, when the user needs a first brief and scope, or when initial feature files and version framing must be drafted before architecture or code work.
---

# Lean Brainstorm

## Purpose

Use this skill when the project is still an idea dump and no stable truth exists yet.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for shared lifecycle and contract rules.

## What This Skill Owns

1. Socratic questioning at project start.
2. Occam cuts on early scope.
3. First draft of project brief and scope.
4. Initial feature candidates with separate feature files.
5. Initial stage and version framing.

## Workflow

1. Ask what real problem hurts enough to solve now.
2. Ask who feels it directly.
3. Ask what smallest useful outcome has value.
4. Ask what hard constraints already exist.
5. Ask what can be safely postponed.
6. Ask which early durable choices already seem unavoidable.
7. Challenge every large assumption with a smaller alternative.
8. Slice early features at the smallest independently valuable behavior level, not at module or roadmap-bucket level.
9. Route prototype limits, temporary bindings, and volatile detail into scope or triggered mapping docs instead of feature or decision files.
10. Produce first drafts for `PROJECT_BRIEF.md`, `SCOPE.md`, `FEATURE_INDEX.csv`, `DECISION_INDEX.csv`, and initial feature and decision files where justified.

## Output Standard

At the end of brainstorming there should be:

1. a sharp project why,
2. clear in-scope and out-of-scope boundaries,
3. a current stage of `discovery` or `foundation`,
4. a current version goal,
5. first feature files with business context and value,
6. early decision files only where a durable choice is already obvious,
7. no implementation tasks yet.

## Boundaries

1. Do not design detailed architecture here.
2. Do not create implementation tasks here.
3. Do not choose language or framework before the first real features are visible.
4. Do not let the user smuggle in a giant roadmap under one feature.
5. Do not create decision files for trivial preferences.
6. Do not create macro-features such as whole capability areas, modules, or workflows families when smaller outcomes are already visible.
7. Do not put channel numbers, route tables, runtime commands, or other mapping detail into feature or decision truth during brainstorming.

## Challenge Rules

Default questions to surface:

1. What is the smallest cut that still matters?
2. Which actor, state, integration, or config can be removed?
3. What would make this too large to carry?
4. Which idea belongs in deferred scope instead of version one?

## Outcome

Success means the project moved from vague intent to a small, coherent first slice of written truth without starting architecture theater or code prematurely.
