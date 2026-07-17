---
name: lean-sdlc-core
description: Lean-SDLC control plane for repository lifecycle, document contracts, version framing, traceability, tests, diagnostics, and anti-bloat rules. Use when creating or adapting a repo around Lean-SDLC, when another lean skill needs the shared rules, or when the project needs stage/version guidance, doc spawn triggers, or scope discipline.
---

# Lean-SDLC Core

## Purpose

Use this skill as the shared operating system for the Lean-SDLC bundle.

This skill owns the invariant rules. The other `lean-*` skills should stay narrow and delegate back here for lifecycle, contracts, and trigger logic instead of copying process prose.

## What This Skill Owns

1. Lifecycle model: stage, version, iteration.
2. Mandatory repository shape.
3. Authority order and resume reading order.
4. Document contracts and spawn triggers.
5. Abstraction hygiene and change routing.
6. Required sequence and approval checkpoints.
7. Execution-mode and delegation rules.
8. Task linkage and parity rules.
9. Test and diagnostics gates.
10. Occam, Socratic, delegation, and file-split rules.

## Non-Negotiables

1. Preserve the chain: `why -> what -> how -> prove/observe -> task -> artifact -> verification`.
2. Keep feature files as the main units of business and behavior truth.
3. Do not start implementation before scoped truth exists.
4. Do not allow a task without a linked feature or decision.
5. Do not touch code before the task exists in `planning/tasks.csv` with clear, measurable acceptance.
6. Keep one intentional change per task.
7. Check feature fit before planning or implementing work. Split or create a feature first if the behavior does not fit exactly.
8. Do not let one feature hide several independent outcomes.
9. Check decision fit before closeout. Write or update a decision if a durable chosen path appeared.
10. Do not let feature or decision files turn into scratchpads for runtime detail.
11. Do not treat a task as complete without evidence and satisfied acceptance.
12. State every task status transition explicitly when it happens.
13. Do not invent undocumented scope.
14. Challenge unnecessary complexity before accepting it.
15. Keep docs, tasks, code, tests, and diagnostics in parity.
16. Do not skip verification, traceability, or doc cleanup after meaningful implementation or debugging work.
17. Define proof before code, with test-first as the default when practical.
18. Choose execution mode deliberately instead of defaulting to local work.

## Reading Order

When entering a Lean-SDLC repo or resuming after compaction:

1. Read `AGENTS.md`.
2. Read `docs/SCOPE.md`.
3. Read `docs/FEATURE_INDEX.csv` and `docs/DECISION_INDEX.csv`.
4. Read the relevant feature and decision files.
5. Read architecture only if it exists and matters.
6. Read `planning/tasks.csv`.
7. Inspect code only after the chain above is clear.

## Lifecycle Model

Use the stage, version, and iteration model from:

1. [references/lifecycle.md](./references/lifecycle.md)

Treat stage, version, and iteration as separate axes. Do not collapse them into one fuzzy label.

## Repository Contracts

Use the required file contracts and task schema from:

1. [references/repo-contracts.md](./references/repo-contracts.md)

Keep extra docs absent until triggered. Empty structure is fake structure.

Use the AGENTS baseline from:

1. [references/agents-template.md](./references/agents-template.md)

## Trigger Rules

Spawn additional docs only when complexity justifies them:

1. `ARCHITECTURE.md` for several meaningful modules, boundaries, or flows.
2. `TEST_STRATEGY.md` when proof becomes shared policy.
3. `DIAGNOSTICS.md` when runtime visibility becomes shared policy.
4. `INTERFACES.md` or `docs/maps/*.md` when shared mappings, commands, bindings, or contracts need a stable home outside features and decisions.
5. `DOMAIN_MODEL.md`, `STATE_MODEL.md`, `PERMISSIONS.md`, `DATA_MODEL.md`, or `RISKS.md` only when the project structure or risk demands them.
6. `docs/versions/V-*.md` only when version history or changed business context needs preserving.

## Abstraction Hygiene

Before editing docs, creating tasks, or touching code, force one owner to win:

1. project why or success meaning,
2. temporary boundary or deferred scope,
3. actor-facing behavior,
4. durable chosen path,
5. shared system shape,
6. mappings or command tables,
7. low-level implementation detail.

Use `PROJECT_BRIEF.md`, `SCOPE.md`, feature files, decision files, `ARCHITECTURE.md`, `INTERFACES.md` or `docs/maps/*.md`, and code or tests accordingly.

If one statement tries to live in two layers, split it.

## Required Sequence

Treat the Lean-SDLC flow as gates, not optional suggestions:

1. Use `lean-brainstorm` or `lean-refine` before new scope or behavior work.
2. Use `lean-task-planning` before code.
3. Choose execution mode: local, delegated, or batch.
4. Use `lean-debugging` when the work is diagnosis or a fix investigation.
5. Use `lean-implementation` only from an active task.
6. Use `lean-verification` before any task moves to `done`.
7. Use `lean-traceability` or `lean-doc-maintenance` after implementation bursts, debug bursts, or drift discovery.

Do not jump straight from code to `done`.

## Execution Mode

Choose how work runs after tasks are ready:

1. local execution for one critical-path task,
2. delegated execution for two or more disjoint ready tasks,
3. batch execution for larger disjoint queues with checkpoints.

Use `gpt-5.4-mini` with:

1. `medium` for mechanical scan work,
2. `high` for ordinary analysis and routine worker edits,
3. `xhigh` for subtle failures, risky bounded edits, and cross-artifact contradictions.

## Debug Path

When the work is debugging:

1. reproduce first,
2. isolate the failing path,
3. classify the problem as behavior, decision, mapping, boundary, or implementation detail,
4. update parent docs only if durable truth changed,
5. keep transient debug detail out of feature and decision files.

## Proof-First

Before code starts:

1. define proof first,
2. default to test-first when the behavior is testable at low cost,
3. if full red/green TDD is awkward, write the explicit proof path anyway,
4. do not treat a task as ready when proof is still vague.

## Tests And Diagnostics

Treat proof and visibility as design inputs, not cleanup work.

No feature is ready for implementation until it defines:

1. acceptance criteria,
2. verification approach,
3. diagnostics or failure signals.

Foundation work should establish:

1. one runnable smoke path,
2. clear config or input validation,
3. useful error reporting,
4. a small self-check or health path where relevant.

## Functional And Non-Functional Requirements

Do not model functional and non-functional requirements as separate first-class objects.

Use them as a refinement lens:

1. behavior requirements belong mainly in feature files,
2. cross-cutting constraints belong in scope, decisions, architecture, risks, test strategy, diagnostics, permissions, interfaces, or data model.

## Occam And Socratic Behavior

During planning, always pressure-test the request:

1. Ask what problem hurts enough to solve now.
2. Ask who feels it directly.
3. Ask what smallest outcome has value.
4. Ask what can be safely deferred.
5. Ask what permanent complexity the request adds.

Default bias:

1. fewer actors,
2. fewer states,
3. fewer integrations,
4. fewer configs,
5. fewer abstractions,
6. fewer docs.

## File And Delegation Discipline

Keep files small and clear:

1. Soft warning around `250-300` source lines.
2. Split review around `400+` lines.
3. Split earlier when one file mixes orchestration, rules, IO, or diagnostics.

Use the delegation policy from:

1. [references/delegation.md](./references/delegation.md)

Default delegate profile:

1. model `gpt-5.4-mini`,
2. reasoning effort chosen by task shape: `medium`, `high`, or `xhigh`.

Use the lowest effort that still fits the task. Save `xhigh` for subtle failures, risky bounded edits, and cross-artifact contradictions.

The main agent keeps scope, decision ownership, and final synthesis.

## Routing

Use the bundle map when choosing the smallest appropriate lean skill:

1. [references/skill-map.md](./references/skill-map.md)

## Outcome

Success means:

1. the repo stays lean,
2. work stays traceable to business intent,
3. tests and diagnostics exist before implementation starts,
4. stage and version framing stay current,
5. features and decisions stay scannable through CSV indexes and separate files,
6. the project can resume safely after memory loss.
