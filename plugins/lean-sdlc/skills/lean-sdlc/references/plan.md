# Plan

Use Plan only after explicit implementation authority. Before creating a task or implementing work, confirm authority. Discussion and proposal requests remain read-only. If authority is ambiguous, remain read-only.

Require the information, not fixed labels. Use natural prose for the outcome, important constraints, and exclusions. Only the plan needs visible structure. Use natural intent confirmation and show a concise visible plan. Define each durable plan item in natural prose with an observable completion condition and verification method. Each durable item includes observable completion conditions and proof. The verification method is its proof. A one-item plan is valid.

Use the confirmed Shape contract `why -> what -> how -> proof`. Plan adds task shape and Proof after Why and What are stable and before task creation or mutation. Derive observable acceptance from the confirmed outcome and affected value. Implementation mechanisms, changed files, and test commands support acceptance but do not define it alone.

## Task transaction

1. Use `tasks.py plan` for future unowned work.
2. Use `tasks.py start` for immediate work or `tasks.py start TASK-ID` to claim planned work.
3. Use `tasks.py update` for corrections and `tasks.py close` only after Verify.
4. Never edit `tasks.csv` directly.
5. Keep one intentional change, observable acceptance, and explicit proof per task.
6. Add dependencies only when sequencing is real.
7. Keep `tasks.csv` as the only durable task plan. Each durable plan item maps to one task, exactly once.
8. Keep requirements and design detail in their owning documents.

## Plan view projection

During implementation, `tasks.py open` supplies unresolved `Planned` and `In Progress` rows. Project each row into `update_plan` with the exact name `TASK-NNN — Title`. Map `Planned` to `pending` and `In Progress` to `in_progress`.

Call `update_plan` after task creation or start, split, merge, or a material plan change. Before or with `tasks.py close`, mark the closing row `completed`; this is an active close transition, not a rebuild state. On startup, resume, clear, or compaction, call `tasks.py open` and rebuild only unresolved rows before Deliver. Do not load full `Done` history. Brainstorming and rephrasing remain read-only and create no task view.

When a qualified parallel pair is active, combine its two ledger rows into one active view row, such as `TASK-045 + TASK-046 — <shared outcome>`. Keep both ledger rows in `tasks.csv`; it remains authoritative.

## Task sizing

One ledger task represents one Engineer checkpoint. Require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review. Keep implementation tests inside the task. Keep Maintainer and Verifier work attached unless it is independently deliverable.

Split a task for independent behavior, module outcome, proof, or work that needs an Architect checkpoint. Split a task when a part can fail, ship, revert, resume, or close independently, crosses a contract, or needs another durable decision. Merge pieces without independent value or proof. Do not use time or line-count limits. Keep one task resumable from repository truth and its ledger row after compaction.

Keep acceptance corrections in the current task. Create a new task for new behavior or a new decision. Shape the nearest dependency frontier fully. Keep later work coarse until its dependencies become current.

## Execution shape

Before Deliver, apply the [Subagent Policy](subagents.md) only when delegation is ready. Solo planning does not load child policy. The Architect settles architecture, interfaces, invariants, allowed paths, acceptance, proof, and stop conditions before execution.

Use [subagents.md](subagents.md) for child triggers, scheduling, handoffs, profiles, checkpoints, and reporting. Keep local implementation steps and correction handoffs transient. Never send several tasks or an internal backlog.

When at least two tasks are ready, the Architect checks the next ready pair. Parallelize only when the resource gate passes and elapsed time should decrease. Otherwise, name the shared resource or dependency and work serially. Do not score the choice or add a mode.

Ready means implementation authority, visible plan, ownership, boundaries, dependencies, acceptance, proof, and integration responsibility are unambiguous.
