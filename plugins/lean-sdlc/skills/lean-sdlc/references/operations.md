# Operations

The Operator sidecar owns repeatable command execution and log compression, while the lead owns procedure approval and task decisions.

## Learn, then repeat

An operation moves through:

`unknown -> guided success -> recorded -> verified -> repeatable -> stale`

For the first build, package, deploy, flash, runtime, or smoke operation:

1. The lead, user, or bounded worker guides the exact attempt.
2. The Operator observes commands, inputs, target, success signal, artifacts, and recovery facts.
3. After success, the Operator returns a short procedure draft.
4. The lead records it in optional `docs/OPERATIONS.md` under the active task.
5. Later Operator runs replay the recorded procedure exactly.

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

Request:

`Task | operation | checkpoint | exact target | expected signal`

Return:

`Status | source fingerprint | artifact path or hash | target | signal | saved failure log | next`

Run one state-changing operation at a time for the same `task + operation + target`. Never guess a target, silently change a procedure, or retry a state-changing failure without authority and a recorded recovery rule.

Discard successful raw logs after the compact result. Keep failed logs only as temporary artifacts and report their path. The Operator reports failure; Diagnose owns root cause and Deliver owns repairs.

## Delivery classes

Infer the operation sequence from task proof:

- routine: Deliver -> Verify;
- artifact: Deliver -> Verify -> build or package;
- operational: Deliver -> Verify -> build -> deploy or flash -> smoke.

In Solo mode, the lead follows the same recorded procedures and return fields locally.
