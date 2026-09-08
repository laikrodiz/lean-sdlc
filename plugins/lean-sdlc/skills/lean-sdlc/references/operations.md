# Recorded operations

Read this reference when learning or replaying a project procedure. Lead owns domain decisions. Maintainer records and runs authorized bounded operations. Verifier runs test steps, including smoke checks. Agree on ownership before a procedure that combines build, deployment, and tests.

## Learn and record

A procedure progresses from unknown, through guided success and a verified record, to repeatable use. Changed inputs or contracts make it stale.

For the first guided build, package, deploy, flash, runtime, or smoke procedure, record the successful commands and result in `docs/OPERATIONS.md`. Use an `OPS-*` document when independent target or recovery detail needs its own subject. Follow the documentation reference for indexes and sizing.

A record contains purpose, maintenance owner, status, canonical command, explicit inputs, safe defaults, prerequisites, ordered steps, exact target, artifacts, success signal, known failure signal, authorized recovery, and last verified context. Do not record an unsuccessful guess as a working procedure.

## Replay and authority

Read the existing valid procedure first. Reuse project commands and scripts. An operation record or script never grants permission.

Honor explicit current or standing authority for the same scope and target. This can include build, deployment, publication, commits, and pushes. Do not ask again when the authority remains valid. Do not infer those actions from a request for an idea or code change.

Run one state-changing operation at a time for the same target. Use the accepted source identity. Do not guess a target, silently alter steps, or retry a state-changing failure without an authorized recovery rule.

If a recorded failure matches, use only its already-authorized recovery. For an unknown failure, changed target, stale procedure, or source defect, stop and return evidence to Lead. Lead owns diagnosis and repairs.

Cancellation follows the common protocol: check the underlying process or command, not only the agent status. Keep uncertain targets blocked. Relevant source or target changes invalidate previous operation results.

## Reusable commands

Automatic routine discovery and automatic script-creation suggestions are not part of this workflow. Existing commands remain usable and documented. Create a new reusable script only when the user explicitly requests it.

Lead implements such a script using an existing command, installed tool, or the smallest necessary code. Verifier runs a focused check. Require explicit inputs, target validation, stable exit status, noninteractive behavior, atomic output where practical, and bounded output. Use dry-run when mutation risk warrants it.

## Result

Return status, target, artifact, and next Lead action. Keep successful raw logs out of routine reports. Retain failure logs only as useful temporary evidence. Redact tokens, passwords, keys, authorization headers, connection strings, and secret environment values.

Report ready for testing only when the actual artifact or deployment and required immediate checks are ready. Final delivery also requires the agreed integration proof, documentation, and ledger reconciliation.
