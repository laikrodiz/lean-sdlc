# Parallel Engineers

Use only for the current request. Without explicit opt-in, create no worktrees. Engineer count is a maximum, not a quota. Keep coupled outcomes together. Explain any lower useful count once.

Lead uses the primary ledger only. Settle interfaces and give shared files, generated outputs, and external resources one owner. Start from a clean, named destination branch. Record its name and commit. Never stash user changes automatically. Use `scripts/parallel.py begin REPOSITORY RUN` for a temporary local integration checkout. Record its returned path.

Use `tasks.py --repo REPOSITORY ready --slots FREE TASK-ID ...` for this request's eligible tasks. Limit free slots by requested width, host capacity, resources, and pending integration. Zero slots means wait. Claim each selected task with the normal before-write gate. Refill on completion events. Do not start dependent work until its accepted inputs exist in its checkout.

Launch one host-managed worktree per Engineer. In T3, use `delegate_task` with `isolation:"worktree"` and the Lead model and effort. Never substitute a shared checkout. Use task IDs, not a fixed name pool. Give each Engineer its base commit, allowed files, interface, acceptance, check, and stop condition. Verify checkout identity and base before edits. If the host cannot supply that base or isolation, stop the affected dispatch.

Give Engineers the Lead's startup context and successful task gate with the assignment. The primary repository owns the ledger; the assigned worktree owns the edits. Do not initialize a worker ledger or rediscover the project there.

Engineers make one local task commit and return its ID, owned paths, checks, and exceptions. No ledger writes, pushes, merges, cleanup, or children. Lead alone integrates. Use `parallel.py accept INTEGRATION WORKER BASE CHECKPOINT PATH ...` after inspecting the change and evidence. Merge one checkpoint at a time. On conflict, preserve both sides; resolve and test within scope or stop. Never select a side automatically.

Scout investigates specific unknowns. Maintainer updates shared documents after integration. Verifier checks the frozen combined result when independent proof is required. Do not create support teams per Engineer. Show accepted, active, queued, and blocked outcomes in the existing task view.

Use `parallel.py land REPOSITORY INTEGRATION BRANCH BASE VERIFIED` to stage the combined change. Add `--commit` only with commit authority. Push only the accepted destination, once, if authorized. Never publish worker branches.

After confirming processes stopped, retire only recorded run-owned checkouts: `parallel.py retire KEEPER TEMPORARY CHECKPOINT`. Keep the integration branch as recovery for an uncommitted delivery. Delete only named run branches with Git's merged-branch check after durable retention. Preserve dirty, canceled, disputed, or unverified work. Report retained paths and the next safe action.
