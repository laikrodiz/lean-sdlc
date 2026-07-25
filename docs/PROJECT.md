# Project

## Problem and User

Codex repository work can drift from user intent, lose ownership across tasks, or claim completion without useful proof. Existing process frameworks often add more ceremony and context cost than the work justifies.

The project serves people who want Codex to keep a software repository organized and accountable without requiring them to operate a heavyweight development system.

## Intended Outcome and Value

Provide one simple, shareable Codex plugin that routes work through the smallest relevant delivery lane, preserves a readable task overview, uses agents conservatively, and closes work only with evidence.

## Scope

### In

- one Lean-SDLC dispatcher skill;
- minimal repository initialization and migration;
- atomic private task-ledger transactions;
- controlled lead, sidecar, and temporary-agent roles;
- learned project-specific operational procedures;
- structural validation, tests, packaging, and installation guidance.

### Out or Deferred

- a hosted task service or replacement issue tracker;
- mandatory feature, decision, architecture, or operations documents;
- CI enforcement, dashboards, telemetry, or cache accounting;
- project-specific build, deploy, or flash recipes inside the generic plugin.

## Constraints and Assumptions

- Use shell and Python standard library only.
- Keep task state human-readable and safe for concurrent Codex tasks.
- Keep `tasks.csv` private to each working copy.
- Never route reasoning below `medium`.
- Preserve explicit user model and orchestration requests.
- Prefer deterministic depth-one delegation over agent hierarchies.

## Success Criteria

- Codex reliably triggers Lean-SDLC when explicitly invoked or required by repository rules.
- A new repository needs only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- Task transactions remain atomic, owner-aware, dependency-valid, and cycle-free.
- Assisted, Focused, and Solo modes follow the same delivery gates.
- The plugin validates, installs from a pinned Git tag, and passes its full test suite.

## Current Promise

- Stage: Evolution
- Version: 1.0.0
- Version goal: Ship the simplified plugin, six-lane workflow, controlled multi-agent strategy, and root task ledger.
- Exit evidence: Tests, skill and plugin validation, local installation, repository checks, reviewed diff, tagged commit, and successful push.
