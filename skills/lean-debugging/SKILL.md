---
name: lean-debugging
description: Reproduce, isolate, and classify failing behavior before deciding whether code, features, decisions, mappings, or lower technical docs should change. Use when the work is diagnosis, bug investigation, glitch triage, or root-cause analysis rather than straightforward implementation.
---

# Lean Debugging

## Purpose

Use this skill when the job is to understand a failure before changing code or parent docs.

Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) first for required sequence, proof-first rules, and abstraction hygiene.

## What This Skill Owns

1. Reproducing the failure.
2. Isolating the failing path.
3. Classifying the root cause at the right level.
4. Deciding whether the next step is task planning, implementation, traceability, or doc maintenance.
5. Keeping transient debug detail out of durable requirement truth.

## Workflow

1. Start from the reported symptom, failing test, runtime signal, or user complaint.
2. Reproduce the issue or state clearly why reproduction is currently impossible.
3. Narrow the failing path until the likely fault surface is small enough to reason about.
4. Classify the root cause as behavior, decision, mapping, boundary, or implementation detail.
5. Check whether an existing active task already covers the fix.
6. If no task covers it, route back through `lean-refine` or `lean-task-planning` before code.
7. Update features or decisions only if durable truth changed.
8. Keep transient findings in logs, tests, comments, or lower technical docs instead of feature or decision files.
9. Hand off to `lean-implementation` only when the fix is properly scoped.

## Proof-First Rules

1. Prefer test-first when the failing behavior is easy to capture in a test.
2. If a test is awkward, define another explicit proof path before the fix.
3. Do not accept "I know what the problem is" as proof.

## Delegation Checkpoints

Use sub-agents only for bounded sidecar diagnosis:

1. Spawn an `explorer` with `gpt-5.4-mini` for log triage, trace scans, or isolated codebase questions.
2. Use `xhigh` when the failure mode is subtle or spans several artifacts.
3. Use `medium` or `high` for short inventory or mechanical scan work.
4. Keep root-cause classification and next-step choice in the main agent.

## Refusal Rules

1. Do not jump straight to code when the failure is not reproduced or bounded.
2. Do not turn feature or decision files into debugging notebooks.
3. Do not treat a guess as a diagnosis.
4. Do not close the loop without routing into verification after the fix.

## Outcome

Success means the failure is reproduced or bounded, the root cause is classified at the right level, and the next step is clear without polluting durable docs.
