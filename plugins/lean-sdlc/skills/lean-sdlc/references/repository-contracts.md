# Repository Contract

Read this reference for initialization, legacy migration, or document ownership.

## Minimal core

An initialized project requires only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`. The initializer preserves existing files, adds `/tasks.csv` and `/.tasks.lock` to `.gitignore`, and closes `TASK-000` as owner `bootstrap` before the session restarts.

Optional documents appear only under durable shared pressure:

- `docs/features/FEAT-*.md` for behavior too detailed for `PROJECT.md`.
- `docs/decisions/DEC-*.md` for costly or easily forgotten choices.
- `docs/OPERATIONS.md` after the first guided build, package, deploy, flash, runtime, or smoke procedure.

README remains project-owned.

## Document ownership

- Project value, behavior boundary, scope, stage, and version promise -> `docs/PROJECT.md`.
- Durable behavior detail -> an optional feature document.
- Durable costly choice -> an optional decision document.
- Repeatable procedure -> `docs/OPERATIONS.md`.
- Shared mapping or interface -> technical documentation.
- Local mechanism -> code, tests, or comments.

Resolve conflicting truth in the authoritative source before synchronization.

## Visual explanations

Use a diagram only when flow, state, ownership, sequence, or dependencies become materially easier to understand. Prefer small Mermaid diagrams with one concept and a clear direction. Use tables for mappings and prose for simple relationships. Never use ASCII pseudographics. Code, contracts, and repository truth remain authoritative.

## Task ledger

Use exactly:

`Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence`

Use `Project`, `FEAT-*`, `DEC-*`, or `Bootstrap` as `Context`.

1. Use `tasks.py`; never edit the CSV directly.
2. `plan` creates unowned `Planned` work. `start` creates `In Progress` work or claims a planned task.
3. `update` requires the task owner for In Progress work.
4. `close` belongs to the owner after verification. A direct user request may override with a recorded reason.
5. Dependencies must exist, remain acyclic, and be `Done` before close.
6. Task transactions are the formal exception to task-before-write.

`tasks.py upgrade` accepts the previous `Parent` header and older planning header. It maps `REPO` to `Project` and `BOOTSTRAP` to `Bootstrap`, then atomically writes one root CSV under the existing lock.

The command serializes writers with a short root lock, reads the latest ledger under that lock, validates dependencies, changes one transaction, and replaces the file atomically. Owner IDs coordinate threads; they are not a security boundary.

## Work hierarchy

- Project promise: current outcome, scope, stage, and exit evidence.
- Feature: durable behavior that spans tasks.
- Task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.
- Local step: transient implementation or correction work that does not become a ledger row.

## Task sizing summary

Split or merge tasks by the independent boundaries in [plan.md](plan.md). Shape the nearest dependency frontier fully and keep later work coarse.
