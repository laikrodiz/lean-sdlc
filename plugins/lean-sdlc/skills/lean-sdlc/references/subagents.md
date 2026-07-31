# Subagent Policy

This file is the canonical policy for every Lean-SDLC child agent. Other references may invoke a role or trigger from here; they must not redefine child-agent behavior.

## Roles and modes

- Lead: owns user dialogue, behavior, architecture, interfaces, task state, acceptance, proof, integration, and closeout. Preserve the user-selected lead profile.
- Executor: a reusable task-scoped child that completes one settled execution unit at a time.
- Verifier sidecar: runs checks and returns evidence.
- Operator sidecar: runs guided or recorded operations and compresses their output.

Assisted is the default mode: required sidecars run lazily, and a ready execution unit beyond the direct fast path must use Executor. Focused keeps required sidecars and disables Executor. Solo disables every child; the lead follows the same execution, check, and operation contracts locally.

The user's mode remains active for the task until changed. An explicit user profile pins the lead. When the user says all work must use one profile, apply it to every child or use Solo when it cannot be supplied.

## Orchestration Gate

Before Deliver or the first delegated read-only operation, state:

`Mode | Required sidecars | Executor action | Reason`

Apply the gate again only when task scope, mode, proof, or available agents materially changes. Skipping a mandatory sidecar, skipping a required Executor handoff, or sending multiple execution units in one handoff is a workflow failure.

## Lead authority

Before delegating, the lead settles the observable outcome, architecture, interfaces and invariants, dependencies, allowed paths, acceptance, proof, and stop conditions. The lead creates and owns the durable task, runs the before-write gate, reviews every return for architectural and scope compliance, integrates the result, and decides whether to correct, continue, or close.

A sequential Executor works under the lead-owned task and never edits `tasks.csv`. Its execution units are transient checkpoints, not ledger rows. Separate leads may each use one writing Executor only under separate owned tasks with disjoint paths.

Executor may choose local implementation mechanics inside the settled boundaries. It must stop and return when work exposes a missing architecture decision, interface or dependency change, public behavior change, acceptance change, path conflict, or work outside the allowed scope.

## Executor trigger and loop

In Assisted mode, spawn or reuse Executor when every condition is true:

1. an owned task and its before-write gate are active;
2. behavior, architecture, interfaces, and acceptance are settled;
3. the next unit has one coherent outcome and explicit allowed paths;
4. its proof is known;
5. it needs no user or lead decision.

A localized change in one file followed by one narrow proof command may stay with the lead. When any readiness condition is missing, the lead resolves the missing truth before execution. For ready work beyond that fast path, delegation is mandatory.

Keep one writing Executor active per lead. Reuse the same named Executor for the task while its role, repository, architecture, and assumptions remain stable. Give it enough related work to justify the handoff: one observable outcome, one architecture and invariant set, one related path group, and one proof surface. Never send a backlog or multiple execution units.

Send:

`Role | Task | Checkpoint | Outcome | Architecture | Interfaces and invariants | Allowed paths | Proof | Stop conditions`

Executor may iterate within that unit until its proof passes while scope remains unchanged. It returns:

`Done or Blocked | Files changed | Proof result | Deviation or decision needed`

After every return, the lead reviews architecture and scope, then applies the Verifier checkpoint. Only an accepted result may unlock the next execution unit.

## Mandatory sidecar triggers

Spawn a sidecar only when its first command is ready. Reuse the same named sidecar while task, role, repository, and assumptions remain stable.

### Verifier

In Assisted or Focused mode, spawn or reuse Verifier when either condition is true:

1. code, configuration, schema, generated artifacts, or observable behavior changed and reached a coherent proof checkpoint;
2. promised proof requires multiple commands or produces output worth isolating and compressing.

A documentation-only change with one narrow proof command may stay with the lead. Verifier runs tests, lint, type checks, structural checks, and diff inspection. It returns operation pass/fail and exact evidence. It never repairs source or chooses task disposition.

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

The profile receives the Executor, Verifier, or Operator role through the spawn handoff. Use Luna only through `lean_sdlc_luna` at `max`. Use Terra only at `xhigh`, and only when the Luna profile is unavailable, unexposed, rejected, or when the user explicitly chooses the lower-latency fallback. Announce the substitution. Keep architecture, task setting, integration, and other consequential decisions with the lead.

## Spawn protocol

Before every spawn:

1. resolve the trigger, role, mode, user authority, and exposed models;
2. use `agent_type=lean_sdlc_luna` for the primary Luna route;
3. omit direct `model` and `reasoning_effort` fields for the primary Luna route because the named profile pins them;
4. set `fork_turns` to `none` for sidecars and normally for Executor;
5. use a bounded positive `fork_turns` for Executor only when those exact recent turns are required;
6. announce the failure and directly spawn `gpt-5.6-terra` at `xhigh` without `agent_type` when the Luna profile is absent, unexposed, or rejected;
7. keep the work with the lead when neither the required profile nor the Terra fallback is exposed.

Full-history inheritance is forbidden. The primary Luna route requires the named profile. The Terra fallback requires direct `model=gpt-5.6-terra` and `reasoning_effort=xhigh`. An automatic model default, inherited lead profile, silent fallback, effort downgrade, or incompatible fork is a routing failure.

After a Codex update, run one bounded profile smoke test before the first required Luna handoff. Confirm the child reports Luna `max`. If the route fails, announce the failure and use the Terra fallback.

For a sidecar, send:

`Role | Task | Trigger | Checkpoint | Scope | Allowed writes | Expected result | Stop conditions`

Require:

`Status | Evidence or artifacts | Issue or risk | Next`

Status describes the delegated operation or deliverable, never task disposition. Reference files and saved logs instead of pasting large output. Preserve exact decisions supplied by the lead, commands, fingerprints, failures, and evidence; omit exploration chatter.

The lead reviews and consumes every return before integration or closeout.

## Authority and isolation

- Only the lead spawns, steers, or redirects children.
- Depth is one. Children never spawn or hand work directly to another child.
- Sidecars do not edit source or `tasks.csv`; expected temporary and build artifacts are allowed.
- Executor edits only the assigned paths under the active lead-owned task.
- Children stop when scope, assumptions, checkpoint identity, or authority becomes unclear.

## Checkpoint barrier

1. Pause relevant writers.
2. Identify the checkpoint by commit or exact working-tree fingerprint.
3. Send the identity and narrow command or procedure.
4. Require the sidecar to confirm the identity before acting.
5. Invalidate the result after any relevant source change.

## Reuse, context, and loss recovery

Keep stable role instructions, tools, profiles, architecture, and invariants unchanged during a task. Put volatile unit data last and send only incremental deltas to a reused child.

Agent lifetime is not durable. A wait timeout may only end the wait, and a child may disappear. Store durable knowledge in repository documents. Rehydrate a replacement from its role, active task, relevant repository procedure, current checkpoint, and latest unresolved result.

Treat prompt-cache reuse as best effort. Never preserve stale context, create unnecessary agents, or weaken verification for a possible cache hit.
