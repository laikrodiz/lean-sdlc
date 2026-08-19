# Plan

Require information, not fixed labels. Use natural prose for outcome, constraints, and exclusions. Only the plan needs visible structure. Show a concise visible plan. Define each durable plan item in natural prose with an observable completion condition and verification method. The verification method is its proof. A one-item plan is valid.

Use the confirmed Shape contract `why -> what -> how -> proof`. Plan adds task shape and Proof after Why and What are stable. Derive observable acceptance from the confirmed outcome and affected value. Implementation mechanisms, changed files, and test commands support acceptance but do not define it alone.

## Quick Fix classification

Quick Fix is inline Plan classification, not a mode, lane, task type, or prompt. Record Context `Quick Fix`.

Eligibility requires an exact requested outcome, local reversible scope, no unresolved product, design, architecture, public interface, schema, migration, dependency, security, generated-file, or external-state choice, and one immediate narrow proof. If uncertain, use Standard work. A user may choose Standard. A request to use Quick Fix never bypasses eligibility.

Every Quick Fix write needs implementation authority, one visible plan item, one owned task, and `lean_check.py --before-write` before the first non-control write. Show classification briefly in plan prose. Keep `update_plan` names exact: `TASK-NNN — Title`.

Architect may execute Quick Fix in Assisted or Solo. Do not spawn Engineer, Maintainer, or Verifier per Quick Fix. Shared batch may reuse or start Verifier when normal proof trigger applies. Review diff and run narrow proof before close.

Mixed: Standard final checkpoint reviews pending Quick Fixes and closes with `--review-through TASK-NNN`. Quick-only multi-fix batch: last Quick Fix may close with that flag after review. Standalone remains pending until next Standard checkpoint.

## Backlog

Backlog is parked work. It never authorizes planning or implementation. Only a direct user request may add or promote it. An Architect may propose placement only for a substantial reason and must wait for approval.

Before new Standard work, the Architect reads `tasks.py backlog` and checks duplicates, broader items, or related ideas. Do not load Backlog on startup, resume, brainstorming, or Quick Fix work.

Promotion is Shape and Plan, not a raw status flip. It adds proper title sizing, acceptance, proof, and dependencies. Promotion to In Progress adds an owner and requires explicit implementation authority. Planned promotion is not implementation authority. If a Backlog idea is broad, promote the original ID as the first coherent task and create sibling tasks for other independent outcomes. A Feature document remains optional under its existing trigger.

## Task preflight

Before task creation, ask whether one behavior, one contract boundary, one proof cluster, and one accept-or-reject decision cover all work. Split on any independent answer. Treat `and` in a title as a review signal, not an automatic split.

## Task transaction

Use `tasks.py plan` for work and `tasks.py start` for immediate or claimed work. Use `tasks.py update` for corrections and `tasks.py close` only after Verify. Never edit `tasks.csv`. Each task has observable acceptance and explicit proof. Add dependencies only when sequencing is real. Keep `tasks.csv` as the only durable task plan; each durable plan item maps to one task.

## Plan view projection

During implementation, `tasks.py open` supplies unresolved `Planned` and `In Progress` rows and excludes Backlog. Project each row into `update_plan` with the exact name `TASK-NNN — Title`. Map `Planned` to `pending` and `In Progress` to `in_progress`.

Refresh `update_plan` after task creation or start, split, merge, or material plan change. Before or with `tasks.py close`, mark the closing row `completed`; this is an active close transition, not a rebuild state. On startup, resume, clear, or compaction, call `tasks.py open` and rebuild only unresolved non-Backlog rows before Deliver. Do not load full `Done` history. Brainstorming and rephrasing remain read-only and create no task view.

Combine a qualified parallel pair into one view row; `tasks.csv` remains authoritative.

## Task sizing

One ledger task represents one Engineer checkpoint. One ledger task equals one independently accepted behavior change under one owning contract boundary, one proof cluster, and one close decision. It may touch several files, tests, documentation, or migration steps only when all work is inseparable for that behavior.

Require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review. Keep implementation tests inside the task. Keep Maintainer and Verifier work attached unless independently deliverable. Keep one task resumable from repository truth and its ledger row after compaction.

Split a task when a part can succeed, fail, defer, revert, release, or be accepted independently; belongs to another behavior or contract area; or needs another Architect decision. Merge pieces without independent value or proof.

Keep a correction in the same task when it only satisfies unchanged acceptance. A new behavior needs a new task. Never size by elapsed time, file count, line count, or command count.

## Ready work

When at least two tasks are ready, Architect checks the next ready pair. Parallelize when resource gate passes and elapsed time should decrease. Otherwise, name the shared resource or dependency; work serially. Do not score the choice or add a mode.

Keep local implementation steps and correction handoffs transient.
