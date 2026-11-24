# Recorded operations

Lead runs authorized procedures, including built-in checks. Maintainer documents confirmed procedures when needed. Do not split procedures among agents merely for tests. Assign Verifier read-only validation for missing independent proof, changed behavior or risk, or disputed evidence. Lead does not repeat that run.

## Learn and record

Record guided success before replay. Changed inputs or contracts make a result stale.

Record the first successful build, package, deploy, flash, runtime, or smoke procedure in `docs/OPERATIONS.md` with commands and results. Use `OPS-*` for independent targets or recovery details. Follow documentation rules for indexes and sizing.

A record contains purpose, maintenance owner, status, canonical command, explicit inputs, safe defaults, prerequisites, ordered steps, exact target, artifacts, success signal, known failure signal, authorized recovery, and last verified context. Do not record an unsuccessful guess as a working procedure.

## Replay and authority

Read the valid procedure; reuse project commands. An operation record or script never grants permission.

Honor explicit current or standing authority for the same scope and target. This can include build, deployment, publication, commits, and pushes. Do not ask again when the authority remains valid. Do not infer those actions from a request for an idea or code change.

Run one state-changing operation at a time for the same target. Use the accepted source identity. Do not guess a target, silently alter steps, or retry a state-changing failure without an authorized recovery rule. Reuse valid artifact proof; do not repeat it solely to add a support handoff. A successful exit is sufficient only when the procedure's success checks establish the required result. Missing required proof blocks completion.

Design recovery to inspect the destination’s durable state. On an authorized retry, apply only confirmed missing effects. If completion is uncertain, stop before repeating the action. If a recorded failure matches, use only its already-authorized recovery. For an unknown failure, changed target, stale procedure, or source defect, stop the procedure and preserve the evidence. Lead diagnoses within current authority; a changed target or unapproved recovery requires user direction.

Cancellation follows the common protocol: check the underlying process or command, not only the agent status. Keep uncertain targets blocked. Relevant source or target changes invalidate previous operation results.

## Reusable commands

Do not automatically discover routines or suggest scripts. Retain documented commands. Create reusable scripts only on explicit request.

Lead implements such a script using an existing command, installed tool, or the smallest necessary code. Verifier runs a focused check. Require explicit inputs, target validation, stable exit status, noninteractive behavior, atomic output where practical, and bounded output. Use dry-run when mutation risk warrants it.

## Result

Return status, target, artifact, and next Lead action. Keep successful raw logs out of routine reports. Retain failure logs only as useful temporary evidence. Redact tokens, passwords, keys, authorization headers, connection strings, and secret environment values.

Report ready for testing only when the actual artifact or deployment and required immediate checks are ready. Final delivery also requires the agreed integration proof, documentation, and ledger reconciliation.
