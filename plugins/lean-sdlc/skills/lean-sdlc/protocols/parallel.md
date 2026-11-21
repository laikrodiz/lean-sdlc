# Parallel Engineers

Without explicit opt-in, create no worktrees. When the user requests or offers Engineers, give the count, including zero, in the plan before implementation. Explain which work can run independently or why none can. Respect the requested maximum. At zero, Lead implements directly.

Use only the primary ledger. Settle interfaces; assign shared files, outputs, and external resources one owner. Record the clean destination branch and commit. Never automatically stash user changes. Record the integration checkout from `scripts/parallel.py begin REPOSITORY RUN`.

Select this request’s tasks with `tasks.py --repo REPOSITORY ready --slots FREE TASK-ID ...`. Bound slots by requested width, capacity, resources, and pending integration. At zero, wait. Claim with the before-write gate. Refill on completion. Dependencies need accepted inputs in their checkout.

Launch one host worktree per Engineer. In T3, use `delegate_task` with `isolation:"worktree"` and Lead’s model and effort. Never substitute a shared checkout. Set the `delegate_task` title to `Engineer <task ID>` from the ledger. Use the same name in progress updates. Assign base commit, files, interface, acceptance, check, and stop condition. Before edits, verify checkout identity and base. Stop dispatch if either guarantee fails.

Supply Lead’s startup context and passed task gate. Edit only the assigned worktree. Never initialize a worker ledger or rediscover the project there.

Engineers return one local task commit, owned paths, checks, and exceptions. T3 Codex Engineers also return their own `CODEX_SESSION_ID` if available. No ledger writes, pushes, merges, cleanup, or children. Lead alone integrates. Inspect changes and evidence before `parallel.py accept INTEGRATION WORKER BASE CHECKPOINT PATH ...`. Merge checkpoints individually. Preserve both conflict sides; resolve and test within scope or stop. Never select a side automatically.

Scout investigates unknowns. Maintainer updates shared documents after integration. Verifier independently checks frozen combined results when required. No per-Engineer support teams. Show accepted, active, queued, and blocked outcomes.

Use `parallel.py land REPOSITORY INTEGRATION BRANCH BASE VERIFIED` to stage the combined change. Add `--commit` only with commit authority. Push only the accepted destination, once, if authorized. Never publish worker branches.

After confirming processes stopped, retire only recorded run-owned checkouts: `parallel.py retire KEEPER TEMPORARY CHECKPOINT`. Keep the integration branch as recovery for an uncommitted delivery. Delete only named run branches with Git's merged-branch check after durable retention. Preserve dirty, canceled, disputed, or unverified work. Report retained paths and the next safe action.

After accepted cleanup, with commit and checks recorded, archive only the finished T3 Engineer’s Codex chat. Verify its explicit ID with Codex `thread/read`: T3 origin, subagent classification, and exact assigned worktree. Never infer identity from a title or T3 ID. Confirm it has no descendants before calling `thread/archive` or the Codex archive tool with that ID. Leave parents, projects, T3 records, and unresolved work alone. If any check or archive operation fails, report the skip without blocking delivery.
