# Plan and task shape

## Understand and shape

Distinguish constraints from proposals. For material uncertainty, identify the primary source, failure and observable proof. Resolve facts safely; ask about consequential choices, unavailable facts or missing permission.

Cover every explicit user requirement before task creation. A plan-only request stops after the plan; propose write-requiring experiments without running them. Implement an approved plan without reprinting it or seeking redundant approval.

Check every candidate for bundled outcomes before assigning a grade. Split independently acceptable outcomes, even for apparent Simple or Normal work. Keep implementation, tests, docs, and corrections together when they share a contract, proof, and closure decision.

Use one sizing pass before creation or display. Dependencies represent required results, not execution order. Preserve combined proof. Never split by file count, duration, staffing or grade.

Reserve Complex for intrinsic difficulty or inseparable coupling. Explain why splitting cannot help.

Each task carries its own observable outcome, acceptance, required checks, and limits in existing ledger fields. State shared constraints once. Add no sizing fields, documents, or approvals.

Split only work within the approved scope. For a new independent outcome, define a separate task before implementing that outcome. Update affected dependencies. Preserve existing evidence and unresolved original requirements. Moving work does not close the original task.

If a required refactor exceeds scope, pause affected work. Explain why and propose the smallest viable refactor. Wait for user approval before editing it. Unaffected authorized work can continue.

## Grades

Grade settled tasks Simple, Normal, or Complex. Grades describe complexity, not authority or safety.

- Simple: settled, bounded work with known paths and an immediate narrow check. Avoid routine Scout use and unnecessary broad tests.
- Normal: understood behavior with related implementation or verification steps.
- Complex: intrinsic uncertainty, difficult reasoning, or inseparable coupling needing stronger proof.

Show grades and Complex reasons in plans and handoffs without adding columns or files.

## Ledger and visible status

Before task creation, check current `overview` for duplicates and related work. Skip this during discussion. Adding or promoting ideas requires direct authority.

Claim through the [ledger](ledger.md). Before implementation confirm owner, In Progress status, acceptance, proof and gate. Dependencies must be Done.

Use real task IDs, outcomes, completion criteria, grades, and confirmed status. One Simple fix: state the result, what passed, and anything pending. No table. Before multi-task implementation, show:

| Task ID | Outcome | Done when | Grade | Status |
| --- | --- | --- | --- | --- |

Exclude unrelated and stopped work. Show actual final states after ledger reconciliation. Between checkpoints report only changes, decisions, failures or results. Combine related announcements.

After accepting proof, close the task directly through the helper, confirm success, and show Done. Report transaction failures immediately. Pause affected work; never bypass dependencies. Follow [common](../protocols/common.md) for sequencing and waits.

If `update_plan` is available, mirror unresolved tasks as `TASK-NNN — Title`. Map Planned to `pending`, In Progress to `in_progress`, and Done to `completed`. The ledger remains authoritative; the native view is optional.

## Simple tasks and deferred review

For eligible Simple tasks, use the existing `Quick Fix` context and pending-review markers, not another workflow. Require an exact reversible result, settled boundaries, and useful immediate proof. Unresolved architecture, interfaces, migration, security, permissions, or material choices require Normal or Complex.

Lead implements, writes necessary tests, and may run immediate essential checks. Assign Verifier for independent proof, not merely because a test exists. User testing can start once the artifact, immediate proof, and required safety or usage instructions are ready.

Broader regression and documentation/interaction review may wait. Explicitly mark pending review on Done tasks; never call them fully reviewed. At the next shared checkpoint, and before release, Verifier checks the pending range. After acceptance, Lead records `--review-through TASK-ID` only for a valid Done prefix. Failed review requires an owned correction.

Never defer essential validation, known documentation defects, or safety proof. For cosmetic changes, sufficient immediate inspection needs no additional test.
