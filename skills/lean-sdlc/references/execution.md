# Execution Routing Workflow

Use after tasks are approved and before code starts when execution ownership is not already obvious.

Use Terra at `medium` or Sol at `low` for straightforward routing. Read [model-routing.md](model-routing.md) and [agent-coordination.md](agent-coordination.md) before delegating. Explicit user model choices take precedence.

## Modes

1. Local: one ready task blocks the next critical step or ownership overlaps.
2. Delegated: one substantial bounded task benefits from isolated execution, or two tasks have disjoint write scope and exact proof paths.
3. Batch: a larger disjoint queue benefits from explicit integration checkpoints.

Unknown diagnosis goes to debugging before a worker receives implementation. Keep quick work local. Delegation must save meaningful wall time or main-agent context after assignment, review, and integration costs.

Default to no workers. When the user has enabled subagents for the thread, use one worker for a substantial isolated task when assignment and integration cost less than local execution. Use at most two for independent scopes. Reuse an agent only for the same task, role, paths, and assumptions. Every writing worker owns one `In Progress` task; parallel writers require separate tasks and disjoint paths.

Use the assignment and return contracts in the coordination reference. Workers return only to the main agent and never mark tasks `Done`.

After execution, review scope and evidence, then route to verification. Use traceability for uncertain truth and documentation maintenance only for approved cleanup.

Success means ownership and model effort match the task without spending more on delegation than the work itself.
