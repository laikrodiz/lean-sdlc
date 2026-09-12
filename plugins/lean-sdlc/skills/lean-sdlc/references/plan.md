# Plan and task shape

Before creating or claiming the initial task set, visibly restate the user's intended result, important constraints, and authorized actions. Preserve the substance of a detailed request; a generic summary is not enough. Distinguish user requirements from proposed additions. Read-only planning creates no ledger rows.

## Visible plan

After the intent restatement, always show all five fields:

- Outcome: the observable result and why it matters.
- Work: independently accepted changes, their grades, and real sequencing.
- Acceptance: what must be true for each result.
- Checks: how required proof will establish those facts and who checks it.
- Limits: exclusions, unresolved choices, and operation authority.

Complete coverage matters more than length. A small plan can use five short fields; a detailed request needs its relevant detail preserved. A task table, internal plan, or progress summary cannot replace this visible plan. Label material assumptions rather than silently making them requirements.

Compare the visible plan with every explicit user requirement before creating or claiming tasks. Supply missing coverage first. A plan-only request stops after the plan. A request to plan and implement proceeds without another approval round unless a material choice remains unresolved. For new authorized work or a material scope change, restate the changed intent and update the affected plan fields before changing tasks. Otherwise, reuse the visible approved plan; do not reprint it for each task transition.

Before creating tasks, Lead reviews atomicity. One task has one independently accepted outcome, owning contract boundary, proof cluster, and close decision. Split when parts can succeed, fail, defer, revert, or be accepted independently. Do not split by file count, estimated time, or agent availability. Keep tests, documentation, and corrections with their owning outcome unless independently deliverable. Local implementation steps remain transient.

## Grades

Assign Simple, Normal, or Complex to each task, not the project. Grades describe work complexity, not authority or safety.

- Simple: settled, bounded work with known paths and an immediate narrow check. Avoid routine Scout use and unnecessary broad tests.
- Normal: one understood behavior with several related implementation or verification steps.
- Complex: uncertain or cross-boundary work needing a reading map, explicit decisions, or stronger integration proof.

Keep grades in the visible plan, multi-task tables, and handoffs, not a CSV column or new state file. Recover their basis after compaction; reassess when facts change.

## Ledger and visible status

Before new execution tasks, use compact Backlog and current-work views to check duplicates or related work. Do not load Backlog during ordinary conversation or startup. Only direct user authority permits adding or promoting an idea. An existing row does not authorize execution.

Lead creates or claims work directly through [ledger](ledger.md). Confirm owned In Progress status, acceptance, proof, and the before-write gate before implementation. Dependencies must be Done before dependent work starts. All roles may read task facts.

Use real IDs and exact task titles, never invented proposal IDs. After confirmed creation and ownership, announce each task:

> Starting <real task ID>: <exact title>.
> Optimal process: <actual execution, support work, and wait or continue relationship>.

List only needed roles and steps, without a separate assessment stage. Repeat the process only when it changes. This can satisfy the [support announcement](../protocols/common.md).

For one task, replace the table with this announcement and short status-change and final-state lines. For multiple tasks, use these overview columns:

| Task ID | Short description | Grade | Status |
| --- | --- | --- | --- |

The full table covers the current authorized work, not unrelated history or stopped tasks.

- Beginning: for multiple tasks, show the full table after creation and confirmed ownership, with the first task In Progress, before implementation. If prerequisites block a task, report the blocker instead of announcing it as started.
- Middle: show a short status line for one changed task; combine simultaneous changes in changed rows only. Identify newly authorized scope; do not repeat unchanged rows.
- End: for multiple tasks, show the full table with actual final states after ledger reconciliation. If work stops, show the unfinished states. Do not force stopped or blocked work to Done.

After accepting required proof, close the task directly through the helper, confirm success, and show Done. Report transaction failures immediately; never present pending or failed writes as confirmed state. Pause affected work, but continue independent ready work. Confirm IDs, ownership, and write prerequisites; never bypass dependencies.

If `update_plan` is available, mirror each unresolved task there as `TASK-NNN — Title`. Map Planned to `pending`, In Progress to `in_progress`, and Done to `completed`. Rebuild unresolved rows after resume. The ledger remains authoritative; the native view is optional.

## Simple tasks and deferred review

Eligible Simple tasks use the existing `Quick Fix` context and pending-review markers. This is a review classification, not another workflow. Eligibility requires an exact reversible result, settled boundaries, and one useful immediate proof. Use Normal or Complex when architecture, interfaces, migration, security, permissions, or other material choices remain unresolved.

Lead implements, writes any necessary test, and can run the immediate essential check directly. Use Verifier when the required proof needs independent review, not merely because a test exists. Once the artifact, immediate essential proof, and required safety or usage instructions are ready, the user can test the result.

Broader regression and documentation/interaction reviews may wait for a shared checkpoint. A task may be Done with that review explicitly pending; do not call it fully reviewed. At the next shared checkpoint, and before release, Verifier covers the pending range. Lead records `--review-through TASK-ID` only after accepting the review and only for a valid Done prefix. A failed shared review needs an owned correction.

Never defer essential validation, a known documentation defect, or safety proof. Do not add mandatory tests for a purely cosmetic change when an immediate inspection supplies the necessary evidence.
