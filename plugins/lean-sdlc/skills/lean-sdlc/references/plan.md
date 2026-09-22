# Plan and task shape

Before initial task creation or claiming, visibly restate the intended result, constraints, and authorized actions. Preserve detailed requirements; distinguish proposed additions. Read-only planning creates no ledger rows.

## Visible plan

After the intent restatement, always show all five fields:

- Outcome: who needs what improvement and why, using established context without invented business benefits.
- Work: independently accepted changes, grades, sequencing, and the chosen approach with its main reason.
- Acceptance: observable behavior and constraints that must hold for each result.
- Checks: evidence needed to establish acceptance, its limits, and who checks it.
- Limits: exclusions, unresolved choices, and operation authority.

Use short fields for small work; preserve necessary detail. Reuse settled context and decisions. Tables cannot replace the plan. Label material assumptions.

Compare the visible plan with every explicit user requirement; restore missing coverage before creating or claiming tasks. A plan-only request stops after the plan. Plan-and-implement proceeds without renewed approval unless a material choice remains unresolved. For new work or material scope changes, update intent and affected fields before tasks. Otherwise reuse the approved plan without reprinting it.

Before creating tasks or showing a task table, settle outcome boundaries and grades. One task has one independently accepted outcome, owning contract boundary, proof cluster, and close decision. For Complex candidates, distinguish combined scope from intrinsic difficulty or inseparable coupling. Split separately acceptable outcomes; grade the resulting tasks. Stop before implementation fragments or duplicated proof. Retain Complex when difficulty cannot usefully be separated; briefly explain why in Work. Resolve only uncertainty that could materially change boundaries. Revisit settled boundaries only when relevant facts change, not because Complex remains. Preserve the user outcome, real dependencies, and responsibility for combined-result proof. Splitting does not authorize parallel execution. Keep tests, documentation, and corrections with their outcome unless independently deliverable. Never split by file count, estimated time, agent availability, or a target grade.

## Grades

Assign Simple, Normal, or Complex to each task, not the project. Grades describe work complexity, not authority or safety.

- Simple: settled, bounded work with known paths and an immediate narrow check. Avoid routine Scout use and unnecessary broad tests.
- Normal: one understood behavior with several related implementation or verification steps.
- Complex: one coherent outcome with intrinsic uncertainty, difficult reasoning, or inseparable cross-boundary changes needing stronger proof.

Keep grades in plans, multi-task tables, and handoffs, not new columns or state files. Recover their basis after compaction.

## Ledger and visible status

Before new execution tasks, check compact Backlog and current-work views for duplicates or related work, never during ordinary conversation or startup. Adding or promoting ideas requires direct user authority; existing rows do not authorize execution.

Lead creates or claims work directly through [ledger](ledger.md). Confirm owned In Progress status, acceptance, proof, and the before-write gate before implementation. Dependencies must be Done before dependent work starts. All roles may read task facts.

Name tasks by their intended change. Use real IDs and exact titles, never invented proposal IDs. After confirmed creation and ownership, announce each task:

> Starting <real task ID>: <exact title>.
> Optimal process: <actual execution, support work, and wait or continue relationship>.

List only needed roles and steps, without a separate assessment stage. Repeat the process only when it changes. This can satisfy the [support announcement](../protocols/common.md).

For one task, replace the table with this announcement and short status-change and final-state lines. For multiple tasks, use these overview columns:

| Task ID | Short description | Grade | Status |
| --- | --- | --- | --- |

The full table covers the current authorized work, not unrelated history or stopped tasks.

- Beginning: for multiple tasks, show the full table after creation and confirmed ownership, before implementation. The first task is In Progress; report blocked prerequisites instead of announcing a blocked task as started.
- Middle: show one changed task as a short status line, or simultaneous changes as changed rows only. Identify newly authorized scope.
- End: for multiple tasks, show the full table with actual final states after ledger reconciliation. If work stops, show the unfinished states. Do not force stopped or blocked work to Done.

After accepting required proof, close the task directly through the helper, confirm success, and show Done. Report transaction failures immediately; never present pending or failed writes as confirmed state. Pause affected work, but continue independent ready work. Confirm IDs, ownership, and write prerequisites; never bypass dependencies.

If `update_plan` is available, mirror each unresolved task there as `TASK-NNN — Title`. Map Planned to `pending`, In Progress to `in_progress`, and Done to `completed`. Rebuild unresolved rows after resume. The ledger remains authoritative; the native view is optional.

## Simple tasks and deferred review

Eligible Simple tasks use the existing `Quick Fix` context and pending-review markers. This is a review classification, not another workflow. Eligibility requires an exact reversible result, settled boundaries, and one useful immediate proof. Use Normal or Complex when architecture, interfaces, migration, security, permissions, or other material choices remain unresolved.

Lead implements, writes any necessary test, and can run the immediate essential check directly. Use Verifier when the required proof needs independent review, not merely because a test exists. Once the artifact, immediate essential proof, and required safety or usage instructions are ready, the user can test the result.

Broader regression and documentation/interaction reviews may wait for a shared checkpoint. A task may be Done with that review explicitly pending; do not call it fully reviewed. At the next shared checkpoint, and before release, Verifier covers the pending range. Lead records `--review-through TASK-ID` only after accepting the review and only for a valid Done prefix. A failed shared review needs an owned correction.

Never defer essential validation, a known documentation defect, or safety proof. Do not add mandatory tests for a purely cosmetic change when an immediate inspection supplies the necessary evidence.
