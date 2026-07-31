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
- deterministic lead, Executor, Researcher, Verifier, and Operator roles under one canonical policy;
- one named Luna Max custom-agent profile for child execution;
- a standard-library configurator that installs the profile and its multi-agent metadata;
- lead-directed execution with one durable task and one reviewed checkpoint at a time;
- independent Verifier proof and risk-based regression without blind repetition of Executor checks;
- read-only Researcher evidence collection for substantial multi-source or noisy inquiries;
- Operator-owned stateful operations with Verifier consumption of recorded evidence;
- applicable ASD-STE100 Issue 9 rules for generated English technical prose;
- learned project-specific operational procedures;
- minimal modular engineering, plausible edge-case treatment, and lightweight rendered diagrams;
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
- Never route reasoning below `high`.
- Preserve explicit user model and orchestration requests.
- Prefer deterministic depth-one delegation over agent hierarchies.
- Route primary Luna children through the named `lean_sdlc_luna` profile.
- Use direct Terra XHigh only when the Luna profile is unavailable, unexposed, or rejected.
- Apply ASD-STE100 sentence limits, active voice, consistent terms, condition-first instructions, and applicable spelling rules.
- Preserve exact code, commands, paths, identifiers, protocol fields, quotations, and required domain terms.
- Prefer cohesive replaceable units and earned boundaries over project-size architecture tiers.

## Success Criteria

- Codex reliably triggers Lean-SDLC when explicitly invoked or required by repository rules.
- A new repository needs only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- Task transactions remain atomic, owner-aware, dependency-valid, and cycle-free.
- Assisted, Focused, and Solo modes follow the same delivery gates.
- Assisted mode delegates each settled durable task beyond the direct fast path to one reusable Executor.
- The lead reviews every returned task checkpoint and Verifier checks each accepted checkpoint before another task begins.
- Spawned Luna agents use the named Max profile, Terra High is never routed, and children never inherit lead decision authority.
- Generated English technical prose follows applicable ASD-STE100 Issue 9 rules without unsupported certification claims.
- Changed contracts receive proportionate edge-case treatment and architecture remains modular without speculative seams.
- The plugin validates, installs from a pinned Git tag, and passes its full test suite.

## Current Promise

- Stage: Evolution
- Version: 1.4.0
- Version goal: Preserve lead decision authority while making named Luna Max execution, research, proof, and technical English controlled.
- Exit evidence: Tests, skill and plugin validation, local installation, repository checks, reviewed diff, tagged commit, and successful push.
