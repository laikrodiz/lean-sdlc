# Plan

Use Plan when approved work needs a task, dependencies, ownership, or an execution shape.

The user-selected lead owns planning. Without an explicit profile, use Sol `high`; use `xhigh` or `max` for unusually risky dependencies or integration choices.

## Task transaction

1. Use `tasks.py plan` for future unowned work.
2. Use `tasks.py start` for immediate work, or `tasks.py start TASK-ID` to claim a Planned task.
3. Use `tasks.py update` for corrections and `tasks.py close` only after Verify.
4. Never edit `tasks.csv` directly.
5. Keep one intentional change, observable acceptance, and explicit proof per task.
6. Add dependencies only when sequencing is real. A task cannot close before its dependencies.
7. Keep requirements and design detail in their owning documents rather than the ledger.

Task transactions themselves are exempt from the task-before-write rule; otherwise the rule would be circular.

## Execution shape

Before Deliver, apply the [Subagent Policy](subagents.md) and state its one-line Orchestration Gate. The lead settles architecture, interfaces, invariants, allowed paths, acceptance, proof, and stop conditions before issuing one execution unit.

Execution units are transient checkpoints under the lead-owned task; never add ledger rows for sequential Executor handoffs. Parallel writers require separate owned tasks and disjoint paths.

Ready means ownership, boundaries, dependencies, acceptance, proof, and integration responsibility are unambiguous.
