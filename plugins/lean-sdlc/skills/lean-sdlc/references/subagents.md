# Subagent Policy

This file is the canonical policy for every Lean-SDLC child agent. Other references may invoke a role or trigger from here; they must not redefine child-agent behavior.

## Roles and modes

- Lead: owns user dialogue, scope, decisions, task state, integration, and closeout.
- Verifier sidecar: runs checks and returns evidence.
- Operator sidecar: runs guided or recorded operations and compresses their output.
- Worker: produces one bounded deliverable under explicit ownership.

Assisted is the default mode: required sidecars run lazily and eligible Workers may be used. Focused keeps required sidecars and disables Workers. Solo disables every child; the lead follows the same check and operation contracts locally.

The user's mode remains active for the task until changed. An explicit user profile pins the lead. When the user says all work must use one profile, apply it to every child or use Solo when it cannot be supplied.

## Orchestration Gate

Before Deliver or the first delegated read-only operation, state:

`Mode | Required sidecars | Eligible Workers | Reason`

Apply the gate again only when task scope, mode, proof, or available agents materially changes. Skipping a mandatory sidecar trigger or spawning a Worker outside its eligibility gate is a workflow failure.

## Mandatory sidecar triggers

Spawn a sidecar only when its first command is ready. Reuse the same named sidecar while task, role, repository, and assumptions remain stable.

### Verifier

In Assisted or Focused mode, spawn or reuse Verifier when either condition is true:

1. code, configuration, schema, generated artifacts, or observable behavior changed and reached a coherent proof checkpoint;
2. promised proof requires multiple commands or produces output worth isolating and compressing.

A documentation-only change with one narrow proof command may stay with the lead. Verifier runs tests, lint, type checks, structural checks, and diff inspection. It returns operation pass/fail and exact evidence. It never repairs source or chooses task disposition.

### Operator

In Assisted or Focused mode, spawn or reuse Operator when a build, package, CI, deploy, flash, runtime, or smoke operation is ready and its procedure is guided or recorded under [operations.md](operations.md).

For an unknown first operation, the lead, user, or bounded Worker guides the exact attempt while Operator observes. Operator never invents a procedure, target, retry, or recovery rule. It returns operation status, artifacts, target, signals, and bounded logs. It never repairs source or chooses task disposition.

## Worker eligibility

Spawn a Worker only in Assisted mode and only when every condition is true:

1. the deliverable is independent and bounded;
2. owned files, interfaces, or outputs are explicit;
3. acceptance and proof are known;
4. no unresolved product, architecture, safety, or integration decision is delegated;
5. assignment plus integration costs less context or wall time than lead execution.

One Worker is the normal limit. A second is allowed only for independent scopes with disjoint outputs. Parallel writers require separate owned tasks and disjoint paths. Keep quick, coupled, critical-path, or explanation-heavy work with the lead.

Workers never own user communication, task state, cross-scope integration, or closeout.

## Profiles

Never use `low` reasoning. Never silently reduce a requested or required profile.

| Child work | Required profile | Fallback |
| --- | --- | --- |
| Verifier | GPT-5.6 Luna `max` | GPT-5.6 Terra `high` |
| Operator | GPT-5.6 Luna `max` | GPT-5.6 Terra `high` |
| Narrow mechanical Worker with exact proof | GPT-5.6 Luna `max` | GPT-5.6 Terra `high` |
| Worker requiring broad engineering judgment | GPT-5.6 Terra `high` | Keep with lead |

Use Luna only at `max`. Use the fallback only when the required profile is unavailable on the current spawn surface, and make the substitution explicit.

## Spawn protocol

Before every spawn:

1. resolve the trigger, role, mode, user authority, and exposed models;
2. explicitly pass `model` and `reasoning_effort`; never rely on parent, configured, or automatic defaults;
3. set `fork_turns` to `none` for sidecars and normally for Workers;
4. use a bounded positive `fork_turns` for a Worker only when those exact recent turns are required;
5. keep the work with the lead when neither the required profile nor its fallback is exposed.

Full-history inheritance is forbidden. An omitted model, omitted reasoning effort, inherited lead profile, silent effort downgrade, or incompatible fork is a routing failure.

Send:

`Role | Task | Trigger | Checkpoint | Scope | Allowed writes | Expected result | Stop conditions`

Return:

`Status | Evidence or artifacts | Issue or risk | Next`

Status describes the delegated operation or deliverable, never task disposition. Reference files and saved logs instead of pasting large output. Preserve exact decisions supplied by the lead, commands, fingerprints, failures, and evidence; omit exploration chatter.

The lead reviews and consumes every return before integration or closeout.

## Authority and isolation

- Only the lead spawns, steers, or redirects children.
- Depth is one. Children never spawn or hand work directly to another child.
- Sidecars do not edit source or `tasks.csv`; expected temporary and build artifacts are allowed.
- Workers edit only their assigned scope. A writing Worker must own a separate active task and disjoint paths.
- Children stop when scope, assumptions, checkpoint identity, or authority becomes unclear.

## Checkpoint barrier

1. Pause relevant writers.
2. Identify the checkpoint by commit or exact working-tree fingerprint.
3. Send the identity and narrow command or procedure.
4. Require the sidecar to confirm the identity before acting.
5. Invalidate the result after any relevant source change.

## Reuse, context, and loss recovery

Keep stable role instructions, tools, and profiles unchanged during a task. Put volatile task data last and send only incremental deltas to a reused child.

Agent lifetime is not durable. A wait timeout may only end the wait, and a child may disappear. Store durable knowledge in repository documents. Rehydrate a replacement from its role, active task, relevant repository procedure, current checkpoint, and latest unresolved result.

Treat prompt-cache reuse as best effort. Never preserve stale context, create unnecessary agents, or weaken verification for a possible cache hit.
