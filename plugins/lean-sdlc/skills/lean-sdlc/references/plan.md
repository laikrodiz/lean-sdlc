# Plan and task shape

## Understand and shape

Distinguish constraints from proposals. For material uncertainty, identify the primary source, failure and observable proof. When the main uncertainty is whether components work together, plan the smallest end-to-end check first. Resolve facts safely; ask about consequential choices, unavailable facts or missing permission.

Cover every explicit user requirement before task creation. A plan-only request stops after the plan; propose write-requiring experiments without running them. Implement an approved plan without reprinting it or seeking redundant approval.

Check every candidate for bundled outcomes before assigning a grade. If one requested result could pass while another fails, split them when each has its own acceptance decision. Apply this to a reusable capability and its first use, even when the second depends on the first. Keep implementation, tests, docs, and corrections together when they prove one outcome.

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

Explain the grade when it affects execution; state why any remaining Complex task cannot split.

## Ledger and visible status

Before task creation, check current `overview` for duplicates and related work. Skip this during discussion. Adding or promoting ideas requires direct authority.

Claim through the [ledger](ledger.md). Before implementation confirm owner, In Progress status, acceptance, proof and gate. Dependencies must be Done.

Use real task IDs, outcomes, completion criteria, grades, and confirmed status. One quick fix: one sentence with result, check and gaps. When tracking one task across turns, use one text line: ID, confirmed status, result or next step. Reuse confirmed facts; never call tools solely to format it. Put blocking user decisions first.

When a request has a second recorded task, show its related rows before continuing work, even if the first is Done. Include this request's completed prerequisites. Keep rows unchanged. Give grades separately; plans without records use no synthetic IDs.

Exclude unrelated and stopped work. Show actual final states after ledger reconciliation. Between checkpoints report only changes, decisions, failures or results. Combine related announcements.

Choose the display path before running the table command. In T3, look up `html_preview` and `html_render` if they are not already visible.

- **T3 with both tools:** Run `tasks.py table --html-json TASK-ID ...` first. After exit 0, parse the complete JSON and preview its nonempty `html` string. Render that same string after preview succeeds. Never send raw command output to either tool.
- **Other hosts, a missing tool, or a failed HTML path:** Run `tasks.py table TASK-ID ...` and show Markdown only on success. Otherwise report the display issue in text.

If an upgrade removed the helper, follow [helper recovery](ledger.md#missing-installed-helper) and retry the display once. Show only one table. Refresh on request, material plan changes, or useful handoff; keep blockers in plain text.

After accepting proof, close the task directly through the helper, confirm success, and show Done. Report transaction failures immediately. Pause affected work; never bypass dependencies. Follow [common](../protocols/common.md) for sequencing and waits.

For multiple tasks, optionally mirror `TASK-NNN — Title` in `update_plan` when available. Map Planned/In Progress/Done to `pending`/`in_progress`/`completed`. The ledger remains authoritative.

## Simple tasks and deferred review

For eligible Simple tasks, use the existing `Quick Fix` context and pending-review markers, not another workflow. Require an exact reversible result, settled boundaries, and useful immediate proof. Unresolved architecture, interfaces, migration, security, permissions, or material choices require Normal or Complex.

Lead implements, writes necessary tests, and may run immediate essential checks. Assign Verifier for independent proof, not merely because a test exists. User testing can start once the artifact, immediate proof, and required safety or usage instructions are ready.

Broader regression and documentation/interaction review may wait. Explicitly mark pending review on Done tasks; never call them fully reviewed. At the next shared checkpoint, and before release, Verifier checks the pending range. After acceptance, Lead records `--review-through TASK-ID` only for a valid Done prefix. Failed review requires an owned correction.

Never defer essential validation, known documentation defects, or safety proof. For cosmetic changes, sufficient immediate inspection needs no additional test.
