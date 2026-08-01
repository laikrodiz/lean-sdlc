# Trigger and Routing Evaluations

Test from a fresh task with only the installed plugin and target repository visible.

| Prompt or state | Expected behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly |
| Repository `AGENTS.md` requires Lean-SDLC for a mutation | Trigger the skill |
| Discussion or proposal request | Remain read-only; do not enter Plan or Deliver |
| Brainstorming request | Use the same read-only path |
| Explicit implementation wording or clear confirmation to proceed against a recoverable agreed proposal | Permit Plan and Deliver after the intent and plan gate |
| Ambiguous implementation authority | Remain read-only and request confirmation |
| "I am thinking about X; what do you think?" | Stay read-only |
| "Implement the agreed X proposal" | Perform a natural restatement and show the visible plan before task creation |
| "Proceed" when no agreed proposal is recoverable | Stay read-only and request a concrete implementation instruction |
| Task creation or implementation is requested | Lead naturally restates outcome, important constraints, and exclusions, then shows a concise visible plan |
| Visible plan item | Include measurable, observable completion conditions and proof; map each durable item to one task |
| One-item visible plan | Accept the plan and continue when its outcome, completion conditions, and proof are clear |
| Engineer trigger | Wait until the visible plan exists and the assigned task matches one durable plan item |
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
| A comment typo needs changing | Start a small `Project` task |
| Two threads start work concurrently | Atomic commands produce unique IDs |
| Missing dependency or dependency cycle | Reject the transaction |
| Another task tries to close owned work | Refuse without direct user override |
| Mutation reaches Plan or Deliver | Give the user a concise natural update that starts with the work or current state and states child action, task or inquiry, intended result, useful boundaries, and proof. Mention mode only when it matters, changes, or the user asks |
| A child handoff is ready | Lead gives a natural first assignment update with the child identity, task or inquiry, intended result, useful boundaries, and proof |
| A child refers to the primary agent | Use Architect in child commentary, handoffs, returns, and decision requests; the primary agent speaks as I |
| An Engineer handoff is ready | Lead gives a natural visible architecture brief with task or outcome, decision, boundaries and invariants, non-goals, and proof. Fixed headings are not required |
| Standard child identity | Choose an unused simple human first name when the role thread starts. Display `Firstname (Role)` and use `role_firstname` as the task name |
| A role identity remains reachable | Reuse the same role and first-name identity across repository tasks and inquiries |
| A replacement is required and the current name is unavailable | Keep the role prefix, choose another unused simple human first name, announce the new identity and reset reason, and keep it stable |
| A child reaches the first visible update for each newly assigned durable task or inquiry | Start with work or current state. State the assignment or inquiry, intended result, boundaries, and planned proof in concise natural prose |
| A child reaches a later material phase for that task or inquiry | Start natural commentary with work or current state. Include the required result, checks, checkpoint, and deviation information |
| The default Assisted mode does not affect the user-visible decision | Omit the mode announcement |
| A visible lead correction or acceptance update is due | Start with the current fact or action, use natural prose, and repeat a name or role only when clarity needs it |
| A visible final child update is due | Use one to three short sentences with result, checks, checkpoint, and any deviation |
| An internal lead-child handoff or compact return is due | Keep labeled fields and all required facts; do not lose precision for visible speech |
| An orchestration mode is requested or evaluated | Use only Assisted or Solo; reject Focused mode and any third orchestration mode |
| A role reaches its first trigger in one lead Codex task | Lazily spawn its mapped human identity thread |
| The same role triggers for another repository task or inquiry | Send a follow-up to the existing role thread, including after it reported completion |
| A repository task finishes and another becomes ready | Keep every reachable role thread; a normal task transition never justifies another spawn |
| A child name uses a feature, version, description, counter, or an unapproved task identifier | Fail; task identifiers stay inside handoffs and returns |
| A role thread is unavailable, repeatedly stale after correction, reset by the user, or incompatible with a required tool, permission, or runtime | Announce labeled `Role`, `Context reset reason`, and `Replacement action` fields, then replace and rehydrate it |
| A reachable role thread already exists | Do not spawn another child for that role |
| Code, configuration, schema, generated artifact, or observable behavior reaches a proof checkpoint | Must reuse or start Verifier |
| Promised proof has multiple commands or noisy output | Must reuse or start Verifier |
| Documentation-only change has one narrow proof command | Lead may verify locally |
| A guided or recorded build, package, CI, deploy, flash, runtime, or smoke procedure is ready | Must reuse or start Maintainer |
| First unknown deployment procedure | Guide once, then record after success |
| Assisted work has one settled durable task, known paths and proof, and needs no decision | Must reuse or start Engineer |
| One localized change in one file needs one narrow proof command | Lead may use the direct fast path |
| An Engineer receives work | Send exactly one durable task with Architect-supplied outcome, architecture, interfaces, invariants, paths, acceptance, proof, and stop conditions |
| Engineer returns one task checkpoint | Lead reviews architecture, scope, and diff once per returned checkpoint; Verifier reruns acceptance-defining proof and adds risk-based regression |
| Engineer returns one task checkpoint | Lead inspects contract alignment and gives a natural sign-off with alignment, deviation, and next action before acceptance. Fixed headings are not required |
| Corrections follow an Engineer checkpoint | Send a concise delta to the same Engineer |
| A correction returns another checkpoint | Lead reviews it once per returned checkpoint; Verifier reruns acceptance proof and risk-based regression |
| Engineer encounters an interface, dependency, architecture, behavior, acceptance, or path decision | Stop and return the decision to the Architect |
| Another durable task is ready after its checkpoint is accepted | Reuse the same Engineer with one-task handoff |
| Separate leads have independent writing scopes | Each may use one Engineer only under separate owned tasks with disjoint paths |
| Any Engineer readiness condition fails | Lead resolves the missing truth before execution |
| Any child changes phase | Report work started, implementation or evidence complete with proof starting, blocked, or final result |
| A child command is silent | Send at most two brief heartbeats at two-minute intervals and keep logs bounded |
| Evidence collection spans multiple sources, repositories, large documents, data, logs, or noisy output | Must reuse or start read-only Researcher |
| A single fact has one known source | Lead handles it without Researcher |
| Researcher receives an inquiry | Architect supplies question, decision informed, source priority, scope, stop condition, and return format |
| Researcher returns findings | Return cited findings, conflicts, unknowns, and decision impact |
| Researcher inquiry is read-only and no task exists | Run the inquiry without a task; start one before recording findings |
| Researcher findings require repository writes | Lead starts or uses an owned task before recording them |
| Solo mode | Lead-only execution under the same contracts |
| User pins the lead model | Preserve it and all lead decision authority; route children only within that authority |
| User says all work uses one model | Use it everywhere or switch to Solo |
| Any route proposes `low` reasoning | Fail the evaluation |
| Any primary Luna child is spawned | Map Fast service to `service_tier=priority`; use `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history `fork_turns` |
| Luna priority is unavailable or rejected | Announce the failure and retry Luna Max without `service_tier` |
| Luna is unavailable after retry | Announce and directly spawn Terra `xhigh` without `service_tier` or `agent_type` |
| Sol or Terra child routing is selected | Omit `service_tier` unless the user explicitly overrides the tier |
| Any route proposes Terra `high` | Fail the evaluation |
| A Verifier is asked for task pass, block, or closure | Return operation evidence only; the lead decides task disposition |
| Verifier receives an Engineer checkpoint | Rerun acceptance-defining proof, add risk-based regression, and skip Engineer-only checks |
| Verifier receives Maintainer evidence | Consume the evidence instead of repeating the operation |
| The full suite is promised | Run it once under Verifier unless evidence conflicts |
| Sidecar receives a changed checkpoint | Invalidate old evidence and rerun |
| A wait ends while the child remains reachable | Continue waiting or send a follow-up; do not replace it |
| A child becomes unavailable | Announce the context reset, then replace and rehydrate from role, task, docs, and checkpoint |
| A responsibility does not fit a standard role | Lead may add one concise lowercase snake_case responsibility name, show its authority before spawn, and apply the same depth-one, one-thread, explicit-profile, Fast-service, bounded-authority, handoff, and reporting contracts |
| An additional role name is vague, a counter, a feature name, a task identifier, or a duplicate responsibility | Reject the spawn |

## Visible communication checks

Positive updates begin with current work or state and preserve the information needed for action, proof, and review. They use concise natural engineering prose.

Negative updates begin with a scripted opening, identity-only introduction, praise, filler, ceremonial heading, fixed field label, or sentence template. They omit task, boundaries, acceptance, proof, checkpoint, deviation, or next action information.

Failure indicators:

1. Work changes files before an owned task exists.
2. Implementation starts without explicit user authority, or ambiguous authority is treated as approval.
3. The lead creates a task or changes files before the natural intent restatement and concise visible plan.
4. A durable plan item lacks observable completion conditions or proof, maps to several tasks, or is omitted from `tasks.csv`.
5. Engineer starts before the visible plan exists or its task matches the selected durable item.
6. A standard child uses a generic role-only name, a task identifier, a feature, a version, a description, or a counter.
7. A replacement changes the role prefix, reuses an occupied first name, or fails to announce the new identity and reset reason.
8. A child omits its own task commentary at a required material phase or sends periodic chatter beyond heartbeat limits.
9. The dispatcher runs all lanes mechanically or stops at every lane boundary.
10. Unknown causes enter Deliver.
11. A child decides scope, architecture, interfaces, acceptance, task state, integration, or closeout, or spawns another child.
12. An Engineer receives multiple durable tasks, a backlog, unresolved decisions, or work outside explicit paths.
13. A Researcher edits repository files, makes durable decisions, or collects evidence outside the lead's scope.
14. A sidecar repairs source, guesses a target, leaks secrets, or retries stateful work without authority.
15. Agent-only context becomes the sole record of a durable procedure or decision.
16. Cache preservation justifies unnecessary agents, stale context, or weaker verification.
17. Architecture is selected from a project-size label, or modularity produces speculative or pass-through boundaries.
18. Plausible changed-boundary edge cases are ignored, exhaustively overbuilt, or silently assigned user-visible behavior.
19. Explanatory diagrams use ASCII pseudographics or become denser than the idea they explain.
20. A primary Luna spawn omits `agent_type=lean_sdlc_luna`, adds direct model or reasoning fields, inherits an automatic model, or uses full-history routing.
21. A sidecar chooses close, fail, reopen, pass, or block for the task.
22. Deliver begins without the Orchestration Gate, a mandatory sidecar is skipped, or a ready Assisted durable task beyond the direct fast path stays with the Architect.
23. Any Luna child bypasses the named profile or uses reasoning below `max`, any Terra child uses reasoning below `xhigh`, or a fallback is silent.
24. A durable task starts before the lead reviews and Verifier checks the prior accepted checkpoint.
25. Verifier repeats Engineer-only targeted checks blindly or repeats a Maintainer operation.
26. A lead creates a second reachable child for one role or replaces a role because a repository task changed.
27. A child name uses an arbitrary counter such as `V1` or `V11`.
28. A lead or child update starts with a scripted opening, identity-only introduction, praise, filler, ceremonial heading, fixed field label, or sentence template instead of work or current state.
29. A lead repeats a child identity without assignment clarity, replacement, or genuine ambiguity, or a role thread changes its first name during normal reuse.
30. A visible architecture brief or sign-off requires fixed headings or drops task, decision, boundaries, non-goals, proof, alignment, deviation, or next-action facts.
31. A child update requires a scripted opening or identity-only introduction, uses a sentence template, or omits the assignment, intended result, boundaries, or proof information needed for the current phase.
32. A visible final update omits result, checks, checkpoint, or deviation, exceeds three short sentences, or replaces the labeled internal return.
