# Lean-SDLC AGENTS Template

Keep `AGENTS.md` short. It is the repo control plane, not a knowledge base.

## 1. Authority Order

1. `docs/PROJECT_BRIEF.md`
2. `docs/SCOPE.md`
3. feature files
4. decision files
5. `docs/ARCHITECTURE.md`
6. `planning/tasks.csv`
7. current codebase reality

If docs and code disagree, flag it and reconcile it explicitly.

## 2. Reading Order

1. Read `AGENTS.md`.
2. Read `docs/SCOPE.md`.
3. Read `docs/FEATURE_INDEX.csv` and `docs/DECISION_INDEX.csv`.
4. Read the relevant feature and decision files.
5. Read `docs/ARCHITECTURE.md` and other triggered docs only if they matter.
6. Read `planning/tasks.csv`.
7. Inspect code only after the written chain is clear.

## 3. Change Routing

Exactly one owner should win before any doc or code edit:

- project why, success, and core value -> `docs/PROJECT_BRIEF.md`
- temporary boundary, phase limit, prototype constraint, deferred idea -> `docs/SCOPE.md`
- actor-facing behavior and outcome -> feature file
- durable chosen path with lasting consequences -> decision file
- system shape, boundaries, and shared flows -> `docs/ARCHITECTURE.md`
- hardware mappings, channel numbers, route tables, file names, runtime commands, protocol field maps -> `docs/INTERFACES.md` or `docs/maps/*.md`
- low-level mechanism, algorithm detail, queue behavior, filtering steps, worker logic, and local wiring -> code, tests, or code comments unless broadly shared

If a statement fits two owners, split it until one owner wins.

## 4. Required Sequence

Use this order unless the repo is only being read:

1. `lean-brainstorm` or `lean-refine` before new scope, new behavior, or parent-doc changes
2. `lean-task-planning` before code
3. Choose execution mode: local, delegated, or batch
4. `lean-debugging` when the work is diagnosis or a fix investigation
5. `lean-implementation` only from an active task
6. `lean-verification` before any task moves to `done`
7. `lean-traceability` or `lean-doc-maintenance` after implementation bursts, debug bursts, or drift discovery

## 5. Approval Checkpoints

1. Feature and decision truth must be clean before task planning.
2. Tasks must be clean before execution mode is chosen.
3. Tasks must be clean before implementation.
4. Verification, traceability, and doc parity must be clean before `done`.
5. Debugging work must classify the root cause before code is treated as the answer.

## 6. Before Task Creation

1. Check feature fit.
2. Split or create a feature if the change does not fit one feature exactly.
3. Check whether the work also needs a decision.
4. Create the task only after parent docs are clean.
5. Insert new tasks at the top of `planning/tasks.csv`.

## 7. Before Code

1. Task exists.
2. Clear, measurable acceptance exists.
3. Parent feature or decision is at the right abstraction level.
4. Task status is explicitly moved to `in_progress` when work begins.
5. Proof is defined first, with test-first by default when practical.

## 8. Execution Mode

1. Use local execution for one critical-path task.
2. Delegate substantial disjoint tasks only when parallel work saves meaningful time or main-agent context.
3. Use `gpt-5.6-sol` at `low` for decisions; raise effort only for material ambiguity or risk.
4. Use `gpt-5.6-luna` at `xhigh` for bounded implementation with exact ownership, acceptance, and proof.
5. Use Luna at `low` for mechanical inventory and summaries.
6. Use `gpt-5.6-terra` at the same effort when Luna is unavailable. Never fall back below GPT-5.6 or below `low` effort silently.
7. Give delegates the smallest useful context and require concise evidence-based returns.

## 9. Before Done

1. Acceptance is fully met.
2. Evidence exists.
3. Diagnostics are present where promised.
4. Feature and decision docs still match the new truth.
5. Wrong-level detail has been pushed down into the right doc or code location.
6. Task status is explicitly moved to `done`.

## 10. Debug Path

When debugging:

1. Reproduce first.
2. Isolate the failing path.
3. Classify the problem as behavior, decision, mapping, boundary, or implementation detail.
4. Update docs only if durable truth changed.
5. Keep transient debug detail out of feature and decision files.

## 11. Review Path

After meaningful implementation or debugging bursts:

1. Run verification.
2. Run traceability if parent truth or abstraction may have drifted.
3. Run doc maintenance if stale or misrouted detail remains.

## 12. Stop Conditions

Stop and repair docs before continuing when:

- a feature reads like a subsystem, capability area, or roadmap bucket
- a decision reads like an implementation recipe
- prototype or hardware mapping leaks into feature or decision truth
- a code change would outrun its parent docs
- a task has no exact parent feature or decision

## 13. Triggered Docs

Create extra docs only when pressure is real:

- `docs/ARCHITECTURE.md` for shared system shape
- `docs/INTERFACES.md` for shared contracts
- `docs/maps/*.md` for volatile or dense mapping truth
- other optional docs only when the project clearly needs them
