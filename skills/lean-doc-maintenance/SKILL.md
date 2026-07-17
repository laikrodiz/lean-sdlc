---
name: lean-doc-maintenance
description: Keep Lean-SDLC documentation current, small, and structurally healthy as the project evolves. Use when docs drift from code, when stage or version framing changed, when new triggered docs are justified, or when files are growing into stale or mixed-responsibility planning objects.
---

# Lean Doc Maintenance

## Purpose

Use this skill whenever repository truth needs explicit cleanup instead of another silent code-first turn.

This is the default cleanup path after implementation bursts, debug bursts, or drift discovery when docs need repair before more work continues.

Follow the repository's `AGENTS.md`. Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) only when recovering context or resolving a shared contract.

## Maintenance Workflow

1. Audit active brief, scope, feature, decision, index, and task docs against current reality.
2. Update only the docs whose truth changed.
3. Keep `FEATURE_INDEX.csv` and `DECISION_INDEX.csv` aligned with their files.
4. Run a level check and move misrouted detail down to the right owner.
5. Split features that now hide several outcomes or acceptance clusters.
6. Create or update decisions when implementation introduced durable chosen paths.
7. Create `INTERFACES.md` or `docs/maps/*.md` when mappings or command tables need a stable home.
8. Create triggered docs when the project now clearly needs them.
9. Split large files before they become unreadable.
10. Remove dead text that no longer matches current intent.

Apply the shared [delegation policy](../lean-sdlc-core/references/delegation.md). Luna may perform exact mechanical edits. Keep source-of-truth, document ownership, feature split, and decision changes with the Sol decision profile.

## Rules

1. Do not keep duplicate truth in multiple places.
2. Prefer moving detail into the right authoritative file over adding summaries everywhere.
3. Prefer deletion over stale placeholders.
4. Keep root files sparse and central docs centralized.
5. Do not leave macro-features in place just because splitting them is inconvenient.
6. Do not leave implementation recipes or mapping clutter inside feature or decision truth just because the nearest file is convenient.
7. Do not let "we will clean docs later" become the reason drift survives into the next task.

## Outcome

Success means the repo still reads like one honest system instead of a pile of abandoned planning fossils.
