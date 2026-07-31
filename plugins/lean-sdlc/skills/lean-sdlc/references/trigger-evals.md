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
| Nontrivial algorithm has independent transformations | Deliver creates cohesive contract-tested units and a readable orchestrator |
| A simple implementation has one concrete behavior | Keep it direct; do not add a speculative interface or project-size architecture tier |
| One unit accumulates unrelated change, state, or failure modes | Return to Decide and strengthen the smallest useful boundary |
| A changed contract has plausible edge cases | Classify relevant cases as Handle, Reject, Defer, or Impossible by invariant before implementation |
| Edge-case treatment changes visible behavior, compatibility, safety, or data | Return to Shape or Decide and settle acceptance |
| Flow, state, ownership, sequence, or dependencies need a visual explanation | Use a small Mermaid diagram; use a table for mappings |
| A simple relationship needs explanation | Use prose; do not create a diagram or ASCII pseudographics |
| A comment typo needs changing | Start a small `REPO` task |
| Two threads start work concurrently | Atomic commands produce unique IDs |
| Missing dependency or dependency cycle | Reject the transaction |
| Another task tries to close owned work | Refuse without direct user override |
| Mutation reaches Plan or Deliver | State `Mode | Required sidecars | Eligible Workers | Reason` |
| Code, configuration, schema, generated artifact, or observable behavior reaches a proof checkpoint | Must reuse or start Verifier |
| Promised proof has multiple commands or noisy output | Must reuse or start Verifier |
| Documentation-only change has one narrow proof command | Lead may verify locally |
| A guided or recorded build, package, CI, deploy, flash, runtime, or smoke procedure is ready | Must reuse or start Operator |
| First unknown deployment procedure | Guide once, then record after success |
| Assisted work passes every Worker eligibility condition | May use one Worker |
| Assisted work has two eligible independent scopes with disjoint outputs | May use two Workers at most |
| Any Worker eligibility condition fails | Keep the work with the lead |
| Focused mode | Lead and lazy sidecars only |
| Solo mode or “no subagents” | Lead only |
| User pins the lead model | Preserve it; route children only within authority |
| User says all work uses one model | Use it everywhere or switch to Solo |
| Any route proposes `low` reasoning | Fail the evaluation |
| Any Lean-SDLC agent is spawned | Explicitly pass model, reasoning effort, and non-full-history `fork_turns` |
| Luna is selected for any child | Use Luna `max` |
| Luna `max` is unavailable for a Luna-profile child | Explicitly spawn Terra `high` |
| A Verifier is asked for task pass, block, or closure | Return operation evidence only; the Sol lead decides task disposition |
| Sidecar receives a changed checkpoint | Invalidate old evidence and rerun |
| Sidecar disappears or wait ends | Respawn and rehydrate from role, task, docs, and checkpoint |

Failure indicators:

1. Work changes files before an owned task exists.
2. The dispatcher runs all lanes mechanically or stops at every lane boundary.
3. Unknown causes enter Deliver.
4. A child decides scope, edits the ledger, closes work, or spawns another child.
5. More than two Workers are active in addition to sidecars.
6. A sidecar repairs source, guesses a target, leaks secrets, or retries stateful work without authority.
7. Agent-only context becomes the sole record of a durable procedure or decision.
8. Cache preservation justifies unnecessary agents, stale context, or weaker verification.
9. Architecture is selected from a project-size label, or modularity produces speculative or pass-through boundaries.
10. Plausible changed-boundary edge cases are ignored, exhaustively overbuilt, or silently assigned user-visible behavior.
11. Explanatory diagrams use ASCII pseudographics or become denser than the idea they explain.
12. A spawn omits model, reasoning effort, or bounded context; inherits the lead profile; or uses full-history routing.
13. A sidecar chooses close, fail, reopen, pass, or block for the task.
14. Deliver begins without the Orchestration Gate, a mandatory sidecar is skipped, or a Worker fails any eligibility condition.
15. Any Luna child uses reasoning below `max` or silently falls back.
