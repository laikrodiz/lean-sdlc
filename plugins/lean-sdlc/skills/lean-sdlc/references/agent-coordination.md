# Agent Coordination

## Modes

- Assisted, default: lead plus lazy sidecars and at most two temporary agents.
- Focused: lead plus lazy sidecars; no temporary agents.
- Solo: lead only; execute the same checks and operations locally.

The user's mode remains active for the task until changed. The lead alone owns user dialogue, decisions, task state, integration, and closeout.

## Spawn payload

Read [model-routing.md](model-routing.md) before spawning. Every spawn must explicitly pass its resolved model, reasoning effort, and non-full-history `fork_turns`; omission or accidental lead-profile inheritance is invalid. Use `fork_turns: none` for sidecars and send their compact handoff directly. Use a bounded positive turn count for a temporary agent only when those recent turns are necessary.

## Stable sidecars

Spawn sidecars only when their first operation is ready. Reuse them while task, role, repository, and assumptions remain stable.

- Verifier: run tests, lint, type checks, structural checks, and diff inspection. Return operation pass/fail, evidence, or specific failures. Never repair source or choose close, fail, or reopen for the task.
- Operator: run build, package, CI, deploy, flash, runtime, and smoke procedures. Compress logs and identify artifacts and targets. Never repair source, invent procedures, or choose task disposition.

Sidecars may create only expected temporary or build artifacts within the active task. They never edit source or `tasks.csv`.

## Temporary agents

Use one when a substantial bounded scope saves meaningful lead context or wall time after assignment and integration. Use two only for independent scopes. Good uses include bounded exploration, isolated implementation, log analysis, or a separate proof surface.

Keep work with the lead when it is quick, coupled, decision-heavy, or expensive to explain. Parallel writers require separate owned tasks and disjoint paths.

Only the lead spawns and steers agents. Depth is one; child agents never spawn children or hand work directly to another child.

## Handoff

Send:

`Task | Operation or deliverable | Delta or boundary | Expected result`

Return:

`Status | Evidence or artifacts | Issue or risk | Next`

`Status` describes the delegated operation, never task disposition. Reference files and saved logs instead of pasting large content. Preserve exact decisions, commands, fingerprints, failures, and evidence; omit exploration chatter.

## Checkpoint barrier

1. Pause writers.
2. Identify the checkpoint by commit or an exact working-tree fingerprint.
3. Tell the sidecar that identity and the narrow command or procedure.
4. Require the sidecar to confirm the identity before acting.
5. Invalidate the result after any relevant source change.

## Context and lifetime

Agent lifetime is not durable. A wait timeout may only stop the current wait, and any child may disappear. Store persistent knowledge in repository documents, never only in agent context.

When respawning a sidecar, rehydrate it from:

1. its stable role above;
2. the active task request;
3. `docs/OPERATIONS.md` when relevant;
4. the current checkpoint identity.

Keep profiles, tools, and stable instructions unchanged during a task. Send incremental deltas to reused agents. Treat cache reuse as best effort; do not assume cache transfer across models, new agents, or changed tool sets.

The lead reviews every return, reconciles it with repository truth, and decides the next step.
