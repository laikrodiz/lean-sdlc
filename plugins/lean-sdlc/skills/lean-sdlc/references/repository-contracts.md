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

- Project purpose, value, behavior boundary, scope, stage, and version promise -> `docs/PROJECT.md`.
- Durable behavior detail -> an optional Feature document.
- Technical rationale and durable costly choice -> an optional Decision document.
- Repeatable procedure -> `docs/OPERATIONS.md`.
- Shared mapping or interface -> technical documentation.
- Local corrections -> outcome-focused task truth, code, tests, or comments.
- Engineer owns code-local truth such as tests, comments, docstrings, annotations, and local examples.
- Maintainer owns shared narrative truth in `docs/PROJECT.md`, feature, decision, architecture, interface, README, and operations documents.
- The Architect supplies the behavior and decision delta. Maintainer synchronizes only affected documents through an impact-directed pass.

Keep durable intent in these existing owners. Do not add a file or task column for intent.

Resolve conflicting truth in the authoritative source before synchronization.

## Visual explanations

Use a diagram only when flow, state, ownership, sequence, or dependencies become materially easier to understand. Prefer small Mermaid diagrams with one concept and a clear direction. Use tables for mappings and prose for simple relationships. Never use ASCII pseudographics. Code, contracts, and repository truth remain authoritative.

## Task ledger

Use exactly:

`Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence`

Use `Project`, `FEAT-*`, `DEC-*`, or `Bootstrap` as `Context`.

Use `tasks.py open` for current `Planned` and `In Progress` work. Use `tasks.py show TASK-ID` for one task and its recursive dependencies. These read-only views keep the existing human-readable CSV shape and avoid loading full `Done` history. The human-readable `tasks.csv` remains authoritative.

1. Use `tasks.py`; never edit the CSV directly.
2. `plan` creates unowned `Planned` work. `start` creates `In Progress` work or claims a planned task.
3. `update` requires the task owner for In Progress work.
4. `close` belongs to the owner after verification. A direct user request may override with a recorded reason.
5. Dependencies must exist, remain acyclic, and be `Done` before start or close.
6. Task transactions are the formal exception to task-before-write.

`tasks.py upgrade` accepts the previous `Parent` header and older planning header. It maps `REPO` to `Project` and `BOOTSTRAP` to `Bootstrap`, then atomically writes one root CSV under the existing lock.

The command serializes writers with a short root lock for ledger updates, reads the latest ledger under that lock, validates dependencies, changes one transaction, and replaces the file atomically. The ledger lock is not a source-file lock. Owner IDs coordinate threads; they are not a security boundary.
One root `tasks.csv` remains authoritative. It may hold two ready tasks for one Architect owner after the resource gate passes. The Architect alone mutates or closes both rows.

## Work hierarchy

- Project promise: current outcome, scope, stage, and exit evidence.
- Feature: durable behavior that spans tasks.
- Task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.
- Local step: transient implementation or correction work that does not become a ledger row.

## Task sizing summary

Split or merge tasks by the independent boundaries in [plan.md](plan.md). Shape the nearest dependency frontier fully and keep later work coarse.
