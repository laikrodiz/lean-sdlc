# Plan and task shape

## Understand and shape

Before creating or claiming tasks, restate the request in natural prose. Explain who needs the change and why, using established context. Keep distinct outcomes visible. Include shared constraints, material uncertainty, and authorized actions. State a proposed approach as a proposal, not a verified fact. Do not require fixed headings or a separate opening checklist.

Compare the plan with every explicit user requirement. Restore missing coverage before task creation. A plan-only request stops after the plan without ledger writes. Plan-and-implement needs no renewed approval unless a material choice remains unresolved. Reuse an approved plan without reprinting it.

Check every candidate for bundled outcomes before assigning a grade. One task has one independently acceptable outcome, coherent contract boundary, proof cluster, and close decision. Split outcomes that can succeed or fail independently, even when the original candidate looks Simple or Normal. Keep implementation steps, tests, documentation, and corrections with their outcome unless independently deliverable.

Use one sizing pass before creating tasks or showing their table. Preserve real dependencies and combined-result proof. Do not split by file count, time, available agents, or target grade.

Use Complex for intrinsic difficulty or inseparable coupling, not accumulated scope. Explain in one sentence why another split would not help. Do not repeat sizing.

Each task carries its own observable outcome, acceptance criteria, required checks, and task-specific limits in existing ledger fields. State shared constraints once and refer to them where needed. Do not add fields, documents, or an approval stage for sizing.

Split only work within the approved scope. For a new independent outcome, define a separate task before implementing that outcome. Update affected dependencies. Preserve existing evidence and unresolved original requirements. Moving work does not close the original task.

If a required refactor exceeds scope, pause affected work. Explain why and propose the smallest viable refactor. Wait for user approval before editing it. Unaffected authorized work can continue.

## Grades

Assign Simple, Normal, or Complex after settling boundaries. Grades describe complexity, not authority or safety.

- Simple: settled, bounded work with known paths and an immediate narrow check. Avoid routine Scout use and unnecessary broad tests.
- Normal: one understood behavior with several related implementation or verification steps.
- Complex: one coherent outcome with intrinsic uncertainty, difficult reasoning, or inseparable cross-boundary changes needing stronger proof.

Keep grades and Complex reasons in the visible plan and handoffs, not new columns or state files. Recover their basis after compaction.

## Ledger and visible status

Before new execution tasks, check `overview` for duplicates or related work. Do not do this during ordinary conversation. Adding or promoting ideas requires direct user authority; existing rows do not authorize execution.

Lead creates or claims tasks through [ledger](ledger.md). Confirm owned In Progress status, acceptance, proof, and the before-write gate before implementation. Dependencies must be Done before dependent work starts.

Use real task IDs, outcomes, completion criteria, grades, and confirmed status. For one task, a short task line is sufficient. For multiple tasks, show the settled current work before implementation:

| Task ID | Outcome | Done when | Grade | Status |
| --- | --- | --- | --- | --- |

The table excludes unrelated history and stopped work. Show actual final states after ledger reconciliation. Between these checkpoints, report changed tasks, decisions, failures, or results only. A support announcement can accompany the relevant change; no process slogan or repeated plan is required.

After accepting required proof, close the task directly through the helper, confirm success, and show Done. Report transaction failures immediately; do not present pending writes as confirmed state. Pause affected work; never bypass dependencies. Follow [common](../protocols/common.md) for sequential execution and waiting.

If `update_plan` is available, mirror unresolved tasks as `TASK-NNN — Title`. Map Planned to `pending`, In Progress to `in_progress`, and Done to `completed`. The ledger remains authoritative; the native view is optional.

## Simple tasks and deferred review

Eligible Simple tasks use the existing `Quick Fix` context and pending-review markers. This is a review classification, not another workflow. Eligibility requires an exact reversible result, settled boundaries, and one useful immediate proof. Use Normal or Complex when architecture, interfaces, migration, security, permissions, or other material choices remain unresolved.

Lead implements, writes any necessary test, and can run the immediate essential check directly. Use Verifier when the required proof needs independent review, not merely because a test exists. Once the artifact, immediate essential proof, and required safety or usage instructions are ready, the user can test the result.

Broader regression and documentation/interaction reviews may wait for a shared checkpoint. A task may be Done with that review explicitly pending; do not call it fully reviewed. At the next shared checkpoint, and before release, Verifier covers the pending range. Lead records `--review-through TASK-ID` only after accepting the review and only for a valid Done prefix. A failed shared review needs an owned correction.

Never defer essential validation, a known documentation defect, or safety proof. Do not add mandatory tests for a purely cosmetic change when an immediate inspection supplies the necessary evidence.
