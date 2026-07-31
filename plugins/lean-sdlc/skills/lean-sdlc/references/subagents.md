# Subagent Policy

This file is the canonical policy for every Lean-SDLC child agent. Other references may invoke a role or trigger from here; they must not redefine child-agent behavior.

## Roles and modes

- Lead: owns user dialogue, behavior, architecture, interfaces, task state, acceptance, proof, integration, and closeout. Preserve the user-selected lead profile.
- Executor: receives exactly one durable task, performs local implementation and fast targeted development checks, and returns one task checkpoint.
- Researcher sidecar: gathers substantial read-only evidence and returns cited findings.
- Verifier sidecar: independently reruns acceptance-defining proof and risk-based regression against one checkpoint.
- Operator sidecar: runs guided or recorded build, package, CI, deploy, flash, runtime, and smoke operations.

Assisted is the default mode. Required sidecars run lazily. A ready durable task beyond the direct fast path must use Executor. Focused keeps triggered sidecars, including Researcher when its trigger applies, and disables Executor. Solo disables every child. The lead follows the same implementation, proof, research, and operation contracts locally.

The user's mode remains active for the task or inquiry until changed. An explicit user profile pins the lead. When the user says all work must use one profile, apply it to every child or use Solo when it cannot be supplied.

## Role instance lifecycle

Keep at most one child thread for each role during one lead Codex task. Spawn `executor`, `researcher`, `verifier`, or `operator` lazily after its trigger. Reuse that role thread through follow-up handoffs across repository tasks and inquiries, including after it reports completion.

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

Before delegating read-only work, the lead settles the inquiry, source priority, scope, return format, and stop condition. A read-only inquiry needs no task.

Executor receives exactly one durable task from the lead and never edits `tasks.csv`. It performs local implementation and fast targeted development checks. It returns one task checkpoint. The lead reviews architecture, scope, and diff once per returned checkpoint. Corrections return as a concise delta to the same Executor. Separate leads may each use one writing Executor only under separate owned tasks with disjoint paths.

Executor may choose local implementation mechanics inside the settled boundaries. It must stop and return when work exposes a missing architecture decision, interface or dependency change, public behavior change, acceptance change, path conflict, or work outside the allowed scope.

## Executor trigger and loop

In Assisted mode, spawn or reuse Executor when every condition is true:

1. an owned durable task and its before-write gate are active;
2. behavior, architecture, interfaces, and acceptance are settled;
3. the task has one coherent outcome and explicit allowed paths;
4. its proof is known;
5. it needs no user or lead decision.

A localized change in one file followed by one narrow proof command may stay with the lead. When any readiness condition is missing, the lead resolves the missing truth before execution. For ready work beyond that fast path, delegation is mandatory.

Keep one writing Executor active per lead. Reuse `executor` across repository tasks while its lead Codex task remains active. Give it one observable outcome, one architecture and invariant set, one related path group, one acceptance set, one proof surface, and one stop condition. Never send several durable tasks or an internal backlog.

Send:

```text
Role: Executor
Task: TASK-ID
Outcome: One observable result.
Architecture: Settled implementation boundary.
Interfaces and invariants: Lead-defined contracts.
Allowed paths: Related repository paths.
Acceptance: Observable acceptance criteria.
Proof: Exact targeted checks.
Stop conditions: Decisions that require the lead.
```

The child sends no periodic progress updates.

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

In Assisted or Focused mode, spawn or reuse Researcher when substantial multi-source, multi-repository, large-document, data, log, or noisy evidence collection would pollute lead context.
Keep one known-source fact with the lead.
Use the Researcher contract locally in Solo.
The lead supplies the question, decision informed, source priority, scope, stop condition, and return format.
Researcher is read-only and never edits repository files.
Researcher returns cited findings, conflicts, unknowns, and decision impact.
The lead evaluates sources and retains every decision.
If findings require repository writes, the lead starts or uses an owned task before recording them.
Reuse `researcher` across read-only inquiries. Send the current inquiry and changed assumptions in each handoff.

### Verifier

In Assisted or Focused mode, spawn or reuse Verifier when either condition is true:

1. code, configuration, schema, generated artifacts, or observable behavior changed and reached a coherent proof checkpoint;
2. promised proof requires multiple commands or produces output worth isolating and compressing.

A documentation-only change with one narrow proof command may stay with the lead. Verifier independently reruns acceptance-defining proof against the exact task checkpoint. It adds risk-based regression and skips Executor-only targeted checks. The full suite normally runs once under Verifier. The lead avoids repeating child commands except in Solo mode or to resolve conflicting evidence. Verifier consumes Operator evidence instead of repeating the operation. It returns operation pass/fail and exact evidence. It never repairs source or chooses task disposition.

### Operator

In Assisted or Focused mode, spawn or reuse Operator when a build, package, CI, deploy, flash, runtime, or smoke operation is ready and its procedure is guided or recorded under [operations.md](operations.md).

For an unknown first operation, the lead, user, or bounded Executor guides the exact attempt while Operator observes. Operator never invents a procedure, target, retry, or recovery rule. It returns operation status, artifacts, target, signals, and bounded logs. It never repairs source or chooses task disposition.

## Profiles

Never use `low` reasoning. Never silently reduce a requested or required profile.

Run `scripts/configure_codex.py` before the first assisted task. It registers `lean_sdlc_luna`. It also enables Multi-Agent V2 under the `agents` tool namespace. It exposes agent types and direct fallback controls. Restart Codex after configuration. Do not patch the model catalog.

| Child role | Required profile | Compatibility fallback |
| --- | --- | --- |
| Verifier | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Operator | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Executor | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |
| Researcher | `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` | GPT-5.6 Terra `xhigh` |

The profile receives the Executor, Researcher, Verifier, or Operator role through the spawn handoff. Use Luna only through `lean_sdlc_luna` at `max`. Use Terra only at `xhigh`, and only when the Luna profile is unavailable, unexposed, rejected, or when the user explicitly chooses the lower-latency fallback. Announce the substitution. Keep architecture, task setting, integration, and other consequential decisions with the lead.

## Spawn protocol

Before every spawn:

1. resolve the trigger, role, mode, user authority, and exposed models;
2. check for the existing fixed role thread and use a follow-up handoff when it is reachable;
3. use `task_name=executor`, `researcher`, `verifier`, or `operator` for the first spawn;
4. use `agent_type=lean_sdlc_luna` for the primary Luna route;
5. omit direct `model` and `reasoning_effort` fields for the primary Luna route because the named profile pins them;
6. set `fork_turns` to `none` for sidecars and normally for Executor;
7. use a bounded positive `fork_turns` for Executor only when those exact recent turns are required;
8. announce the failure and directly spawn `gpt-5.6-terra` at `xhigh` without `agent_type` when the Luna profile is absent, unexposed, or rejected;
9. keep the work with the lead when neither the required profile nor the Terra fallback is exposed.

Full-history inheritance is forbidden. The primary Luna route requires the named profile. The Terra fallback requires direct `model=gpt-5.6-terra` and `reasoning_effort=xhigh`. An automatic model default, inherited lead profile, silent fallback, effort downgrade, or incompatible fork is a routing failure.

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
