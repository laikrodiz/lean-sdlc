# Agent Coordination

Use subagents only when their expected benefit exceeds assignment cost, cache-write cost, review cost, and integration risk.

## Delegation Gate

Keep work local when:

1. the next main step blocks on the result,
2. the task is a quick read or one-step edit,
3. ownership overlaps current work,
4. explaining and rechecking costs about as much as doing it,
5. the task still contains a decision the main agent must make.

Use read-only explorers for bounded evidence collection. Use workers for approved execution with exact ownership and proof. Keep user dialogue, scope, decisions, integration, closeout, and final output with the main agent.

## Agent Lifecycle

1. Default to no subagents.
2. Use one worker for one substantial bounded task.
3. Use at most two workers by default, only with disjoint tasks and paths.
4. Keep spawn depth at one. Do not let workers spawn workers.
5. Reuse an existing agent when task id, role, owned paths, and assumptions remain unchanged.
6. Send reused agents only the new evidence or correction.
7. Keep a writing agent available through main-agent verification; close it after the task is verified and integrated.
8. Start a fresh agent when task, ownership, assumptions, or required model changes, or when its context has become noisy or stale.

Do not chain worker handoffs. Every worker returns to the main agent, which reconciles and dispatches the next step.

## Write Ownership

- Every writing agent must own one `In Progress` task.
- One task has one writer at a time.
- Parallel writers require separate tasks and disjoint paths.
- Read-only explorers may work without a task because they cannot mutate repository state.
- Workers may report completion but must not move a task to `Done`; the main agent verifies and closes it.

## Assignment Contract

Place stable role instructions first and task-specific data last. Include:

1. task id and parent reference,
2. exact deliverable,
3. owned paths and read boundary,
4. approved facts and decisions,
5. acceptance and proof commands,
6. forbidden unrelated work,
7. stop conditions for new ambiguity,
8. the return contract below.

## Return Contract

Return only:

1. outcome: complete, partial, or blocked,
2. changed files or produced artifacts,
3. proof commands and exact results,
4. decisions made inside the allowed boundary,
5. unresolved assumptions, risks, or blockers,
6. recommended next action.

Point to files, diffs, commits, and test output instead of copying large artifacts. Preserve decisions and evidence exactly; compress exploration chatter.

## Cache Discipline

1. Keep agent profiles, tools, skills, and shared instructions stable during a task.
2. Put volatile task data after the stable assignment prefix.
3. Reference repository files rather than pasting them repeatedly.
4. Send incremental deltas when reusing an agent.
5. Never spawn or call an agent only to warm a cache.
6. Never sacrifice correctness, isolation, or a clean task boundary for a possible cache hit.
7. Treat cache reuse as best effort unless the current surface exposes cache measurements or controls.

Do not assume cache state transfers across models, newly spawned threads, or changed tool sets.

## Integration

The main agent reads the returned artifacts, checks acceptance fit, reviews scope, reruns relevant proof, reconciles documentation, and records evidence before closeout.
