---
name: lean-sdlc
description: Run Lean-SDLC when the user explicitly invokes Lean-SDLC or `$lean-sdlc`, or when a repository AGENTS.md requires Lean-SDLC for planning, diagnosis, mutation, verification, or closeout. Route the work through Shape, Decide, Plan, Diagnose, Deliver, or Verify; enforce an owned task before repository writes; and use controlled agents and evidence-based completion. Do not invoke implicitly for read-only work outside a Lean-SDLC repository.
---

# Lean-SDLC

Keep repository intent, work, implementation, and proof coherent with the smallest useful process.

## Start

1. Read repository `AGENTS.md`.
2. Read [references/repository-contracts.md](references/repository-contracts.md).
3. Identify the requested outcome, current repository truth, active task, and orchestration mode.
4. For a new repository, run [scripts/init_repo.py](scripts/init_repo.py), verify the minimal contract, close `TASK-000` as owner `bootstrap`, then ask the user to restart or resume so the scoped plugin hook supplies the stable numeric owner. For an older ledger, run [scripts/tasks.py](scripts/tasks.py) `upgrade` under its owned active task.
5. Select the earliest unresolved lane below. Continue through later gates in the same task when their inputs are ready.
6. For substantial work, read [references/model-routing.md](references/model-routing.md) and [references/agent-coordination.md](references/agent-coordination.md). Read [references/operations.md](references/operations.md) before build, package, deploy, flash, runtime, or smoke work.

## Route

| State or request | Lane |
| --- | --- |
| Problem, user, behavior, scope, stage, or version promise is unclear | [Shape](references/shape.md) |
| Stable intent needs a durable technical choice or boundary | [Decide](references/decide.md) |
| Approved work needs a task, dependencies, or execution ownership | [Plan](references/plan.md) |
| A failure exists and its cause or fault boundary is uncertain | [Diagnose](references/diagnose.md) |
| Cause, scope, acceptance, proof, and owned task are ready | [Deliver](references/deliver.md) |
| Completion is claimed, truth conflicts, or a task may close | [Verify](references/verify.md) |

Do not stop merely because one lane completed. Stop when user authority, required truth, or evidence is missing.

## Hard Gates

1. Treat task-ledger commands as control transactions; they do not require a prior task.
2. Before any other repository mutation, create immediate work with `tasks.py start` or claim planned work with `tasks.py start TASK-ID`. Never edit `tasks.csv` directly.
3. Require one `In Progress` task owned by the current task owner, measurable acceptance, and explicit proof.
4. Run `lean_check.py --before-write --task TASK-ID --owner OWNER` before the first write.
5. Diagnose an unknown cause before implementing a fix.
6. Keep scope to one intentional change. Record new durable choices before relying on them.
7. Verify acceptance, documentation parity, and the relevant repository state before `tasks.py close`.
8. Only the owning task closes work. A different task may close it only after a direct user request using the recorded override.

Read-only inspection needs no task. Small writes still use a small `REPO` task.

## Orchestration

Use Assisted mode by default, Focused mode when the user asks for focused work, and Solo mode when the user asks for one agent or no subagents. Keep the lead responsible for user dialogue, decisions, task state, integration, and closeout.

Use the Verifier sidecar at coherent checkpoints. Use the Operator sidecar only for learned or guided operations. Spawn temporary agents conservatively, at depth one, with no more than two active in addition to sidecars.

## Result

Leave one compact chain:

`project truth -> durable decision if needed -> owned task -> change -> proof -> evidence`
