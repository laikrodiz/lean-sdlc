---
name: lean-sdlc
description: Run Lean-SDLC when the user explicitly invokes Lean-SDLC or `$lean-sdlc`, or when repository AGENTS.md requires Lean-SDLC. Require explicit implementation authority, the visible Plan contract, an owned task before writes, and evidence-based completion. Do not invoke implicitly for read-only work outside a Lean-SDLC repository.
---

# Lean-SDLC

Keep current intent, implementation, and proof coherent. The Lead is the existing Architect role, not a model selection.

## Child entry

If the Architect assigned you a child role, read [child.md](references/child.md) and follow that assignment. The Architect startup and orchestration below do not apply to children. Use supplied roots and task facts; ask for missing facts instead of searching for helpers.

## Architect startup

At lifecycle startup, use exact startup fields from the lifecycle system message.
The system message supplies `Repository root`, `Skill root`, `Tasks helper`, `Check helper`, `State helper`, `Owner`, `Mode`, `Active mode`, and `Child tier`.
The `Skill root` is the parent of the loaded `SKILL.md`.
If any field is absent, run `python3 "<directory containing the loaded SKILL.md>/scripts/session_state.py" --context`.
Use the existing `CODEX_SESSION_ID`.
Never set, replace, or invent `CODEX_SESSION_ID`.
The fallback fails when `CODEX_SESSION_ID` is absent.
Only this fallback returns structured JSON with snake_case fields: `repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, `mode`, `active_mode`, and `tier`.
Use returned fields, paths, and owner exactly.
Never reconstruct paths, shorten cache paths, search for helpers, or use placeholder owners.
If the checker reports a missing, invalid, or stale managed startup block, run `python3 "<skill-root>/scripts/init_repo.py" "<repo-root>" --repair-startup --task TASK-ID --owner OWNER` after task start and before the general before-write gate. Treat this repair as a control transaction; it changes only that block, and normal initialization remains create-only.

- `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" <command>` for ledger commands.
- `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" --before-write --task TASK-ID --owner OWNER` for repository checks before a write.
- `python3 "<skill-root>/scripts/session_state.py" --owner OWNER <options>` for session state.

Supply children with task facts, assigned paths, acceptance, proof, and both roots.

## Select the workflow

Use the explicit mode or restored selection. Preserve the Lead's selected model and effort; fresh sessions default to Assisted.
`Active mode: none` or JSON `active_mode: null` means no mode is locked. Honor an explicit mode request before `--begin`.
The default `Mode: assisted` does not mean Assisted is already active. Only a nonempty `active_mode` prevents a mode change.
For authorized implementation, select and lock the mode before loading workflow instructions:
`python3 "<skill-root>/scripts/session_state.py" --owner OWNER --mode assisted|delegating|solo --begin`.
An active session cannot change mode. Invalid state or conflicting legacy instructions stop affected work.
Compare repository mode names, ownership rules, and instruction paths with the selected contract before task creation or handoff.
Do not follow a legacy reference into an unselected mode. Report the conflict and obtain reconciliation authority; do not switch modes or rewrite custom rules silently.
The state helper rejects legacy or unknown contract cores at mode activation. An explicitly authorized contract upgrade is a control transaction; use [repository-contracts.md](references/repository-contracts.md).

Read exactly the selected workflow:

- **Assisted:** [assisted.md](references/assisted.md). Its self-contained contract includes the common gates and standard support.
- **Delegating:** Read [mode-common.md](references/mode-common.md), then [delegating.md](references/delegating.md).
- **Solo:** Read [mode-common.md](references/mode-common.md), then [solo.md](references/solo.md).

Do not load other mode policies. Do not additionally load `mode-common.md` or `support.md` for ordinary Assisted work.
After startup, resume, clear, compaction, or a skill upgrade, restore current intent and the selected contract.
Reuse unchanged instructions that remain in context.

## Stop active work

A stop request cancels the assignment, including its running commands. Command termination remains part of that stop request.
"Do not wait for completion" excludes the obsolete result, not command-cancellation evidence. Obtain only the evidence needed to stop safely.
Before interrupting a child that owns a running command, cancel and verify the command through [support.md](references/support.md#command-cancellation).
Then interrupt the child. Do not infer command termination from an agent's interrupted status.
An explicit stop does not authorize unrelated cleanup, tests, task closure, or later restart.

## Conditional references

Read only the reference needed for an unresolved decision or required proof. Reuse settled facts instead of restarting the workflow.

- [shape.md](references/shape.md): unclear intent, scope, or authority.
- [decide.md](references/decide.md): a durable technical choice.
- [plan.md](references/plan.md): task sizing, dependencies, Quick Fix, or plan-view details.
- [diagnose.md](references/diagnose.md): an unknown failure cause.
- [deliver.md](references/deliver.md): implementation checkpoints.
- [verify.md](references/verify.md): acceptance, independent proof, and closure.
- [operations.md](references/operations.md): an authorized build, release, or other recorded operation.
- [repository-contracts.md](references/repository-contracts.md): initialization, legacy migration, or document ownership.
