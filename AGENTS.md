# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work.

Architect-assigned children follow the loaded skill's Child entry. Architect startup and ledger steps below do not apply to children.

<!-- lean-sdlc:startup v1 -->
Use exact startup fields from the lifecycle system message.
The system message supplies `Repository root`, `Skill root`, `Tasks helper`, `Check helper`, `State helper`, `Owner`, `Mode`, `Active mode`, and `Child tier`.
The `Skill root` is the parent of the loaded `SKILL.md`.
If any field is absent, run `python3 "<directory containing the loaded SKILL.md>/scripts/session_state.py" --context`.
Use the existing `CODEX_SESSION_ID`.
Never set, replace, or invent `CODEX_SESSION_ID`.
The fallback fails when `CODEX_SESSION_ID` is absent.
Only this fallback returns structured JSON with snake_case fields: `repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, `mode`, `active_mode`, and `tier`.
Use returned fields, paths, and owner exactly.
Never reconstruct paths, shorten cache paths, search for helpers, or use placeholder owners.
Children receive task facts, load only common boundaries and their assigned role section, and do not locate or run these helpers.
If the checker reports a missing, invalid, or stale managed startup block, run `python3 "<skill-root>/scripts/init_repo.py" "<repo-root>" --repair-startup --task TASK-ID --owner OWNER` before the general before-write check.
<!-- /lean-sdlc:startup -->

## Execution contract

The loaded skill owns mode selection, task gates, documentation, support, proof, and closure.
Follow its selected mode contract. Do not load unselected mode policies or repeat unchanged instruction reads.
Keep `tasks.csv` authoritative and mutate it only through the packaged tasks helper.
Use `docs/PROJECT.md` as the mandatory shared project document. Preserve current user scope and required documentation.
