# Lean-SDLC Repository Contracts

## Minimal Core

An initialized project uses:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_BRIEF.md`
- `docs/SCOPE.md`
- `docs/FEATURE_INDEX.csv`
- `docs/DECISION_INDEX.csv`
- `docs/features/FEAT-xxx-*.md` when features exist
- `docs/decisions/DEC-xxx-*.md` when decisions exist
- `planning/tasks.csv`

Use [../assets/AGENTS.md](../assets/AGENTS.md) as the project control plane. Run `scripts/init_repo.py [repository]` to create missing control files without overwriting existing work.

## Project Brief and Scope

Keep `PROJECT_BRIEF.md` short: problem, target user, intended outcome, value, constraints, non-goals, and success criteria.

Use `SCOPE.md` for in/out boundaries, assumptions, known limitations, deferred ideas, current stage, current version, version goal, version exit criteria, and stage exit criteria.

## Indexes

Use these `FEATURE_INDEX.csv` columns:

`feature_id,name,status,actor,outcome,value_summary,file,version,notes`

Use these `DECISION_INDEX.csv` columns:

`decision_id,name,status,type,impact_scope,reversal_cost,scope_ref,file,date,notes`

Indexes are mechanical pointers. Keep full truth in the referenced files.

## Feature Files

Each feature records its id, name, status, reason/value, business context, behavior, constraints, exclusions, acceptance criteria, verification approach, diagnostics/failure signals, related decisions, and related tasks.

One feature represents one independently valuable and deferrable actor outcome. Split when it contains distinct outcomes, actor goals, acceptance clusters, repeated "and also" behavior, or independently deliverable parts.

## Decision Files

Each decision records its id, name, status, type, context, decision, consequences, related features, related tasks, and related docs.

Create a decision for a durable chosen path that is costly to reverse or easy to forget. Keep recipes, debug notes, helper names, and volatile tuning in lower technical docs, code, or tests.

## Task Ledger

Use these `planning/tasks.csv` columns:

`task_id,title,status,parent_ref,depends_on,acceptance`

Allowed statuses are `planned`, `in_progress`, and `done`.

Rules:

1. Insert new tasks directly below the header.
2. Keep one intentional change per task.
3. Link every task to one feature or decision.
4. Define measurable acceptance before implementation.
5. Keep the task open until evidence and documentation parity exist.
6. State status transitions explicitly.

## Change Ownership

- project why or success → `PROJECT_BRIEF.md`
- temporary boundary or deferred scope → `SCOPE.md`
- actor-facing behavior → feature file
- durable chosen path → decision file
- shared system shape → `ARCHITECTURE.md`
- mappings, commands, file layouts, or protocol fields → `INTERFACES.md` or `docs/maps/*.md`
- local mechanism → code, tests, or comments

Split a statement when it fits several owners. Create optional technical docs only when repeated shared pressure justifies them.
