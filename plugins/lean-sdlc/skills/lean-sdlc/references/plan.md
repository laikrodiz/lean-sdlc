# Plan

Use Plan only after the user gives explicit implementation authority. Discussion or proposal requests remain read-only, and ambiguous authority stays read-only.

Require the information, not fixed labels. Use natural prose for the outcome, important constraints, and exclusions. Only the plan needs visible structure.

Before creating a task or implementing work, the lead gives the natural intent confirmation, then shows a concise visible plan. Define each durable plan item in natural prose with its observable completion condition and verification method. The verification method is its proof. A one-item plan is valid.

Each durable item includes observable completion conditions and proof.

The user-selected lead owns planning. Without an explicit profile, use Sol `high`; use `xhigh` or `max` for unusually risky dependencies or integration choices.

## Task transaction

1. Use `tasks.py plan` for future unowned work.
2. Use `tasks.py start` for immediate work, or `tasks.py start TASK-ID` to claim a Planned task.
3. Use `tasks.py update` for corrections and `tasks.py close` only after Verify.
4. Never edit `tasks.csv` directly.
5. Keep one intentional change, observable acceptance, and explicit proof per task.
6. Add dependencies only when sequencing is real. A task cannot close before its dependencies.
7. Keep `tasks.csv` as the only durable task plan. Map each durable plan item to exactly one task.
8. Keep requirements and design detail in their owning documents rather than the ledger.

## Task sizing

One durable task represents one independently accepted repository state.
The task owns one observable outcome, one coherent change boundary, one acceptance set, one proof set, and one close decision.
The task must resume from repository truth and its ledger row after compaction.
Each durable plan item maps to one task, exactly once. Implementation steps and correction handoffs remain transient. Do not add them as separate plan items.

Split a task when a part can fail, ship, revert, resume, or close independently.
Split a task when a part needs different proof.
Split a task when a part crosses a contract.
Split a task when a part needs another durable decision.
Merge rows when they only describe inseparable coding mechanics.
Avoid fixed limits based on time, lines, or file count.
Shape the nearest dependency frontier fully. Keep later work coarse until its dependencies become current.

Task transactions themselves are exempt from the task-before-write rule; otherwise the rule would be circular.

## Execution shape

Before Deliver, apply the [Subagent Policy](subagents.md) and state its one-line Orchestration Gate. The lead settles architecture, interfaces, invariants, allowed paths, acceptance, proof, and stop conditions before issuing one execution unit. The execution task must match one item in the visible plan.

Executor receives one durable task. Reuse the existing `executor_david` thread when another repository task becomes ready. Local implementation steps and correction handoffs remain transient. Never send several tasks or an internal backlog. Parallel writers require separate owned tasks and disjoint paths.

Ready means implementation authority, the visible plan, ownership, boundaries, dependencies, acceptance, proof, and integration responsibility are unambiguous.
