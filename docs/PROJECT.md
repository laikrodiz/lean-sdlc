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
- a human-monitorable ledger with durable `Context` values and labeled child reports;
- deterministic principal-engineer lead with Engineer, Maintainer, Verifier, and Researcher roles under one canonical policy;
- one lazily spawned child thread per role and lead Codex task, reused across repository tasks and inquiries;
- one named Luna Max custom-agent profile for child execution;
- a standard-library configurator that installs the profile and its multi-agent metadata;
- lead-directed execution with one durable task and one reviewed checkpoint at a time;
- independent Verifier proof and risk-based regression without blind repetition of Engineer checks;
- read-only Researcher evidence collection for substantial multi-source or noisy inquiries;
- Maintainer-owned stateful operations with Verifier consumption of recorded evidence;
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
- Keep discussion and proposal requests read-only until the user authorizes implementation explicitly or confirms proceeding against an agreed recoverable proposal.
- Apply the canonical Plan contract before task creation and implementation.
- Keep `tasks.csv` as the only durable task plan. Map each durable plan item to exactly one task, and keep implementation steps transient.
- Use `Context` values `Project`, `FEAT-*`, `DEC-*`, and `Bootstrap` for durable project truth.
- Require one concise natural lead assignment before every child handoff and one natural final update after child work. Keep required facts visible.
- Choose an unused simple human first name for each role when its thread starts. Display `Role Firstname` and use `role_firstname` as the task name. Keep the identity stable while the thread remains reusable. Require short child-task commentary at material phases while keeping lead reports compact.
- Require every user-facing lead message to start with outcome, work, or current state. Avoid repeated lead identity, model, mode, internal labels, greetings, praise, filler, and roleplay unless clarity requires them. Keep internal control data structured.
- Require children to call the primary agent Architect in visible commentary, handoffs, returns, and decision requests. The primary agent speaks as I. Keep lead for internal policy wording where useful.
- Have the lead identify the child when assignment clarity requires it. Require concise natural updates that state the assignment or inquiry, intended result, boundaries, acceptance, proof, checkpoint, and deviation. Do not require greetings, self-introductions, or sentence templates.
- Require a concise natural architecture brief before every Engineer handoff and a natural lead sign-off after every Engineer checkpoint. Keep internal handoffs and compact returns labeled and lossless.
- Report child phase changes sparsely and bound silent-command heartbeats to two at two-minute intervals.
- Do not send unbounded child progress updates.
- Keep `tasks.csv` private to each working copy.
- Never route reasoning below `high`.
- Preserve explicit user model and orchestration requests.
- Prefer deterministic depth-one delegation over agent hierarchies.
- Route primary Luna children through the named `lean_sdlc_luna` profile with Fast service mapped to `service_tier=priority`.
- Retry Luna Max without `service_tier` when priority is unavailable or rejected. Use direct Terra XHigh without `service_tier` only when Luna is unavailable.
- Apply ASD-STE100 sentence limits, active voice, consistent terms, condition-first instructions, and applicable spelling rules.
- Preserve exact code, commands, paths, identifiers, protocol fields, quotations, and required domain terms.
- Prefer cohesive replaceable units and earned boundaries over project-size architecture tiers.

## Success Criteria

- Codex reliably triggers Lean-SDLC when explicitly invoked or required by repository rules.
- A new repository needs only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- Task transactions remain atomic, owner-aware, dependency-valid, and cycle-free.
- Assisted mode uses every triggered role, including Engineer.
- Solo mode uses lead-only execution under the same delivery gates.
- Assisted and Solo are the only orchestration modes.
- Normal repository task transitions reuse existing role threads. Replacement keeps the role prefix and chooses another unused first name only when reset conditions apply. Names never use task identifiers, features, versions, descriptions, or counters.
- The lead reviews every returned task checkpoint and Verifier checks each accepted checkpoint before another task begins.
- Spawned Luna agents use the named profile and priority tier for Fast service, Terra High is never routed, and children never inherit Architect decision authority.
- Generated English technical prose follows applicable ASD-STE100 Issue 9 rules without unsupported certification claims.
- Changed contracts receive proportionate edge-case treatment and architecture remains modular without speculative seams.
- The plugin validates, installs from a pinned Git tag, and passes its full test suite.

## Current Promise

- Stage: Evolution
- Version: 1.8.2
- Version goal: Release intentional planning and human-monitorable children with visible plans and short material-phase commentary.
- Exit evidence: Tests, skill and plugin validation, local installation, accepted checkpoints, repository checks, tagged commit, and successful push.
