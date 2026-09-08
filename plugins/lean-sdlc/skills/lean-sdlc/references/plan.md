# Plan and task shape

Before task creation, restate the user's intended outcome, relevant constraints, and implementation authority. Read-only planning creates no ledger rows. A request to plan and implement uses this same coverage, then proceeds without another approval round.

## Visible plan

Use these five fields:

- Outcome: the observable result and why it matters.
- Work: independently accepted changes, their grades, and real sequencing.
- Acceptance: what must be true for each result.
- Checks: how Verifier will establish those facts.
- Limits: exclusions, unresolved choices, and operation authority.

Keep a small plan small. Necessary facts matter more than word count. Preserve all explicit user requirements. Label proposed additions and material assumptions rather than silently making them requirements.

Before asking Maintainer to create tasks, Lead reviews atomicity. One task has one independently accepted outcome, owning contract boundary, proof cluster, and close decision. Split when parts can succeed, fail, defer, revert, or be accepted independently. Do not split by file count, estimated time, or agent availability. Keep tests, documentation, and corrections with their owning outcome unless independently deliverable. Local implementation steps remain transient.

## Grades

Assign Simple, Normal, or Complex to each task, not the project. Grades describe work complexity, not authority or safety.

- Simple: settled, bounded work with known paths and an immediate narrow check. Avoid routine Scout use and unnecessary broad tests.
- Normal: one understood behavior with several related implementation or verification steps.
- Complex: uncertain or cross-boundary work needing a reading map, explicit decisions, or stronger integration proof.

Keep grades in the visible table and handoffs, not a CSV column or new state file. Recover their basis after compaction; reassess when facts change.

## Ledger and visible status

Before new execution tasks, use compact Backlog and current-work views to check duplicates or related work. Do not load Backlog during ordinary conversation or startup. Only direct user authority permits adding or promoting an idea. An existing row does not authorize execution.

Maintainer creates or claims work through [ledger](ledger.md). Lead confirms owned In Progress status, acceptance, proof, and the before-write gate before implementation. Dependencies must be Done before dependent work starts. All roles may read task facts.

Show this table after creation and material status, scope, or task-boundary changes:

| Task ID | Short description | Grade | Status |
| --- | --- | --- | --- |

Use real IDs and exact task titles. Never invent IDs for a proposal. If `update_plan` is available, mirror each unresolved task there as `TASK-NNN — Title`. Map Planned to `pending`, In Progress to `in_progress`, and accepted closure to `completed`. Rebuild unresolved rows after resume. The ledger remains authoritative; the native view is optional.

Lead may update visible status when requesting a normal transaction. Maintainer reports failures immediately. Confirm prerequisites before depending on them and reconcile the table against actual rows before final completion. Keep unrelated stopped tasks separate; do not silently resume or close them.

## Simple tasks and deferred review

Eligible Simple tasks use the existing `Quick Fix` context and pending-review markers. This is a review classification, not another workflow. Eligibility requires an exact reversible result, settled boundaries, and one useful immediate proof. Use Normal or Complex when architecture, interfaces, migration, security, permissions, or other material choices remain unresolved.

Lead implements and writes any necessary test. Verifier runs the immediate essential check. Once the artifact and required safety or usage instructions are ready, the user can test the result.

Broader regression and documentation/interaction reviews may wait for a shared checkpoint. A task may be Done with that review explicitly pending; do not call it fully reviewed. At the next shared checkpoint, and before release, Verifier covers the pending range. Maintainer records `--review-through TASK-ID` only after Lead acceptance and only for a valid Done prefix. A failed shared review needs an owned correction.

Never defer essential validation, a known documentation defect, or safety proof. Do not add mandatory tests for a purely cosmetic change when an immediate inspection supplies the necessary evidence.
