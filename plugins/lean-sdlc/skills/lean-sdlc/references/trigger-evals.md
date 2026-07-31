# Trigger and Routing Evaluations

Test from a fresh task with only the installed plugin and target repository visible.

| Prompt or state | Expected behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly |
| Repository `AGENTS.md` requires Lean-SDLC for a mutation | Trigger the skill |
| Rough idea, fuzzy behavior, or stale version promise | Shape |
| A large synthesizer-clone request contains several independently verifiable outcomes | Create several independently verifiable tasks and start only the nearest ready task |
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
| Mutation reaches Plan or Deliver | State `Mode | Required sidecars | Executor action | Reason` |
| A role reaches its first trigger in one lead Codex task | Lazily spawn its fixed `executor`, `researcher`, `verifier`, or `operator` thread |
| The same role triggers for another repository task or inquiry | Send a follow-up to the existing role thread, including after it reported completion |
| A repository task finishes and another becomes ready | Keep every reachable role thread; a normal task transition never justifies another spawn |
| A child name uses a feature, version, description, counter, or an unapproved task identifier | Fail; keep task identifiers inside handoffs and returns except for an announced platform-required replacement |
| A role thread is unavailable, repeatedly stale after correction, reset by the user, or incompatible with a required tool, permission, or runtime | Announce `Role | Context reset reason | Replacement action`, then replace and rehydrate it |
| A reachable role thread already exists | Do not spawn another child for that role |
| Code, configuration, schema, generated artifact, or observable behavior reaches a proof checkpoint | Must reuse or start Verifier |
| Promised proof has multiple commands or noisy output | Must reuse or start Verifier |
| Documentation-only change has one narrow proof command | Lead may verify locally |
| A guided or recorded build, package, CI, deploy, flash, runtime, or smoke procedure is ready | Must reuse or start Operator |
| First unknown deployment procedure | Guide once, then record after success |
| Assisted work has one settled durable task, known paths and proof, and needs no decision | Must reuse or start Executor |
| One localized change in one file needs one narrow proof command | Lead may use the direct fast path |
| An Executor receives work | Send exactly one durable task with lead-supplied outcome, architecture, interfaces, invariants, paths, acceptance, proof, and stop conditions |
| Executor returns one task checkpoint | Lead reviews architecture, scope, and diff once per returned checkpoint; Verifier reruns acceptance-defining proof and adds risk-based regression |
| Corrections follow an Executor checkpoint | Send a concise delta to the same Executor |
| A correction returns another checkpoint | Lead reviews it once per returned checkpoint; Verifier reruns acceptance proof and risk-based regression |
| Executor encounters an interface, dependency, architecture, behavior, acceptance, or path decision | Stop and return the decision to the lead |
| Another durable task is ready after its checkpoint is accepted | Reuse the same Executor with one-task handoff |
| Separate leads have independent writing scopes | Each may use one Executor only under separate owned tasks with disjoint paths |
| Any Executor readiness condition fails | Lead resolves the missing truth before execution |
| Evidence collection spans multiple sources, repositories, large documents, data, logs, or noisy output | Must reuse or start read-only Researcher |
| A single fact has one known source | Lead handles it without Researcher |
| Researcher receives an inquiry | Lead supplies question, decision informed, source priority, scope, stop condition, and return format |
| Researcher returns findings | Return cited findings, conflicts, unknowns, and decision impact |
| Researcher inquiry is read-only and no task exists | Run the inquiry without a task; start one before recording findings |
| Researcher findings require repository writes | Lead starts or uses an owned task before recording them |
| Focused mode | Lead and triggered sidecars, including Researcher when its trigger applies; no Executor |
| Solo mode or “no subagents” | Lead only |
| User pins the lead model | Preserve it and all lead decision authority; route children only within that authority |
| User says all work uses one model | Use it everywhere or switch to Solo |
| Any route proposes `low` reasoning | Fail the evaluation |
| Any primary Luna child is spawned | Use `agent_type=lean_sdlc_luna`, omit direct model and reasoning fields, and use non-full-history `fork_turns` |
| Luna is selected for any child | Route through the named profile that pins Luna `max` |
| The Luna profile is absent, unexposed, rejected, or the user explicitly chooses lower child latency | Announce and directly spawn Terra `xhigh` without `agent_type` |
| Any route proposes Terra `high` | Fail the evaluation |
| A Verifier is asked for task pass, block, or closure | Return operation evidence only; the lead decides task disposition |
| Verifier receives an Executor checkpoint | Rerun acceptance-defining proof, add risk-based regression, and skip Executor-only checks |
| Verifier receives Operator evidence | Consume the evidence instead of repeating the operation |
| The full suite is promised | Run it once under Verifier unless evidence conflicts |
| Sidecar receives a changed checkpoint | Invalidate old evidence and rerun |
| A wait ends while the child remains reachable | Continue waiting or send a follow-up; do not replace it |
| A child becomes unavailable | Announce the context reset, then replace and rehydrate from role, task, docs, and checkpoint |

Failure indicators:

1. Work changes files before an owned task exists.
2. The dispatcher runs all lanes mechanically or stops at every lane boundary.
3. Unknown causes enter Deliver.
4. A child decides scope, architecture, interfaces, acceptance, task state, integration, or closeout, or spawns another child.
5. An Executor receives multiple durable tasks, a backlog, unresolved decisions, or work outside explicit paths.
6. A Researcher edits repository files, makes durable decisions, or collects evidence outside the lead's scope.
7. A sidecar repairs source, guesses a target, leaks secrets, or retries stateful work without authority.
8. Agent-only context becomes the sole record of a durable procedure or decision.
9. Cache preservation justifies unnecessary agents, stale context, or weaker verification.
10. Architecture is selected from a project-size label, or modularity produces speculative or pass-through boundaries.
11. Plausible changed-boundary edge cases are ignored, exhaustively overbuilt, or silently assigned user-visible behavior.
12. Explanatory diagrams use ASCII pseudographics or become denser than the idea they explain.
13. A primary Luna spawn omits `agent_type=lean_sdlc_luna`, adds direct model or reasoning fields, inherits an automatic model, or uses full-history routing.
14. A sidecar chooses close, fail, reopen, pass, or block for the task.
15. Deliver begins without the Orchestration Gate, a mandatory sidecar is skipped, or a ready Assisted durable task beyond the direct fast path stays with the lead.
16. Any Luna child bypasses the named profile or uses reasoning below `max`, any Terra child uses reasoning below `xhigh`, or a fallback is silent.
17. A durable task starts before the lead reviews and Verifier checks the prior accepted checkpoint.
18. Verifier repeats Executor-only targeted checks blindly or repeats an Operator operation.
19. A lead creates a second reachable child for one role or replaces a role because a repository task changed.
20. A child name uses an arbitrary counter such as `V1` or `V11`.
