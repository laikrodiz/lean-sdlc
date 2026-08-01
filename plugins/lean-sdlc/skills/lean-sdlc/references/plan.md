# Plan

Use Plan only after explicit implementation authority. Before creating a task or implementing work, confirm authority. Discussion and proposal requests remain read-only. If authority is ambiguous, remain read-only.

Require the information, not fixed labels. Use natural prose for the outcome, important constraints, and exclusions. Only the plan needs visible structure. Use natural intent confirmation and show a concise visible plan. Define each durable plan item in natural prose with an observable completion condition and verification method. Each durable item includes observable completion conditions and proof. The verification method is its proof. A one-item plan is valid.

## Task transaction

1. Use `tasks.py plan` for future unowned work.
2. Use `tasks.py start` for immediate work or `tasks.py start TASK-ID` to claim planned work.
3. Use `tasks.py update` for corrections and `tasks.py close` only after Verify.
4. Never edit `tasks.csv` directly.
5. Keep one intentional change, observable acceptance, and explicit proof per task.
6. Add dependencies only when sequencing is real.
7. Keep `tasks.csv` as the only durable task plan. Each durable plan item maps to one task, exactly once.
8. Keep requirements and design detail in their owning documents.

## Task sizing

One durable task represents one independently accepted repository state. The task owns one observable outcome, one coherent change boundary, one acceptance set, one proof set, and one close decision. The task must resume from repository truth and its ledger row after compaction.

Split a task when a part can fail, ship, revert, resume, or close independently. Split a task when a part needs different proof. Split a task when a part crosses a contract. Split a task when a part needs another durable decision. Merge rows when they only describe inseparable coding mechanics. Avoid fixed limits based on time, lines, or file count. Shape the nearest dependency frontier fully. Keep later work coarse until its dependencies become current.

## Execution shape

Before Deliver, apply the [Subagent Policy](subagents.md) only when delegation is ready. Solo planning does not load child policy. The Architect settles architecture, interfaces, invariants, allowed paths, acceptance, proof, and stop conditions before one execution unit.

Engineer receives one durable task. Reuse the existing Engineer role thread when another repository task becomes ready. Local implementation steps and correction handoffs remain transient. Never send several tasks or an internal backlog. Parallel writers require separate owned tasks and disjoint paths.

Ready means implementation authority, visible plan, ownership, boundaries, dependencies, acceptance, proof, and integration responsibility are unambiguous.
