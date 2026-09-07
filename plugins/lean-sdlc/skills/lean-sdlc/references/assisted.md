# Assisted Mode

The Lead owns intent, decisions, permissions, production code, core tests, task ownership, acceptance, and closure.
Read `AGENTS.md`, `docs/PROJECT.md`, and the task helper's compact `open` view. Use `show TASK-ID` for relevant detail.
Discussion stays read-only. Explicit implementation authority is required before task creation or other project changes.

## Work from acceptance

1. Read the original request, affected code, and callers. Resolve material uncertainty and diagnose failures before choosing a change.
2. Define observable acceptance before implementation. Retain every requested deliverable, exact example, location, and preserved behavior in the existing task acceptance.
3. For testable behavior, prepare or identify the acceptance check before changing production code. Cover all requested behavior, not only the easiest example.
4. Check that new assertions detect the missing behavior in the original implementation. Existing regression checks may already pass. Do not force irrelevant failures.
5. Implement the smallest change that satisfies those checks. Keep requested documentation inside the same outcome.

A requirement about runtime output is not satisfied by placing that text only in documentation. A task summary cannot remove original requirements.
Use ordinary project tests or a small standard-library check. Do not create another acceptance registry, task schema, framework, or mandatory document.

## Own the change

Show one concise plan covering purpose, scope, approach, and proof. Classify the task once:
Routine is bounded, understood, and recoverable. Critical includes consequential data, security, irreversible, shared-contract, concurrency, or subtle architectural risk.
Read `backlog` before new Standard work; only a direct user request can add or promote it.

Start or claim an owned task before editing tests, source, or documents. Preparation before task start is read-only.
Use the exact supplied helper paths:

- New task: `tasks.py --repo <repo-root> start --owner OWNER --title "..." --context Project --acceptance "..." --proof "..."`.
- Existing task: `tasks.py --repo <repo-root> start TASK-ID --owner OWNER`.
- Before first non-control write: `lean_check.py <repo-root> --before-write --task TASK-ID --owner OWNER`.
- Completion: `tasks.py --repo <repo-root> close TASK-ID --owner OWNER --evidence "..."`.

Dependencies must be Done before start. Each task represents one independently acceptable outcome.
Keep root `tasks.csv` authoritative. Project unresolved task IDs and exact titles into `update_plan` when available.
Use [plan.md](plan.md) for task splitting, dependency decisions, or Quick Fix eligibility, not for every settled task.

## Establish completion

Compare the finished files and test coverage with the original request, not only the task summary.
Inspect relevant callers, failure cases, complexity, documentation, and integration before completion.
For every requirement, identify its actual result and proof. Missing, failed, or untested acceptance remains incomplete.

Run documentation commands exactly as a user would in the documented environment.
If a command fails, fix the document or document and verify its prerequisite. Do not create an undocumented alias or environment workaround to call it passed.
Preserve any explicitly required literal example while documenting a usable verified alternative when necessary.

Choose proof from the changed boundary. One command can establish acceptance and regression.
Keep the proof owner, purpose, and relevant invalidation inputs in existing task facts or cited evidence.
Run the full suite for migrations, releases, broad shared contracts, build-graph changes, explicit requirements, or absent reliable selectors.
Reuse successful proof while source, dependencies, environment, configuration, toolchain, and target remain valid. Repeat affected proof after changes or disputed evidence.
Keep failed logs. Do not schedule the same final gate separately for both Lead and Verifier.

Routine work can use Lead proof. Critical, combined parallel, release, or disputed work requires an independent Verifier.
Give that Verifier the original request, current acceptance, actual changes, relevant callers, and existing evidence.
The Verifier follows [verify.md](verify.md) and checks actual behavior and test adequacy, not the Lead's confidence.
Freeze review inputs. Correct blocking findings, then refresh affected proof. Optional hardening does not redefine acceptance.

Only when current acceptance and required proof pass, give one alignment signoff and close with evidence.
Only the owner closes. A direct-user override requires an explicit reason. Delivery and verified acceptance are distinct.
Report the result, checks, documentation, remaining limits, and actual delivery status. Never claim an unperformed release.

## Support and changed intent

The Lead may use Maintainer for bounded documents or mechanics, Scout for substantial unknowns, and Verifier for independent proof.
Do not use Engineer or custom roles. Children cannot change production code, acceptance, permissions, tasks, or session state, or allocate children.
Use [support.md](support.md) only when assigning support; give the child [child.md](child.md) and its bounded assignment.
Do small chores directly. Reuse reachable support. Keep mutable paths separate and count all descendants against native capacity.
Do not create branches or worktrees for parallelism. Silence or wait expiry does not prove failure.

The latest valid request controls unfinished work. Send changed scope to affected children before dependent actions.
Cancel obsolete work through native messages and safe interruption, including active dependent commands. Late results cannot restore canceled authority.
For running commands, apply [support.md](support.md#command-cancellation). An agent interrupt alone does not prove that its command stopped.
An explicit stop ends nonessential work. Do not delay it for obsolete cleanup or paperwork. Record unfinished work without forcing Done.
A failed metadata update stops dependent actions. A status question does not cancel work.
Use short, active American English and preserve exact identifiers. Report decisions and evidence, not private reasoning.
