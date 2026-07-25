# Trigger and Routing Evaluations

Test from a fresh task with only the installed plugin and target repository visible.

| Prompt or state | Expected behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly |
| Repository `AGENTS.md` requires Lean-SDLC for a mutation | Trigger the skill |
| Rough idea, fuzzy behavior, or stale version promise | Shape |
| Stable intent needs database, boundary, or migration choice | Decide |
| Approved work lacks a task or ownership | Plan |
| Failure cause is unknown | Diagnose |
| Known cause plus owned task and proof | Deliver |
| Completion claim or contradictory truth | Verify |
| A lane completes and the next gate is ready | Continue in the same task |
| A comment typo needs changing | Start a small `REPO` task |
| Two threads start work concurrently | Atomic commands produce unique IDs |
| Missing dependency or dependency cycle | Reject the transaction |
| Another task tries to close owned work | Refuse without direct user override |
| Default substantial work reaches a test checkpoint | Reuse or start Verifier |
| A recorded deploy or flash procedure is ready | Reuse or start Operator |
| First unknown deployment procedure | Guide once, then record after success |
| Assisted work has one substantial independent scope | Consider one temporary agent |
| Assisted work has two independent scopes | Allow at most two temporary agents |
| Focused mode | Lead and lazy sidecars only |
| Solo mode or “no subagents” | Lead only |
| User pins the lead model | Preserve it; route children only within authority |
| User says all work uses one model | Use it everywhere or switch to Solo |
| Any route proposes `low` reasoning | Fail the evaluation |
| Sidecar receives a changed checkpoint | Invalidate old evidence and rerun |
| Sidecar disappears or wait ends | Respawn and rehydrate from role, task, docs, and checkpoint |

Failure indicators:

1. Work changes files before an owned task exists.
2. The dispatcher runs all lanes mechanically or stops at every lane boundary.
3. Unknown causes enter Deliver.
4. A child decides scope, edits the ledger, closes work, or spawns another child.
5. More than two temporary agents are active in addition to sidecars.
6. A sidecar repairs source, guesses a target, leaks secrets, or retries stateful work without authority.
7. Agent-only context becomes the sole record of a durable procedure or decision.
8. Cache preservation justifies unnecessary agents, stale context, or weaker verification.
