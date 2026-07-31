# Repository Contract

## Minimal core

An initialized Lean-SDLC project requires only:

- `AGENTS.md`
- `docs/PROJECT.md`
- root `tasks.csv`

The initializer creates missing control files without replacing project work. It creates or extends `.gitignore` with `/tasks.csv` and `/.tasks.lock`; the checker enforces both entries. Verify the result, close `TASK-000` as owner `bootstrap`, then restart or resume Codex so the scoped plugin hook supplies the stable numeric owner.

Optional documents appear only under durable shared pressure:

- `docs/features/FEAT-*.md` for behavior too detailed for `PROJECT.md`;
- `docs/decisions/DEC-*.md` for costly or easily forgotten choices;
- `docs/OPERATIONS.md` after the first guided build, package, deploy, flash, runtime, or smoke procedure succeeds;
- other technical documentation when several code locations need one stable mapping or interface.

README remains project-owned.

## Project truth

Keep `docs/PROJECT.md` short:

- problem and user;
- intended outcome and value;
- in-scope and deferred boundaries;
- constraints and assumptions;
- observable success;
- current stage, version promise, and exit evidence.

Put implementation mechanisms in code, tests, or technical docs. Put repeatable operational procedures in `docs/OPERATIONS.md`.

## Visual explanations

Use a diagram only when flow, state, ownership, sequence, or dependencies become materially easier to understand. Prefer small Mermaid diagrams with one concept, short labels, a clear direction, and minimal semantic accents. Split dense views; use tables for mappings and prose for simple relationships. Never use ASCII pseudographics. Code, contracts, and repository truth remain authoritative.

## Task ledger

Use exactly:

`Task ID,Title,Status,Parent,Dependencies,Owner,Acceptance Criteria,Proof,Evidence`

Rules:

1. Use `tasks.py`; never edit the CSV directly.
2. `plan` creates unowned `Planned` work.
3. `start` creates immediate `In Progress` work; `start TASK-ID` claims Planned work.
4. `update` may correct Planned work without an owner and In Progress work only as its owner.
5. `close` belongs to the owner after verification. A direct user request may override with a recorded reason.
6. Separate dependencies with spaces, semicolons, or quoted commas. Every dependency must exist, cycles are invalid, and dependencies must be Done before close.
7. Use `REPO` unless a durable `FEAT-*` or `DEC-*` document owns the change. An active task may reserve the document it creates. Use `BOOTSTRAP` once.
8. Task transactions are the formal exception to task-before-write.

The command serializes writers with a short root lock, reads the latest ledger under that lock, validates dependencies, changes one transaction, and replaces the file atomically. Owner IDs coordinate threads; they are not a security boundary.

## Ownership

- project value, behavior boundary, scope, stage, or version promise -> `docs/PROJECT.md`
- durable behavior detail -> optional feature document
- durable costly choice -> optional decision document
- repeatable build or target procedure -> optional `docs/OPERATIONS.md`
- shared technical mapping or interface -> technical documentation
- local mechanism -> code, tests, or comments

Split statements until one owner wins. Reconcile conflicting truth before closeout.

## Work hierarchy

- Project promise: current outcome, scope, stage, and exit evidence.
- Feature: durable behavior that spans tasks.
- Task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.
- Local step: transient implementation or correction work that does not become a ledger row.

## Task sizing summary

Split or merge tasks by the independent boundaries in [plan.md](plan.md).
Shape the nearest dependency frontier fully and keep later work coarse.
