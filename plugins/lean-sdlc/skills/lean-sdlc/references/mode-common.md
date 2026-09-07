# Shared Boundaries

These rules apply to every mode. The Lead retains intent, architecture, permissions, task ownership, acceptance, and final judgment.
Preserve the selected Lead model and effort. Fresh state defaults to Assisted. Legacy `assisted` maps to Delegating; legacy `solo` stays Solo.
Mode state belongs to one session owner. An older owner's selection does not select a mode for a new session.

## Current request

Keep the current outcome, authorized scope, required evidence, and stopping condition clear in existing task or handoff facts.
Record material changes once. Do not create a history store, receipt system, or second task-status record.

When the user changes the request, update affected assignments and their request revision before further dependent actions.
The latest valid user intent supersedes earlier request-specific procedure. Changed or canceled acceptance invalidates earlier evidence for that acceptance.
Cancel obsolete work through native messages and safe interruption. Stop already-running dependent work. Start no new action under a canceled assignment.
For running commands, apply [support.md](support.md#command-cancellation). An agent interrupt alone does not prove that its command stopped.
Late results can supply evidence, but cannot restore canceled authority. An open ledger task does not authorize canceled work.
Status questions do not cancel work. After resume or compaction, restore the latest request before unfinished procedural steps.

Delivery, verified acceptance, and task `Done` are distinct facts. Return the requested result with its actual verification status.
An explicit stop ends nonessential background work too. Perform only necessary safe interruption before ending the work.
Do not delay handoff for obsolete cleanup, documentation, or earlier acceptance requirements. Record unfinished work without forcing `Done`.
If a metadata update fails, stop dependent actions and report the failure. Do not start a cleanup loop.

## Task and proof gates

Read `AGENTS.md`, `docs/PROJECT.md`, and the compact `tasks.py --repo <repo-root> open` view at startup.
Use `show TASK-ID` for relevant detail. Do not load full completed history.
Discussion remains read-only. Require explicit implementation authority before task creation or repository changes.

Before mutation, establish `why -> what -> how -> proof` and show a concise plan.
Classify each independently accepted task once as Routine or Critical, with a short reason.
Before new Standard work, check the compact `backlog` view for related work. Only a direct user request can add or promote Backlog.
Use [plan.md](plan.md) for task sizing, dependencies, Quick Fix eligibility, and plan-view projection.

Use the packaged tasks helper for every ledger mutation. Start or claim an owned `In Progress` task with acceptance and proof.
Use Context `Project` for Standard work. Each task represents one independently acceptable implementation checkpoint.
Project unresolved IDs and exact titles into `update_plan` when available. The ledger remains authoritative if that tool is unavailable.
Before the first non-control write, run `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" --before-write --task TASK-ID --owner OWNER`.
Do not change another writer's assigned paths. Diagnose an unknown failure cause before attempting a fix.

Verify actual changes, required behavior, relevant regressions, and documentation parity. Critical work requires independent evidence, including Lead-written work.
Follow [verify.md](verify.md) for independent review and closure. Only the owner closes with evidence; direct-user override requires a recorded reason.
Reuse proof only while relevant source, dependencies, configuration, environment, toolchain, and target inputs remain valid.
Repeat affected checks after relevant changes, failures, or disputed evidence. Do not repeat successful checks merely to fill another stage.

## Communication

Use short, active American English and one term per meaning. Preserve exact code, identifiers, paths, and protocol fields.
Apply ASD-STE100 Issue 9 sentence limits: procedural sentences at most 20 words; descriptive sentences at most 25 words.
Do not claim certified compliance without a checker. Report decisions and evidence, not private chain-of-thought.
Use a small Mermaid diagram only when it clarifies a relationship. Never require a diagram for routine work.
