# Lean-SDLC Skill Map

Use the smallest skill that matches the current job.

Preferred sequence:

- new scope or new behavior truth -> `lean-brainstorm` or `lean-refine`
- approved truth -> `lean-task-planning`
- ready task set -> `lean-execution`
- bug or fix investigation -> `lean-debugging`
- active task -> `lean-implementation`
- task closeout -> `lean-verification`
- drift after implementation or debugging -> `lean-traceability` or `lean-doc-maintenance`

- `lean-sdlc-core`
  Use when the repo needs overall lifecycle rules, repo shape, triggers, or routing.
- `lean-brainstorm`
  Use when starting from a rough idea and no stable project truth exists yet.
- `lean-refine`
  Use when scope, features, decisions, proof, diagnostics, or cross-cutting constraints are still ambiguous.
- `lean-architecture`
  Use when the project needs stack choice, major boundaries, architecture notes, or decisions.
- `lean-task-planning`
  Use when approved feature or decision work must become atomic tasks.
- `lean-execution`
  Use when ready tasks must be dispatched locally, to workers, or in a checkpointed batch.
- `lean-debugging`
  Use when a failing behavior must be reproduced, isolated, and classified before deciding whether docs or code should change.
- `lean-implementation`
  Use when coding against already-scoped tasks.
- `lean-verification`
  Use when proving acceptance, checking tests, or deciding whether a task can close.
- `lean-traceability`
  Use when links between brief, scope, features, decisions, tasks, and artifacts need repair.
- `lean-versioning`
  Use when the project is stuck in stale stage or version framing.
- `lean-doc-maintenance`
  Use when documentation drift, file growth, or stale planning artifacts need cleanup.

## Companion Skills

- `cad`
  Use for script-driven CAD generation, inspection, and validation. It supports CAD artifacts inside a project, while Lean-SDLC still owns scope, decisions, tasks, proof, and documentation parity.
