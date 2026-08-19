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

Use `docs/operations/OPS-*.md` for a procedure with an independent target, recovery rule, lifecycle, or useful standalone detail. Create `docs/operations/INDEX.md` with the first numbered procedure. Keep `docs/OPERATIONS.md` for the first simple recorded procedure and shared operation map.

## Automation lifecycle

Reuse recorded operations as the only automation catalog. Do not add another file, registry, hook, state field, role, mode, dependency, or runtime framework.

A stable repeated mechanic may include repository checks, transforms, reports, build, package, deploy, flash, runtime, smoke work, or repeated external-tool procedures. Never automate product, architecture, permission, security, acceptance, or conflict decisions. A script never grants authority.

Raise a transient candidate after a second equivalent successful execution or direct evidence that the mechanic will recur. Candidates do not enter durable docs or Backlog automatically. The Architect approves the contract before scripting.

Use this selection ladder, stopping at the first existing option:

1. existing project command or target;
2. existing script;
3. native or installed tool;
4. smallest new script.

Engineer implements an approved script and one focused runnable check. Maintainer records and later replays the canonical command in `docs/OPERATIONS.md` or an existing `OPS-*` document. Later work reads recorded operations first and uses the valid canonical command. Solo follows the same record.

Maintainer marks an automation as stale when its contract, dependency, environment, target, or output changes. Architect approves meaning changes.

## Runtime contract

Every approved script must:

- take explicit inputs and safe defaults;
- validate the target;
- return a stable exit status;
- run noninteractive;
- write output atomically when practical;
- omit secrets and machine-specific paths;
- bound default output and include detailed logs only on failure or explicit request.

Use dry-run only when mutation risk is meaningful.

## Failure routing

A transient signal may retry only under recorded recovery. A recorded failure follows authorized recovery. A script defect goes to Engineer. A changed contract or unknown cause stops and returns to Architect/Diagnose.

## Procedure record

For each operation, keep:

- status and maintenance owner;
- purpose;
- canonical command;
- explicit inputs and safe defaults;
- outputs and artifacts;
- exact target;
- prerequisites;
- exact ordered steps;
- success signal;
- recorded operation failure signal and authorized recovery or rollback rule;
- last verified context.

Do not store secrets. Redact tokens, passwords, keys, authorization headers, connection strings, and secret environment values from procedures and reports.

## Run contract

Keep the task, operation, source identity, target, expected signal, and recovery context in the internal machine handoff. Keep Verifier fingerprints local. Omit them from visible operation reports.

Visible operation result order: `<status> -> <target> -> <artifact> -> <next Architect action>`. Add failure-log context only when needed.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

Run one state-changing operation at a time for the same `task + operation + target`. Never guess a target, silently change a procedure, or retry a state-changing failure without authority and a recorded recovery rule.

Maintainer classifies failures only by matching a recorded operation failure signal. It runs only an already-authorized recorded recovery. Unknown, ambiguous, source-changing, or new retry behavior stops and routes to Diagnose/Scout and Architect.

Discard successful raw logs after the compact result. Keep failed logs only as temporary artifacts and report their path. The Maintainer reports failure; Diagnose owns root cause and Deliver owns repairs.

## Delivery classes

Infer the operation sequence from task proof:

- routine: Deliver -> Verify;
- artifact: Deliver -> Verify -> build or package;
- operational: Deliver -> Verify -> build -> deploy or flash -> smoke.

In Solo mode, the lead follows the same recorded procedures and visible result order.
