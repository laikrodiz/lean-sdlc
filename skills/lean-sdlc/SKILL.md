---
name: lean-sdlc
description: Route and run Lean-SDLC for software project discovery, requirements refinement, architecture, task planning, execution, debugging, implementation, verification, traceability, versioning, and documentation maintenance. Use whenever the user says Lean-SDLC; asks to initialize, audit, continue, resume, plan, debug, implement, or close work in a Lean-SDLC repository; requests any repository file mutation; or when repository AGENTS.md requires Lean-SDLC routing. Select one primary workflow from repository state and load only its reference. Use the fast path only for read-only explanation and inspection; every repository mutation requires an active task.
---

# Lean-SDLC

Keep software work linked from intent through evidence without turning documentation into a second product.

## Start

1. Read repository `AGENTS.md` when present.
2. Identify the user's requested outcome and whether the work changes behavior, durable decisions, code, or completion state.
3. If any repository file may change, find or create its task before the first write.
4. Inspect only enough project truth to select one primary workflow.
5. Open the matching workflow reference below and follow it.
6. State the selected lane briefly when it affects what happens next.

For a new or unadapted repository, read [references/repository-contracts.md](references/repository-contracts.md), then use [scripts/init_repo.py](scripts/init_repo.py) for the atomic bootstrap exception. It creates the task ledger and authorizing bootstrap row in one control operation, then creates missing control files without overwriting existing work.

## Route One Primary Lane

| Repository state or request | Primary lane | Instructions |
| --- | --- | --- |
| Rough idea; brief or scope missing | brainstorm | [references/brainstorm.md](references/brainstorm.md) |
| New behavior, fuzzy scope, contradictions, or oversized features | refine | [references/refine.md](references/refine.md) |
| Stable behavior needs technical choices or boundaries | architecture | [references/architecture.md](references/architecture.md) |
| Approved repository mutation lacks an active task, or approved feature or decision lacks executable tasks | task planning | [references/task-planning.md](references/task-planning.md) |
| Ready tasks need local, delegated, or batch selection | execution | [references/execution.md](references/execution.md) |
| Failure exists and its cause is uncertain | debugging | [references/debugging.md](references/debugging.md) |
| Cause and scope are known; an approved task is ready | implementation | [references/implementation.md](references/implementation.md) |
| Work claims completion or a task may close | verification | [references/verification.md](references/verification.md) |
| Sources disagree or ownership/linkage is uncertain | traceability | [references/traceability.md](references/traceability.md) |
| Stage, version promise, or exit criteria no longer fit | versioning | [references/versioning.md](references/versioning.md) |
| Correct truth is known and approved docs need cleanup or propagation | documentation maintenance | [references/doc-maintenance.md](references/doc-maintenance.md) |

Choose the earliest unresolved lane. Do not mechanically run every lane. End by naming the next lane only when another step is actually required.

## Hard Gates

1. Do not mutate any repository file without one active task owned by the writer. The atomic insertion of that authorizing task row is the only routine pre-task write.
2. Use a feature, decision, `REPO`, or one-time `BOOTSTRAP` parent appropriate to the change.
3. Do not implement without measurable acceptance and an explicit proof path.
4. Route unknown causes through debugging before implementation.
5. Do not move work to `done` without evidence and documentation parity.
6. Reconcile conflicting truth before closeout.

Use the fast path only for read-only explanation and inspection. Create a small `REPO` task even for a trivial maintenance write.

## Shared References

Open only what the active lane needs:

- [references/repository-contracts.md](references/repository-contracts.md): files, schemas, ownership, and abstraction rules.
- [references/lifecycle.md](references/lifecycle.md): stage, version, and iteration framing.
- [references/model-routing.md](references/model-routing.md): model choice and user-selected model authority.
- [references/agent-coordination.md](references/agent-coordination.md): delegation, reuse, handoffs, cache discipline, and integration.
- [assets/AGENTS.md](assets/AGENTS.md): concise repository control-plane template.
- [references/trigger-evals.md](references/trigger-evals.md): maintainer cases for checking routing reliability.

Run [scripts/lean_check.py](scripts/lean_check.py) with `--before-write --task TASK-ID` before the first mutation, then run it again before closeout. Treat it as a structural check; semantic acceptance and evidence still require judgment.

## Outcome

Leave one coherent chain:

`why -> scope -> behavior/decision -> task -> implementation -> proof`
