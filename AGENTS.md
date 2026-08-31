# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work.

<!-- lean-sdlc:startup v1 -->
Use exact startup fields from the lifecycle system message.
The system message supplies `Repository root`, `Skill root`, `Tasks helper`, `Check helper`, `State helper`, `Owner`, `Mode`, and `Child tier`.
The `Skill root` is the parent of the loaded `SKILL.md`.
If any field is absent, run `python3 "<directory containing the loaded SKILL.md>/scripts/session_state.py" --context`.
Use the existing `CODEX_SESSION_ID`.
Never set, replace, or invent `CODEX_SESSION_ID`.
The fallback fails when `CODEX_SESSION_ID` is absent.
Only this fallback returns structured JSON with snake_case fields: `repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, `mode`, and `tier`.
Use returned fields, paths, and owner exactly.
Never reconstruct paths, shorten cache paths, search for helpers, or use placeholder owners.
Children receive task facts and do not locate or run these helpers.
If the checker reports a missing, invalid, or stale managed startup block, run `python3 "<skill-root>/scripts/init_repo.py" "<repo-root>" --repair-startup --task TASK-ID --owner OWNER` before the general before-write check.
<!-- /lean-sdlc:startup -->

## Repository gate

Read `docs/PROJECT.md` and work with `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" open`. Use `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" show TASK-ID` for one task. Do not load full `Done` history. Keep root `tasks.csv` authoritative; change it only through the packaged `tasks.py` helper. Read `references/repository-contracts.md` only for initialization, legacy migration, or document ownership.

`python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" backlog` is the compact Backlog view. `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" open` and the Codex plan overlay exclude Backlog. Before new Standard work, read `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" backlog` and check duplicates, broader items, or related ideas. Do not load Backlog on startup, resume, brainstorming, or Quick Fix work.

Discussion and proposal requests remain read-only. Require explicit implementation authority before Shape and Plan. If ambiguous, remain read-only. Shape owns `why -> what -> how -> proof`; assumptions affecting behavior, scope, or architecture require confirmation. Show a visible plan before task creation. Each durable plan item maps to one task.

Backlog never authorizes planning or implementation. Only a direct user request may add or promote Backlog work. An Architect may propose Backlog placement only for a substantial reason and must wait for approval.

## Task gate

Before any other repository mutation, use `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" start` to create immediate work or claim planned work. Require an owned `In Progress` task, observable acceptance, explicit proof, and a matching visible plan. Run `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" --before-write` before the first non-control write. Dependencies must be `Done` before start. Only the owner closes; a direct user request may override closure with a recorded reason.

During Plan, Quick Fix is inline, not a mode, lane, task type, or prompt. Use it only for an exact reversible outcome, no unresolved product, design, architecture, interface, schema, migration, dependency, security, generated-file, or external-state choice, and one immediate narrow proof. Use Standard when uncertain. Record Context `Quick Fix`; all write gates apply. Architect executes directly, reviews the diff, and runs narrow proof; closure defers broad review.

## Assisted lifecycle and proof

- A running child lifecycle state remains available despite wait expiry or silence. The Architect may request status and wait again.
- Before delegation, the Architect posts a short visible design explanation. The Engineer visibly restates its understanding.
- Route broad evidence reads to Scout. Verification is risk-based and not duplicated. The Architect gives one final visible alignment signoff.
- Before each child handoff, use the canonical pre-handoff design brief in `plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md`.
- The brief states the reason, selected decision, affected ownership, interfaces, and invariants.
- It states a useful rejected option, child decision limits, acceptance, proof, and stop condition.
- Never expose chain-of-thought.

## Plan view and lifecycle

After task creation or start, split, merge, or material plan change, project unresolved IDs and titles into `update_plan` as exact `TASK-NNN — Title` rows. Before or with `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" close`, mark closing row completed. Startup, resume, clear, or compaction: rebuild only unresolved rows from `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" open`; do not load `Done` history. Brainstorming remains read-only and creates no task view. Ledger authoritative.

Assisted mode and Standard children are defaults. Lifecycle restoration restores owner, mode, and tier. Run `python3 "<skill-root>/scripts/session_state.py" --owner OWNER --mode assisted|solo`, `--fast-children`, or `--no-fast-children` for changes. Read `references/subagents.md` before delegation. The Architect owns architecture, interfaces, tasks, acceptance, integration, and closeout. The plugin hook supplies a stable 8-digit task owner.
