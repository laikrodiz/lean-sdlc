# Lean-SDLC Repository Rules

<!-- lean-sdlc:startup v1 -->
Use $lean-sdlc for repository work. Read SKILL.md and only the instructions for the current request or assigned role.
Conversation and planning remain read-only unless the user authorizes implementation.
For execution, use exact Repository root, Skill root, Tasks helper, Check helper, State helper, Owner, and Child tier from startup context.
If fields are absent, run `python3 "<directory containing the loaded SKILL.md>/scripts/session_state.py" --context` from the selected repository.
Use returned paths and owner exactly. Preserve CODEX_SESSION_ID; never invent paths or an owner.
Read references/ledger.md for task transactions, initialization, or upgrades. The ledger remains authoritative.
After an authorized upgrade, reload the current applicable instructions and continue the authorized task.
Preserve custom project rules outside this block. Report conflicts instead of silently discarding them.
<!-- /lean-sdlc:startup -->
