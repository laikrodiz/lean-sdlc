---
name: lean-refine
description: Tighten Lean-SDLC project truth by removing ambiguity, splitting clean features, defining proof and diagnostics, and identifying which optional docs are actually justified. Use when brainstorm output is still fuzzy, contradictory, oversized, or not ready for architecture or task planning.
---

# Lean Refine

## Purpose

Use this skill after `lean-brainstorm` and before architecture or task planning.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for repository contracts and trigger rules.

## What This Skill Owns

1. Tightening scope boundaries.
2. Splitting feature files into clean units.
3. Tightening decision files into durable chosen paths.
4. Removing contradictions and fuzzy language.
5. Defining acceptance, verification, and diagnostics at feature level.
6. Using functional and non-functional requirements as a review lens without spawning a second requirements system.
7. Identifying which optional docs are justified.

## Workflow

1. Re-read `PROJECT_BRIEF.md`, `SCOPE.md`, `FEATURE_INDEX.csv`, `DECISION_INDEX.csv`, and active feature and decision files.
2. Run a level check on every planned edit: behavior, decision, boundary, mapping, or implementation detail.
3. Find contradictions between value, behavior, scope, exclusions, and chosen paths.
4. Check whether each feature is truly one independently valuable behavior slice.
5. Split large or mixed features into smaller units when they hide several outcomes, actor goals, or acceptance clusters.
6. Tighten decisions so they record real chosen paths, not trivia, recipes, or background noise.
7. Push prototype or hardware mappings, route tables, file names, and commands out of features and decisions into the right lower doc or code location.
8. Rewrite vague behavior into observable behavior.
9. Check functional behavior and cross-cutting constraints as a refinement lens.
10. Add acceptance criteria, verification approach, and diagnostics notes to every active feature.
11. Decide whether triggered docs are now justified.

This is the required path before task planning when scope, behavior, decisions, or abstraction level changed.

## Feature Fit Gate

Before task planning, force these questions on every active feature:

1. Does this file describe one outcome or several?
2. Could part of it ship later without breaking the rest?
3. Does it have more than one real acceptance cluster?
4. Would a new code change fit exactly, or is the feature too broad?

If the answer exposes mixed scope, split the feature before planning tasks.

## Decision Fit Gate

Before accepting a decision edit, force these questions:

1. Is this a durable chosen path or just a temporary implementation note?
2. Is reversal costly enough to matter?
3. Will this likely be forgotten or re-litigated later?
4. Does this belong in architecture, interfaces, mapping docs, or code instead?

If the answer points downward, move the detail out of the decision file.

## Delegation Checkpoints

Use sub-agents when they reduce context instead of multiplying it:

1. Spawn an `explorer` with `gpt-5.4-mini` for parallel contradiction scans or feature-boundary audits.
2. Use `xhigh` when the refinement question is non-trivial and changes scope shape.
3. Use `medium` or `high` for simple inventory or lookup work.
4. Keep final feature splits and scope decisions in the main agent.

## Trigger Checks

Propose new docs only when there is real pressure:

1. several core entities or roles,
2. lifecycle transitions that affect correctness,
3. external interfaces or file contracts,
4. persistence constraints,
5. cross-cutting test policy,
6. cross-cutting diagnostics policy,
7. meaningful security, safety, reliability, or performance risk.

## Requirement Lens

Apply this simple check to every active area:

1. What behavior must exist?
2. What cross-cutting constraints must hold?

Put behavior mostly in feature files.
Put durable cross-cutting choices mostly in decisions and triggered technical docs.

## Refusal Rules

1. Do not let one feature hide a roadmap.
2. Do not write architecture prose when the real issue is unclear scope.
3. Do not create tasks until the active features are small and testable.
4. Do not keep vague placeholders such as "handle edge cases later" without saying which ones are deferred.
5. Do not accept feature files that read like capability areas, subsystems, or release buckets.
6. Do not accept decision files that read like implementation recipes, debug logs, or tuning diaries.
7. Do not let implementation start when refine work is still obviously pending.

## Outcome

Success means each active feature is small, scannable, business-grounded, provable, diagnosable, and ready either for architecture or for direct task planning.
