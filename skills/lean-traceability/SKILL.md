---
name: lean-traceability
description: Audit and repair Lean-SDLC links between brief, scope, features, decisions, tasks, code, tests, and diagnostics. Use when documents drift, tasks lose their parent truth, code no longer matches the written plan, or the repo must recover safely after compaction.
---

# Lean Traceability

## Purpose

Use this skill when the chain of intent is breaking or needs explicit repair.

This is the default review path after implementation or debugging bursts when parent truth may have drifted.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for authority order, reading order, and repository contracts.

## What This Skill Owns

1. Checking that work traces back to business intent.
2. Finding drift between feature files, decision files, indexes, tasks, code, tests, and diagnostics.
3. Repairing missing or broken links.
4. Checking that features and decisions are written at the right abstraction level.
5. Helping resume cleanly after context loss.

## Audit Workflow

1. Start from the active task or changed artifact.
2. Trace backward to feature or decision.
3. Trace backward again to scope and project brief.
4. Check that CSV indexes still point to the right files.
5. Run a level check on the changed truth: behavior, decision, boundary, mapping, or implementation detail.
6. Check whether the linked feature is exact or over-broad for the changed behavior.
7. Check whether the work introduced a durable chosen path that needs a decision.
8. Trace forward to code, tests, and diagnostics.
9. Flag any broken, contradictory, over-broad, or misrouted link.
10. Repair the smallest set of docs needed to restore a clean chain at the right abstraction level.

## Delegation Checkpoints

This skill benefits from parallel bounded reads:

1. Spawn `explorer` agents with `gpt-5.4-mini` for separate trace paths or drift checks.
2. Use `xhigh` when the contradiction is subtle or spans several artifacts.
3. Use lower effort for straightforward link inventory.
4. Keep final reconciliation and source-of-truth decisions in the main agent.

## Common Failures

1. Task has no parent feature or decision.
2. Feature exists in code but not in docs.
3. Decision exists in practice but not in a decision file.
4. Acceptance changed in code but not in the feature file.
5. Tests prove different behavior than the written scope.
6. Diagnostics exist nowhere the feature promised them.
7. One feature hides several independent outcomes.
8. A code change should have created a new feature or split an old one.
9. Mapping detail leaked into a feature or decision.
10. A decision file describes a recipe instead of a durable chosen path.

## Outcome

Success means the repo once again tells one coherent story from business why through completed evidence.
