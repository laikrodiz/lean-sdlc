# Repository Contract

Read this reference for initialization, legacy migration, or document ownership.

## Minimal core

An initialized project requires only `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`. The initializer preserves existing files, adds `/tasks.csv` and `/.tasks.lock` to `.gitignore`, and closes `TASK-000` as owner `bootstrap` before the session restarts.

`docs/PROJECT.md` remains the only mandatory shared project document. `AGENTS.md` and root `tasks.csv` remain required repository files. README remains project-owned.

Optional documents appear only when a concrete need-based trigger exists. Use semantic sizing: one document holds one cohesive meaning, not an arbitrary line or time limit.

- `docs/features/FEAT-*.md` for one durable behavior too detailed for `PROJECT.md`.
- `docs/decisions/DEC-*.md` for one costly or easily forgotten choice.
- `docs/architecture/ARCH-*.md` for one shared system shape or boundary.
- `docs/state-machines/STATE-*.md` for one named lifecycle with meaningful transitions.
- `docs/interfaces/IFACE-*.md` for one shared or external contract.
- `docs/data/DATA-*.md` for one shared data model or lifecycle.
- `docs/operations/OPS-*.md` for one repeatable procedure that needs durable detail.
- `docs/ARCHITECTURE.md` and `docs/OPERATIONS.md` remain conditional overview documents.
- `docs/SECURITY.md`, `docs/GLOSSARY.md`, and `docs/VERIFICATION.md` remain conditional documents.

Create a family only when its trigger is present. Name each document `PREFIX-NNN-slug.md`, and never reuse an ID. Create `INDEX.md` with the first numbered document. Use the columns `ID`, `Title`, `Status`, `Owns`, and `Related`. List every current numbered document exactly once. The index is navigation, not specification.

Size a document by one independent outcome, reversal boundary, system shape, lifecycle, contract, model, or procedure. Split when outcomes, owners, acceptance clusters, change reasons, or update cadences differ. Merge when neither part has independent value, proof, or maintenance pressure. Do not create a numbered document for a task note, local implementation detail, or transient diagnosis.

### Conditional documents

Create `docs/ARCHITECTURE.md` when responsibilities or data flow are non-obvious and need one system overview. Keep one subsystem needing independent detail in a numbered architecture document.

Create `docs/OPERATIONS.md` after the first guided build, package, deploy, flash, runtime, or smoke procedure, or after the first approved and recorded automation. It owns the first simple recorded procedure, automation catalog, and shared operation map. Use a numbered operation document when a procedure has an independent target, recovery rule, lifecycle, or useful standalone detail.

Create `docs/SECURITY.md` when security boundaries or controls span more than one document or need a shared review gate. Create `docs/GLOSSARY.md` when repeated terms create material ambiguity. Create `docs/VERIFICATION.md` when proof rules span several tasks or document families. Do not create any of these for a single local note.

### Source archives

Normal replacement deletes old code and relies on Git. Do not create an archive for normal replacement.

Create repository-root `archive/` only after an explicit user request. Store each snapshot at `archive/<capability>/<snapshot>/ARCHIVE.md`. Require `archive/INDEX.md` when `archive/` exists. A source archive is inert and excluded from active imports, builds, packaging, and normal tests. Keep only source, focused tests, fixtures, small configuration, and notes needed to understand or restore the snapshot. Do not archive build output, installed dependencies, caches, credentials, or unrelated files.

Do not create a documentation archive policy beyond optional supporting copies inside a source snapshot.

## Document ownership

- Project purpose, value, behavior boundary, scope, stage, and version promise -> `docs/PROJECT.md`.
- Durable behavior detail -> an optional Feature document.
- Technical rationale and durable costly choice -> an optional Decision document.
- System responsibility and flow -> conditional `docs/ARCHITECTURE.md`; independent subsystem detail -> an optional Architecture document.
- State transitions -> an optional State Machine document.
- Shared or external contract -> an optional Interface document.
- Persistent or exchanged data contract -> an optional Data document.
- Simple recorded procedure, automation catalog, and operation map -> conditional `docs/OPERATIONS.md`; independent procedure -> an optional Operation document.
- Shared trust boundaries, terminology, or manual proof -> conditional Security, Glossary, or Verification documents.
- Local corrections -> outcome-focused task truth, code, tests, or comments.
- Engineer owns code-local truth such as tests, comments, docstrings, annotations, and local examples.
- Maintainer owns shared narrative truth in project, feature, decision, architecture, state-machine, interface, data, operations, security, glossary, verification, and README documents.
- Maintainer owns each collection `INDEX.md` and synchronizes shared narrative truth through an impact-directed pass.
- Maintainer owns `archive/INDEX.md` and each snapshot `ARCHIVE.md` after the Architect approves an explicit archive request and boundary.
- Maintainer detects a missing trigger, stale document, stale automation, or oversized semantic unit. Maintainer never invents product or architecture.
- The Architect supplies the behavior and decision delta and approves meaning and document splits. Maintainer synchronizes only affected documents through an impact-directed pass.

Keep durable intent in these existing owners. Do not add a file or task column for intent.

Recorded operations are the only automation catalog. Do not add another automation file, registry, hook, state field, role, mode, dependency, or runtime framework.

Resolve conflicting truth in the authoritative source before synchronization.

## Visual explanations

Use a diagram only when flow, state, ownership, sequence, or dependencies become materially easier to understand. Prefer small Mermaid diagrams with one concept and a clear direction. Use tables for mappings and prose for simple relationships. Never use ASCII pseudographics. Code, contracts, and repository truth remain authoritative.

## Task ledger

Use exactly:

`Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence`

Use `Project`, `FEAT-*`, `DEC-*`, `Bootstrap`, or `Quick Fix` as `Context` for active work. A Backlog row defaults to `Project` context.

Use `tasks.py backlog` for the compact Backlog view. Use `tasks.py open` for current `Planned` and `In Progress` work. Use `tasks.py show TASK-ID` for one task and its recursive dependencies. These read-only views keep the existing human-readable CSV shape and avoid loading full `Done` history. The human-readable `tasks.csv` remains authoritative.

### Backlog contract

A Backlog row has Status `Backlog` and carries values only for `Task ID`, `Title`, `Status`, and `Context`. `Dependencies`, `Owner`, `Acceptance Criteria`, `Proof`, and `Evidence` stay empty. The default Context is `Project`; `Bootstrap` and `Quick Fix` are invalid Backlog contexts. No task may depend on a Backlog task.

`tasks.py backlog-add` adds a sparse Backlog row. `tasks.py backlog` prints the compact Backlog view. `tasks.py promote` promotes a Backlog idea through Shape and Plan, not through a raw status flip. Title and context correction changes only those Backlog fields and keeps the row sparse.

Only a direct user request may add or promote Backlog work. An Architect may propose Backlog placement only for a substantial reason and must wait for approval. A clear implementation request matching an existing Backlog title is promotion authority without an exact ID. Before creating new Standard work, the Architect reads `tasks.py backlog` and checks duplicates, broader items, or related ideas. Do not load Backlog on startup, resume, brainstorming, or Quick Fix work.

Promotion adds proper title sizing, acceptance, proof, and dependencies. Promotion to In Progress adds an owner and requires explicit implementation authority. Planned promotion is not implementation authority. If a Backlog idea is broad, promote the original ID as the first coherent task and create sibling tasks for independent outcomes. A Feature document remains optional under its existing trigger.

1. Use `tasks.py`; never edit the CSV directly.
2. `plan` creates unowned `Planned` work. `start` creates `In Progress` work or claims a planned task.
3. `update` requires the task owner for In Progress work.
4. `close` belongs to the owner after verification. A direct user request may override with a recorded reason.
5. Dependencies must exist, remain acyclic, and be `Done` before start or close.
6. Task transactions are the formal exception to task-before-write.

`tasks.py upgrade` accepts the previous `Parent` header and older planning header. It maps `REPO` to `Project` and `BOOTSTRAP` to `Bootstrap`, then atomically writes one root CSV under the existing lock.

The command serializes writers with a short root lock for ledger updates, reads the latest ledger under that lock, validates dependencies, changes one transaction, and replaces the file atomically. The ledger lock is not a source-file lock. Owner IDs coordinate threads; they are not a security boundary.
One root `tasks.csv` remains authoritative. It may hold two ready tasks for one Architect owner after the resource gate passes. The Architect alone mutates or closes both rows.

## Quick Fix ledger

Quick Fix is an inline Plan classification. It is not a new task type. Closing a Quick Fix records pending broad batch review. `tasks.py quick-fixes` lists completed Quick Fixes that remain unreviewed.

A Standard checkpoint reviews every pending Quick Fix through the highest listed task in Verifier regression and documentation/interaction review. Close that checkpoint with `--review-through TASK-NNN`. The review prefix must contain only `Done` Quick Fix tasks through the target. Invalid review references fail without ledger mutation.

A request with several Quick Fixes may defer broad checks until one shared checkpoint. A standalone Quick Fix may remain pending until a later Standard checkpoint. A failed shared review creates a Standard correction task. Deferred Quick Fix assurance is not automatic technical debt.

## Work hierarchy

- Project promise: current outcome, scope, stage, and exit evidence.
- Feature: durable behavior that spans tasks.
- Task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.
- Local step: transient implementation or correction work that does not become a ledger row.

## Task sizing summary

Split or merge tasks by the independent boundaries in [plan.md](plan.md). Shape the nearest dependency frontier fully and keep later work coarse.
