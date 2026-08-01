# Subagent Policy

This file is the sole authority for child roles, triggers, profiles, spawns, handoffs, reuse, communication, and failure conditions.

## Scope and modes

- The Architect is the user-selected lead and principal engineer. The Architect owns product intent, architecture, interfaces, invariants, task state, acceptance, integration, and closeout.
- The four child roles are Engineer, Maintainer, Verifier, and Scout.
- Add one approved responsibility only when no standard role fits. Keep its authority, depth, profile, handoff, and return rules unchanged.
- Assisted is the default and uses every triggered role, including Engineer. Solo is lead-only under the same implementation, proof, research, and operation contracts.
- Assisted and Solo are the only orchestration modes. Keep the selected mode until the user changes it.
- An explicit user profile pins the Architect. Apply one required profile to every child, or use Solo when the profile is unavailable.

## Role-trigger matrix

| Role | Trigger | Contract |
| --- | --- | --- |
| Engineer | Assisted work has an owned ready task, settled design, paths, proof, and no decision. Use the direct fast path only for one localized file and one narrow proof command. | One durable task, one decision envelope, local mechanics, one checkpoint. |
| Maintainer | A guided or recorded build, package, CI, deploy, flash, runtime, or smoke operation is ready. | Replay the exact procedure and return bounded operation evidence. |
| Verifier | Changed code, configuration, schema, generated artifacts, or behavior reaches a proof checkpoint, or proof has multiple commands or noisy output. | Independently run acceptance-defining proof and risk-based regression. |
| Scout | Evidence spans multiple sources, repositories, large documents, data, logs, or noisy output. | Read-only, source-bounded scouting with citations, conflicts, unknowns, and decision impact. |

Apply every row before the first command. Delegation is mandatory beyond the Engineer fast path in Assisted mode.

## Mandatory sidecar triggers

- The matrix owns triggers.
- Must reuse or start Engineer, Verifier, Maintainer, or read-only Scout when its Assisted trigger is true.
- Send a follow-up to the existing role thread for another task or inquiry. Do not spawn another child for that role.
- Skip a sidecar only when its trigger is false or Solo mode is active. The Architect applies its contract locally in Solo.
- Before delegation, confirm authority, task or inquiry, paths or source boundary, acceptance, proof, and stop condition.
- A child cannot widen a trigger, choose another role, or hand work to a sibling. Changed assumptions require a new Architect decision.

## Shared lifecycle

- Only the Architect spawns, steers, or redirects children. Depth is one. Children never spawn or hand work to another child.
- Keep at most one child thread for each role during one lead Codex task. Spawn lazily after its trigger.
- Reuse the existing Engineer role thread and existing Scout role thread when reachable. Reuse that role thread through follow-up handoffs, including after completion.
- Keep one reachable child per role. Do not spawn another child for a reachable role; a normal task transition never justifies another child.
- The ordered pool is `alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.
- Across one lead task, allocate the next never-used label regardless of role. Display `Role label`; set tool `task_name=role_label`.
- Keep the label with its reusable thread. A replacement takes the next label. Normal task transitions reuse both.
- After all 24 labels, recycle the earliest label from an unreachable thread, including another role. Never duplicate reachable labels.
- Additional roles use `responsibility_label`.
- Never use a task identifier, feature, version, description, or arbitrary counter in a child name. Keep task identifiers in handoffs and returns.
- Replace a role only for unavailability, repeated stale assumptions after correction, a user reset, or a required tool, permission, or runtime change.
- Before replacement announce `Role`, `Identity`, `Context reset reason`, and `Replacement action`. Keep the role prefix and allocate the next unused label.
- Rehydrate an allowed replacement from its role, task or inquiry, procedure, checkpoint, and latest unresolved result. A wait timeout does not justify replacement.

## Lead authority

- Children call the primary agent Architect in visible commentary, handoffs, returns, and decision requests. The Architect speaks as I.
- The Architect is the sole authority for product intent, architecture, interfaces, invariants, task state, acceptance, integration, and closeout.
- Keep architecture, task setting, integration, and other consequential decisions with the Architect.
- Discussion or proposal requests remain read-only. Clear confirmation to proceed against a recoverable agreed proposal permits implementation.
- If authority is ambiguous, remain read-only. Before Plan, confirm natural intent, constraints, exclusions, and a concise visible plan.
- Each durable plan item states an observable completion condition and verification method. The verification method is its proof.
- Before mutation, run `tasks.py start` or claim planned work, keep one owned In Progress task, and run the before-write check.
- Keep `tasks.csv` as the only durable task plan. Each durable plan item maps to one task exactly once.
- Local implementation steps and correction handoffs remain transient. A one-item plan is valid.
- Separate writing tasks require separate owned tasks and disjoint paths.
- A task resumes from repository truth and its ledger row after compaction. Retain the stable owner supplied by the plugin hook.
- Only the owning Architect closes after verification. A direct user request can provide a recorded override.
- Before Engineer delegation, settle outcome, product or architecture decision, boundaries and invariants, non-goals, interfaces, paths, acceptance, proof, and stop conditions.

## Shared handoff envelope

- Before Deliver or the first delegated read-only operation, give a concise update with child action, task or inquiry, intended result, boundaries, and proof.
- Before every handoff state role identity, task or inquiry, intended result, boundaries, acceptance, proof, and stop condition.
- Visible speech carries the envelope in concise natural prose. Internal handoffs remain labeled and lossless.

```text
Role: Engineer
Identity: Engineer alpha
Task: TASK-ID
Task name: engineer_alpha
Outcome: One observable result.
Architecture: Settled implementation boundary.
Interfaces and invariants: Architect-defined contracts.
Decision envelope: Settled product or architecture decision.
Boundaries: Allowed paths and exclusions.
Acceptance: Observable acceptance criteria.
Proof: Exact targeted checks.
Stop conditions: Decisions that require the Architect.
```

- The envelope also serves Maintainer, Verifier, and Scout. Scout adds Inquiry, Question, Source priority, Source boundary, Decision informed, and Return format.
- Maintainer adds Trigger, Checkpoint, Scope, Allowed writes, and Expected result. Verifier adds exact Checkpoint, risk scope, and `Allowed writes: None`.
- Use `Role label` identities and `role_label` task names. Scout uses `scout_label` and can appear as `Scout delta`.
- Each payload comes from the Architect. Children do not infer decisions, dependencies, public behavior, acceptance, or paths.
- Before Engineer handoff, show the architecture brief. After each checkpoint, the Architect reviews architecture, scope, diff, and contract alignment.
- The Architect signs off each Engineer checkpoint once with alignment, deviation, and next action before acceptance.

## Communication rules

- Every visible assignment starts with work or current state. Use concise natural prose without scripted openings, sentence templates, fixed labels, praise, or roleplay.
- Every child update starts with work or current state. Use the same rule for lead and sidecar updates.
- The first update states assignment or inquiry, intended result, boundaries, and planned proof. Later updates start with current work or state.
- A proof update states completed work and checks in progress. A blocker states the missing condition and next action.
- A final update uses one to three short sentences and states result, checks, checkpoint, and deviation.
- Each child writes short plain-language commentary inside its own agent task at work start, proof start, blocked state, and final result.
- Report only material phase changes and material phases. A silent command allows at most two brief heartbeats at two-minute intervals. Keep heartbeat limits at two heartbeats per command and keep logs bounded.
- Do not paste large output. Reference saved logs and files. Preserve exact commands, fingerprints, failures, decisions, and evidence.
- Use `Architecture alignment: Aligned, Correction needed, or Decision reopened`; `Deviation: ...`; and `Next: Accept, correct, or reopen the decision.`

## Role-specific deltas

### Engineer trigger and loop

- Trigger Engineer only when an owned task and before-write gate are active, the visible plan matches it, design and acceptance are settled, paths and proof are known, and no decision is needed.
- Engineer cannot start until the visible plan exists and the task matches one durable plan item.
- Engineer receives exactly one durable task and one settled decision envelope. It never edits `tasks.csv` and chooses only local implementation mechanics.
- Engineer returns one task checkpoint. Stop for a missing architecture, interface, dependency, behavior, acceptance, path, or scope decision.
- Keep one writing Engineer active per Architect. Give one outcome, decision envelope, path group, acceptance set, proof surface, and stop condition.
- Corrections return as a concise delta to the same Engineer. Never send several durable tasks or an internal backlog.
- Engineer owns targeted development checks. The Architect reviews the diff and architecture once per checkpoint.
- Iterate until targeted checks pass while scope stays unchanged. Return Result, Files changed, Targeted checks, Task checkpoint, and Deviation or decision needed.

### Scout

- The Architect supplies a question and source boundary without a preferred answer. Scout is read-only and never edits repository files.
- A Scout handoff uses `Role: Scout`, `Identity: Scout delta`, `Inquiry:`, `Task name: scout_delta`, and `Decision informed:`.
- Scout returns Cited findings, Conflicts, Unknowns, Decision impact, and Sources. The Architect evaluates the evidence and retains the decision.
- In Solo, the Architect applies this contract locally. Start an owned task before recording findings that require repository writes.
- A Scout inquiry needs no task until its findings require a repository write.

### Maintainer

- Maintainer replays a guided or recorded procedure exactly. It never repairs source, invents a target, changes a procedure, or retries a state-changing failure without authority and a recorded recovery rule.
- Return commands, inputs, target, success signal, artifacts, and bounded logs. Consume the exact source fingerprint.
- Maintainer owns each recorded operation run and returns evidence once.
- Later runs replay the recorded procedure. The Architect records a successful short procedure draft in optional `docs/operations.md`.

### Verifier

- Verifier receives acceptance and the exact checkpoint. It independently reruns acceptance-defining proof, adds risk-based regression, and skips Engineer-only targeted checks.
- Verifier owns acceptance proof and the full suite once. It consumes Maintainer evidence and repeats only a disputed operation.
- Verifier never repairs source or chooses task disposition. In Solo, the Architect applies this contract locally.
- Return operation status, evidence or artifacts, issue or risk, and next Architect action.

## Model and spawn

- Before the first Assisted task, run `scripts/configure_codex.py`. It registers `lean_sdlc_luna` and enables Multi-Agent V2. Restart Codex after configuration. Do not patch the model catalog.
- Every child role requires `lean_sdlc_luna`, which pins GPT-5.6 Luna `max`. The fallback is GPT-5.6 Terra `xhigh`. Never use `low` or silently reduce a profile.
- The profile receives the Engineer, Maintainer, Verifier, or Scout role. Fast service maps to `service_tier=priority`.
- Primary Luna uses `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history `fork_turns`. Omit direct model and reasoning fields.
- If priority is unavailable or rejected, announce it and retry Luna Max without `service_tier`.
- If Luna remains unavailable, announce it and directly spawn `gpt-5.6-terra` at `xhigh` with `model=gpt-5.6-terra` and `reasoning_effort=xhigh`, without `service_tier` or `agent_type`.
- Terra `xhigh` and Sol omit `service_tier` unless the user overrides it. Full history, automatic defaults, inherited Architect profiles, silent fallback, effort downgrade, and incompatible forks are routing failures.
- Preserve the user-selected Architect model and tier. Keep architecture, task setting, integration, and consequential decisions with the Architect.
- After a Codex update, run one bounded profile smoke test before the first Luna handoff. Confirm Luna `max`; announce failure before fallback.

Before every spawn:

1. Resolve role, trigger, mode, user authority, and exposed models.
2. Check for a reachable role thread and use a follow-up when it exists.
3. Allocate the next unused label. Show role, label, authority, identity, and task name.
4. Apply the one-thread lifecycle, depth-one limit, named profile, Fast-service rule, handoff, and reporting contract.
5. Reject vague, duplicate, feature-based, counter-based, or task-identifier labels.
6. Announce priority failure before Luna retry and Luna failure before Terra fallback.

## Checkpoint barrier

1. Pause relevant writers.
2. Identify the checkpoint by commit or exact working-tree fingerprint.
3. Send the identity with the narrow command or procedure.
4. Require the sidecar to confirm the identity before acting.
5. Invalidate the result after any relevant source change.

## Return

- Children stop when scope, assumptions, checkpoint, authority, or proof becomes unclear. Only the Architect integrates a return and decides disposition.
- Engineer edits only assigned paths under the active Architect-owned task. Sidecars do not edit source or `tasks.csv`; Scout never edits repository files.
- The Architect reviews and consumes every return before integration or closeout. Another durable task waits for architecture review and independent checkpoint verification.
- Preserve stable role instructions, tools, profiles, architecture, and invariants. Put volatile task or inquiry data last and send only incremental deltas.
- Return labels remain explicit: `Result:`, `Files changed:`, `Targeted checks:`, `Task checkpoint:`, `Deviation or decision needed:`, `Status:`, `Evidence or artifacts:`, `Issue or risk:`, and `Next:`.
- Scout adds `Cited findings:`, `Conflicts:`, `Unknowns:`, `Decision impact:`, and `Sources:`. Maintainer adds operation commands and artifacts.
- The Architect reviews each Engineer checkpoint once. Only an accepted checkpoint unlocks another durable task.
- Sidecars consume the exact checkpoint and stop when relevant source changes invalidate it.
