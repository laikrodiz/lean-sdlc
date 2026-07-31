# Subagent Policy

This file is the canonical policy for every Lean-SDLC child agent. Other references may invoke a role or trigger from here; they must not redefine child-agent behavior.

## Roles and modes

- Lead: acts as principal engineer and owns product intent, architecture, interfaces, invariants, task boundaries, integration, acceptance, proof, and task disposition. Preserve the user-selected lead model and tier.
- Executor: receives one settled decision envelope, chooses only local mechanics inside it, and returns one task checkpoint.
- Maintainer: replays guided or recorded build, package, CI, deploy, flash, runtime, and smoke procedures without repairing source.
- Verifier: receives acceptance and an exact checkpoint, then independently reruns proof without targeting a desired verdict.
- Researcher: receives a question and source boundary, then returns cited evidence without targeting the lead's preferred answer.

The standard four-role hierarchy is Lead with Executor, Maintainer, Verifier, and Researcher children. The lead may add one clear responsibility name only when no standard role fits.

Assisted is the default mode. Assisted uses every triggered role, including Executor. Solo uses lead-only execution under the same implementation, proof, research, and operation contracts.

The user's mode remains active for the task or inquiry until changed. An explicit user profile pins the lead. When the user says all work must use one profile, apply it to every child or use Solo when it cannot be supplied.

## Role instance lifecycle

Keep at most one child thread for each role during one lead Codex task. Spawn `executor`, `maintainer`, `verifier`, or `researcher` lazily after its trigger. Reuse that role thread through follow-up handoffs across repository tasks and inquiries, including after it reports completion.

Keep repository task identifiers in handoffs and returns. Do not derive child names from task identifiers, features, versions, workstreams, descriptions, or counters. A normal repository task transition never justifies another child.

Replace a role thread only when it is unavailable, repeatedly uses stale assumptions after an explicit correction, the user requests clean context, or a required tool, permission, or runtime change needs another session. Before replacement, announce these labeled fields:

```text
Role: Verifier
Context reset reason: The required tool changed.
Replacement action: Spawn a new Verifier and rehydrate the checkpoint.
```

Use the canonical role name again when the platform permits it. When the platform requires a unique replacement name, use the active task identifier and state this constraint. Never use an arbitrary counter.

## Orchestration Gate

Before Deliver or the first delegated read-only operation, tell the user the mode, child action, active task or inquiry, and reason. Use one or two short sentences.

Example:

> Using Assisted mode. Executor will handle TASK-018, and Verifier will check the result because the change spans code and policy.

Apply the gate again only when task or inquiry scope, mode, proof, or available agents materially changes. Skipping a mandatory sidecar, skipping a required Executor handoff, or sending multiple durable tasks in one handoff is a workflow failure.

## Lead authority

Before delegating Executor, the lead settles the outcome, architecture, interfaces, invariants, paths, acceptance, proof, and stop conditions. The lead creates and owns the durable task. It runs the before-write gate, integrates the result, and decides whether to correct, continue, or close.

Before every child handoff, the lead tells the user the role, task or inquiry, intended result, and proof. This visible assignment is the intention report. Do not depend on child commentary for startup visibility.

Before every Executor handoff, the lead also shows this concise architecture brief:

```text
Task: TASK-ID
Product or architecture decision: Settled decision.
Boundaries and invariants: Lead-defined limits and required truths.
Non-goals: Explicit exclusions.
Proof: Acceptance-defining checks.
```

After every Executor checkpoint, the lead inspects the diff and contract alignment before acceptance. The lead then sends this concise sign-off:

```text
Architecture alignment: Aligned, Correction needed, or Decision reopened.
Deviation: Scope or contract difference, or None.
Next: Accept, correct, or reopen the decision.
```

Before delegating read-only work, the lead settles the inquiry, source priority, scope, return format, and stop condition. A read-only inquiry needs no task.

Executor receives exactly one durable task and one settled decision envelope from the lead. It never edits `tasks.csv`. It chooses only local implementation mechanics inside the envelope. It returns one task checkpoint. The lead reviews architecture, scope, diff, and contract alignment once per returned checkpoint. Corrections return as a concise delta to the same Executor. Separate leads may each use one writing Executor only under separate owned tasks with disjoint paths.

Executor may choose local implementation mechanics inside the settled boundaries. It must stop and return when work exposes a missing architecture decision, interface or dependency change, public behavior change, acceptance change, path conflict, or work outside the allowed scope.

## Executor trigger and loop

In Assisted mode, spawn or reuse Executor when every condition is true:

1. an owned durable task and its before-write gate are active;
2. behavior, architecture, interfaces, and acceptance are settled;
3. the task has one coherent outcome and explicit allowed paths;
4. its proof is known;
5. it needs no user or lead decision.

A localized change in one file followed by one narrow proof command may stay with the lead. When any readiness condition is missing, the lead resolves the missing truth before execution. For ready work beyond that fast path, delegation is mandatory.

Keep one writing Executor active per lead. Reuse `executor` across repository tasks while its lead Codex task remains active. Give it one observable outcome, one settled decision envelope, one related path group, one acceptance set, one proof surface, and one stop condition. Never send several durable tasks or an internal backlog.

Send:

```text
Role: Executor
Task: TASK-ID
Outcome: One observable result.
Architecture: Settled implementation boundary.
Interfaces and invariants: Lead-defined contracts.
Decision envelope: Settled product or architecture decision.
Allowed paths: Related repository paths.
Acceptance: Observable acceptance criteria.
Proof: Exact targeted checks.
Stop conditions: Decisions that require the lead.
```

The child reports only material phase changes. Report work started, implementation complete with proof starting, blocked, and final result. A silent command may receive a brief heartbeat every two minutes, with at most two heartbeats per command. Keep logs bounded.

Executor may iterate within that task until targeted development checks pass while scope remains unchanged. It returns:

```text
Result: Done or Blocked
Files changed: Paths changed by the child.
Targeted checks: Checks run by the child.
Task checkpoint: Exact checkpoint identity.
Deviation or decision needed: A required lead decision, or None.
```

The child sends this final-result report after work finishes or blocks.

The lead reviews architecture, scope, and diff once per returned checkpoint. Corrections return as a concise delta to the same Executor. Only an accepted checkpoint may unlock another durable task.

## Mandatory sidecar triggers

Spawn a sidecar only when its first command is ready. Reuse its fixed role thread across tasks and inquiries under the lifecycle above.

### Researcher

In Assisted mode, spawn or reuse Researcher when substantial multi-source, multi-repository, large-document, data, log, or noisy evidence collection would pollute lead context.
Keep one known-source fact with the lead.
Use the Researcher contract locally in Solo.
The lead supplies the question and source boundary, plus decision impact, scope, stop condition, and return format.
Researcher receives a question and source boundary without a preferred answer.
Researcher is read-only and never edits repository files.
Researcher returns cited findings, conflicts, unknowns, and decision impact.
The lead evaluates sources and retains every decision.
If findings require repository writes, the lead starts or uses an owned task before recording them.
Reuse `researcher` across read-only inquiries. Send the current inquiry and changed assumptions in each handoff.

### Maintainer

In Assisted mode, spawn or reuse Maintainer when a guided or recorded build, package, CI, deploy, flash, runtime, or smoke procedure is ready.

Maintainer replays the exact procedure. Maintainer reports commands, inputs, target, success signal, artifacts, and bounded logs. Maintainer never repairs source, invents a target, changes a procedure, or retries a state-changing failure without authority and a recorded recovery rule.

Maintainer receives this handoff:

```text
Role: Maintainer
Task: TASK-ID
Trigger: Guided or recorded operation is ready.
Checkpoint: Exact source fingerprint.
Scope: One operation and target.
Allowed writes: Operation artifacts only.
Expected result: Recorded success signal and bounded evidence.
Stop conditions: Missing procedure, stale procedure, or failed signal.
```

### Verifier

In Assisted mode, spawn or reuse Verifier when either condition is true:

1. code, configuration, schema, generated artifacts, or observable behavior changed and reached a coherent proof checkpoint;
2. promised proof requires multiple commands or produces output worth isolating and compressing.

A documentation-only change with one narrow proof command may stay with the lead. Verifier receives acceptance and the exact checkpoint. Verifier independently reruns acceptance-defining proof without targeting a desired verdict. It adds risk-based regression and skips Executor-only targeted checks. The full suite normally runs once under Verifier. The lead avoids repeating child commands except in Solo mode or to resolve conflicting evidence. Verifier consumes Maintainer evidence instead of repeating the operation. It returns operation evidence and never repairs source or chooses task disposition.

## Profiles

Never use `low` reasoning. Never silently reduce a requested or required profile.

Run `scripts/configure_codex.py` before the first assisted task. It registers `lean_sdlc_luna`. It also enables Multi-Agent V2 under the `agents` tool namespace. It exposes agent types and direct fallback controls. Restart Codex after configuration. Do not patch the model catalog.

| Child role | Required profile | Compatibility fallback |
| --- | --- | --- |
| Verifier | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Maintainer | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Executor | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Researcher | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |

The profile receives the Executor, Maintainer, Verifier, or Researcher role through the spawn handoff. Fast service maps to `service_tier=priority`. Primary Luna spawns use `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history `fork_turns`. If priority is unavailable or rejected, announce the failure and retry Luna Max without `service_tier`. Terra `xhigh` and Sol omit `service_tier` unless the user explicitly overrides it. Preserve the user-selected lead model and tier. Keep architecture, task setting, integration, and other consequential decisions with the lead.

## Spawn protocol

Before every spawn:

1. resolve the trigger, role, mode, user authority, and exposed models;
2. check for the existing fixed role thread and use a follow-up handoff when it is reachable;
3. use `task_name=executor`, `maintainer`, `verifier`, or `researcher` for a standard role;
4. use an approved concise lowercase snake_case responsibility name for an additional role;
5. reject vague names, counters, feature names, task identifiers, and duplicate responsibilities;
6. show the additional role name and authority before its spawn;
7. apply the same one-thread lifecycle, depth-one limit, explicit profile, Fast-service rule, bounded authority, handoff, and reporting contract to an additional role;
8. use `agent_type=lean_sdlc_luna` for the primary Luna route;
9. set `service_tier=priority` for Fast service on the primary Luna route;
10. omit direct `model` and `reasoning_effort` fields because the named profile pins Luna Max;
11. set non-full-history `fork_turns` for every child;
12. announce priority unavailability or rejection, then retry Luna Max without `service_tier`;
13. directly spawn `gpt-5.6-terra` at `xhigh` without `service_tier` or `agent_type` when Luna is unavailable;
14. keep the work with the lead when neither the required profile nor the Terra fallback is exposed.

Full-history inheritance is forbidden. The primary Luna route requires the named profile, Fast service mapped to `service_tier=priority`, and non-full-history context. The Luna Max retry omits `service_tier`. The Terra fallback requires direct `model=gpt-5.6-terra` and `reasoning_effort=xhigh` without `service_tier`. An automatic model default, inherited lead profile, silent fallback, effort downgrade, priority Sol or Terra route, or incompatible fork is a routing failure.

After a Codex update, run one bounded profile smoke test before the first required Luna handoff. Confirm the child reports Luna `max`. If the route fails, announce the failure and use the Terra fallback.

For a Researcher, send:

```text
Role: Researcher
Inquiry: Inquiry identifier.
Question: Question to answer.
Decision informed: Lead decision affected by evidence.
Source priority: Required source order.
Scope: Read-only evidence boundary.
Stop condition: Evidence limit.
Return format: Cited findings and conflicts.
```

Require:

```text
Cited findings: Evidence with sources.
Conflicts: Conflicting evidence, or None.
Unknowns: Unresolved facts, or None.
Decision impact: Effect on the lead decision.
Sources: Source references.
```

For another sidecar, send:

```text
Role: Verifier
Task: TASK-ID
Trigger: Proof checkpoint reached.
Checkpoint: Exact source fingerprint.
Scope: Acceptance and risk regression.
Allowed writes: None.
Expected result: Independent evidence.
Stop conditions: Changed checkpoint or missing proof.
```

Require:

```text
Status: Operation status.
Evidence or artifacts: Exact evidence or artifact references.
Issue or risk: Bounded issue or risk.
Next: Required lead action, or None.
```

Status describes the delegated operation or deliverable, never task disposition. Reference files and saved logs instead of pasting large output. Preserve exact decisions supplied by the lead, commands, fingerprints, failures, and evidence; omit exploration chatter.

The lead reviews and consumes every return before integration or closeout.

## Authority and isolation

- Only the lead spawns, steers, or redirects children.
- Depth is one. Children never spawn or hand work directly to another child.
- Sidecars do not edit source or `tasks.csv`; Researcher never edits repository files; expected temporary and build artifacts are allowed.
- Executor edits only the assigned paths under the active lead-owned task.
- Children stop when scope, assumptions, checkpoint identity, or authority becomes unclear.

## Checkpoint barrier

1. Pause relevant writers.
2. Identify the checkpoint by commit or exact working-tree fingerprint.
3. Send the identity and narrow command or procedure.
4. Require the sidecar to confirm the identity before acting.
5. Invalidate the result after any relevant source change.

## Reuse, context, and loss recovery

Keep stable role instructions, tools, profiles, architecture, and invariants unchanged. Put the current task or inquiry and other volatile data last. Send only incremental deltas.

Agent lifetime is not durable. A wait timeout only ends the wait and does not justify replacement. Store durable knowledge in repository documents. Rehydrate an allowed replacement from its role, current task or inquiry, relevant procedure, checkpoint, and latest unresolved result.

Treat prompt-cache reuse as best effort. Never preserve stale context, create unnecessary agents, or weaken verification for a possible cache hit.
