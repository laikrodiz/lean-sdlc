---
name: lean-sdlc-core
description: Lean-SDLC control plane for repository setup, lifecycle, document contracts, routing, traceability, proof, and anti-bloat rules. Use when creating or adapting a Lean-SDLC repo, auditing its structure, recovering after context loss, or resolving conflicts between shared lifecycle and repository rules.
---

# Lean-SDLC Core

## Purpose

Keep the shared Lean-SDLC rules small and authoritative. Let specialized `lean-*` skills own their workflows.

Use this core when setting up or auditing a repository, recovering context, or resolving a shared contract. During ordinary scoped work, follow the repository's `AGENTS.md` and the active specialized skill.

## Non-Negotiables

1. Preserve `why -> what -> how -> prove/observe -> task -> artifact -> verification`.
2. Keep feature files as the main units of behavior truth.
3. Require scoped truth and a linked task with measurable acceptance before code.
4. Keep one intentional change per task.
5. Split features that hide independent outcomes or acceptance clusters.
6. Record durable chosen paths as decisions.
7. Keep runtime detail out of feature and decision files.
8. Define proof and failure signals before implementation.
9. Close work only when acceptance, evidence, documentation, and diagnostics agree.
10. Challenge unnecessary complexity and undocumented scope.

## Resume Order

1. Read `AGENTS.md`.
2. Read `docs/SCOPE.md`.
3. Read `docs/FEATURE_INDEX.csv` and `docs/DECISION_INDEX.csv`.
4. Read the relevant feature and decision files.
5. Read triggered technical docs only when they matter.
6. Read `planning/tasks.csv`.
7. Inspect code after the written chain is clear.

## Shared Resources

Open only the resource needed for the current job:

- [references/repo-contracts.md](./references/repo-contracts.md): repository files, schemas, and ownership rules.
- [references/lifecycle.md](./references/lifecycle.md): stage, version, and iteration changes.
- [assets/AGENTS.md](./assets/AGENTS.md): copy-ready repository control-plane template.
- [references/delegation.md](./references/delegation.md): model routing, delegation cost gates, and worker contracts.
- [references/skill-map.md](./references/skill-map.md): choose the smallest matching Lean-SDLC skill.

## Required Flow

1. Use `lean-brainstorm` or `lean-refine` before new scope or behavior work.
2. Use `lean-task-planning` before code.
3. Choose local or delegated execution deliberately.
4. Use `lean-debugging` for diagnosis and root-cause work.
5. Use `lean-implementation` only from an active task.
6. Use `lean-verification` before moving a task to `done`.
7. Use `lean-traceability` or `lean-doc-maintenance` when implementation may have caused drift.

## Change Routing

Choose one owner before editing:

- project value or success -> `PROJECT_BRIEF.md`
- temporary boundary or deferred scope -> `SCOPE.md`
- actor-facing behavior -> feature file
- durable chosen path -> decision file
- shared system shape -> `ARCHITECTURE.md`
- mappings and command tables -> `INTERFACES.md` or `docs/maps/*.md`
- implementation detail -> code and tests

Split a statement when it tries to live in multiple layers.

## Proof Gate

Before code, require:

1. measurable acceptance,
2. an explicit verification path,
3. useful diagnostics or failure signals.

Default to test-first when the behavior is cheap to test. Use another explicit proof path when full red/green TDD is awkward.

## Document Triggers

Create extra docs only under real pressure:

- `ARCHITECTURE.md` for meaningful shared boundaries or flows,
- `TEST_STRATEGY.md` or `DIAGNOSTICS.md` for shared policy,
- `INTERFACES.md` or `docs/maps/*.md` for shared bindings or mappings,
- domain, state, permissions, data, or risk docs only when project structure demands them,
- version history only when changed business context needs preservation.

## Outcome

Success means the repository remains small, traceable, provable, and recoverable after context loss.
