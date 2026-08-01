# Operations

Apply the Maintainer trigger, authority, profile, spawn, and handoff rules from [subagents.md](subagents.md). This file owns only how project-specific procedures are learned and repeated.

## Learn, then repeat

An operation moves through:

`unknown -> guided success -> recorded -> verified -> repeatable -> stale`

For the first build, package, deploy, flash, runtime, or smoke operation:

1. The lead, user, or bounded worker guides the exact attempt.
2. The Maintainer observes commands, inputs, target, success signal, artifacts, and recovery facts.
3. After success, the Maintainer returns a short procedure draft.
4. The lead records it in optional `docs/OPERATIONS.md` under the active task.
5. Later Maintainer runs replay the recorded procedure exactly.

Update the recorded procedure after another guided success when reality changes. Stop when a procedure is missing, ambiguous, or stale.

## Procedure record

For each operation, keep:

- purpose;
- prerequisites;
- exact ordered steps;
- success signal;
- artifact and exact target;
- recovery or rollback rule;
- last verified context.

Do not store secrets. Redact tokens, passwords, keys, authorization headers, connection strings, and secret environment values from procedures and reports.

## Run contract

Request these labeled fields on separate lines:

```text
Task: TASK-ID
Operation: Operation name.
Checkpoint: Exact source fingerprint.
Exact target: Target identifier.
Expected signal: Observable success signal.
```

Return these labeled fields on separate lines:

```text
Status: Operation status.
Source fingerprint: Exact source fingerprint.
Artifact path or hash: Artifact reference, or None.
Target: Target identifier.
Signal: Observed success or failure signal.
Saved failure log: Temporary log reference, or None.
Next: Required Architect action, or None.
```

Run one state-changing operation at a time for the same `task + operation + target`. Never guess a target, silently change a procedure, or retry a state-changing failure without authority and a recorded recovery rule.

Discard successful raw logs after the compact result. Keep failed logs only as temporary artifacts and report their path. The Maintainer reports failure; Diagnose owns root cause and Deliver owns repairs.

## Delivery classes

Infer the operation sequence from task proof:

- routine: Deliver -> Verify;
- artifact: Deliver -> Verify -> build or package;
- operational: Deliver -> Verify -> build -> deploy or flash -> smoke.

In Solo mode, the lead follows the same recorded procedures and return fields locally.
