# Subagent Policy

This file is the sole authority for child roles, triggers, profiles, spawns, handoffs, reuse, communication, and failure conditions.

## Scope and modes

- The Architect is the user-selected lead and principal engineer. The Architect owns product intent, architecture, interfaces, invariants, task state, acceptance, integration, and closeout.
- The standard child roles are Engineer, Maintainer, Verifier, and Scout.
- A custom role requires direct user authority. The Architect records its responsibility, depth, profile, handoff, return, and checkpoint rules before use.
- Engineer receives one ledger task after architecture, outcome, proof, and acceptance are settled. See [plan.md](plan.md) for task sizing, split, merge, and correction rules.
- Assisted mode is the default and uses every triggered role, including Engineer. Keep Assisted until the user selects Solo.
- Session state stores the selected mode and the Fast-children preference. Missing or invalid state restores Assisted with Standard children.
- Lifecycle restoration runs after startup, resume, clear, and compaction. It restores owner, mode, and child tier. After restoration, the Architect reloads this policy before Deliver.
- When mode changes, the Architect runs `scripts/session_state.py --owner OWNER --mode assisted|solo` with the selected mode. When the child tier changes, the Architect runs `scripts/session_state.py --owner OWNER --fast-children` or `--no-fast-children`.
- Assisted and Solo are the only orchestration modes. Solo mode is lead-only under the same implementation, proof, research, and operation contracts.
- Fast children require explicit user opt-in. Keep reachable child threads after a tier change. Apply the new tier to new or normally replaced threads.
- An explicit user profile pins the Architect. Apply one required profile to every child, or use Solo when the profile is unavailable.

## Role-trigger matrix

| Role | Trigger | Contract |
| --- | --- | --- |
| Engineer | Assisted work has an owned ready implementation task, settled design, paths, proof, and no decision. Use the direct path only for one mechanical bounded change with one narrow proof command. | One durable task, one decision envelope, local mechanics, one checkpoint. |
| Maintainer | A guided or recorded build, package, CI, deploy, flash, runtime, or smoke operation is ready, an accepted checkpoint has shared-document impact, or a documentation-only task is ready. | Replay the exact procedure, return bounded operation evidence, and synchronize affected shared documents through an impact-directed pass. |
| Verifier | Changed code, configuration, schema, generated artifacts, or behavior reaches a proof checkpoint, or proof has multiple commands or noisy output. | Independently run acceptance proof and one planned regression command. Run the full suite only when the task or repository contract requires it. |
| Scout | A named Architect decision requires distinct source sets or enough material, data, or logs to pollute lead context. | Read-only, source-bounded scouting with citations, conflicts, unknowns, and decision impact. |

Apply every row before the first command. Delegation is mandatory beyond the Engineer direct path in Assisted mode.

## Independence gate

- At most two active children may run when each child has an exclusive primary scope, a settled contract, no dependency on the other child, and useful time reduction.
- This universal independence gate permits Engineer/Engineer, Engineer/Scout, and Scout/Scout pairs.
- The gate never permits a third active child. Otherwise schedule children serially.
- Implementation writers stop before integration. No writer overlaps documentation synchronization, verification, or stateful operations.
- Shared tests, docs, generators, and operations run serially after the checkpoint.
- A Scout may overlap one Verifier or Maintainer only for future work with separate resources.
- Keep at most one reusable Verifier and at most one reusable Maintainer. They remain single sidecars and never create a second sidecar.
- If scope, dependency, contract, or time reduction is uncertain, pause writers and ask the Architect. Continue with one child only after the Architect resolves the uncertainty.

## Child lifecycle

- Reuse or start Engineer, Verifier, Maintainer, or read-only Scout when its Assisted trigger is true. Send a follow-up to a reachable role thread before starting a replacement.
- Skip a sidecar only when its trigger is false or Solo mode is active. The Architect applies its contract locally in Solo.
- Before delegation, confirm authority, task or inquiry, paths or source boundary, acceptance, proof, and stop condition.
- A child cannot widen a trigger, choose another role, or hand work to a sibling. Changed assumptions require a new Architect decision.
- Keep one reachable child thread for each role. A qualified pair may use two Engineer threads, two Scout threads, or one of each; sidecars remain one each.
- Only the Architect spawns, steers, or redirects children. Depth is one. Children never spawn or hand work to siblings.
- The Architect owns each child name at spawn time. A valid name uses one lowercase role prefix (`engineer`, `maintainer`, `verifier`, or `scout`) and one Greek suffix.
- The Architect allocates the next never-used label from `alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.
- The Architect supplies the exact `task_name` and keeps it with the reusable thread. Example: Engineer beta uses `task_name=engineer_beta`. A child never chooses or changes its task name. A replacement takes the next label.
- After all 24 labels, recycle the earliest label from an unreachable thread. Never duplicate a reachable label.
- Rehydrate an allowed replacement from its role, task or inquiry, procedure, checkpoint, and latest unresolved result.
- Replace a role only for unavailability, repeated stale assumptions after correction, a user reset, or a required tool, permission, or runtime change. Announce the role, identity, context reset reason, and replacement action before replacement.
- A qualified pair uses one root `tasks.csv` and one Architect owner when tasks exist, then stops at one combined checkpoint.

## Shared handoff envelope

- Children call the primary agent Architect in visible commentary, handoffs, returns, and decision requests. The Architect speaks as I.
- The Architect is the sole authority for product intent, architecture, interfaces, invariants, task state, acceptance, integration, and closeout.
- Discussion or proposal requests remain read-only. Clear confirmation to proceed against a recoverable agreed proposal permits implementation. If authority is ambiguous, remain read-only.
- Before every handoff, state the outcome, boundary, contract, proof, and stop conditions in concise natural prose without a fixed runtime template.
- Before Deliver or the first delegated read-only operation, state the child action, task or inquiry, intended result, boundaries, and proof. Before every handoff, include role identity, acceptance, and stop condition.
- Each payload comes from the Architect. Children do not infer decisions, dependencies, public behavior, acceptance, or paths. Before Engineer handoff, show the architecture brief.
- After each checkpoint, the Architect reviews the diff, architecture, scope, and contract alignment in concise natural prose.

## Communication

- Every child update starts with work or current state. Use concise natural prose without greetings, scripted openings, fixed labels, praise, or roleplay.
- Report only material phase changes. For a silent command, use at most two useful heartbeats at two-minute intervals and keep logs bounded.
- Engineer returns one checkpoint with the result, changed paths, targeted checks, task checkpoint, and deviation or decision needed in concise natural prose.
- Scout adds cited findings, conflicts, unknowns, decision impact, and sources in concise natural prose. Maintainer adds operation commands and artifacts. Verifier adds operation status, evidence or artifacts, issue or risk, and next Architect action.

## Role-specific rules

### Engineer

- Trigger Engineer only for an owned ready implementation task when the before-write gate is active, the visible plan matches it, design and acceptance are settled, paths and proof are known, and no decision is needed.
- Engineer cannot start until the visible plan exists and the task matches one durable plan item.
- Engineer receives one durable task and one settled decision envelope. It never edits `tasks.csv` or runs Git operations.
- Engineer owns targeted development checks and code-local truth such as tests, comments, docstrings, annotations, and local examples.
- Stop for a missing architecture, interface, dependency, behavior, acceptance, path, or scope decision. Iterate until targeted checks pass while scope stays unchanged.

### Scout

- The Architect supplies a question and source boundary without a preferred answer. Scout is read-only and never edits repository files.
- Scout returns cited findings, conflicts, unknowns, decision impact, and sources. The Architect evaluates evidence and retains the decision.
- A Scout inquiry needs no task until its findings require a repository write.

### Maintainer

- Maintainer replays a guided or recorded procedure exactly. It never repairs source, invents a target, changes a procedure, or retries a state-changing failure without authority and a recorded recovery rule.
- Maintainer owns each recorded operation run and returns evidence once. After Engineers stop and Architect review, Maintainer synchronizes affected shared narrative documents before the final checkpoint.
- Shared narrative includes `docs/PROJECT.md`, feature, decision, architecture, interface, README, and operations documents. The Architect supplies the behavior and decision delta; Maintainer cannot invent product or architecture decisions.
- Later runs replay the recorded procedure exactly. Record a successful short procedure draft in optional `docs/operations.md`.

### Verifier

- Verifier receives acceptance and the exact checkpoint. It independently reruns acceptance proof and one planned regression command, and skips Engineer-only targeted checks.
- Run the full suite once only when the task or repository contract requires it. Consume Maintainer evidence and repeat only a disputed operation.
- Verifier never repairs source or chooses task disposition. In Solo, the Architect applies this contract locally.

## Model and spawn

- Before the first Assisted task, run `scripts/configure_codex.py`. It registers `lean_sdlc_luna` and enables Multi-Agent V2. Restart Codex after configuration. Do not patch the model catalog.
- Every child role uses `lean_sdlc_luna`, which pins GPT-5.6 Luna `max` (`gpt-5.6-luna`). The fallback is GPT-5.6 Terra `xhigh`. Never use `low` or silently reduce a profile.
- The profile receives the Engineer, Maintainer, Verifier, or Scout role. Luna Max uses Standard service by default, so normal spawns omit `service_tier`.
- When the user explicitly enables Fast children, the Architect records that session preference and new or normally replaced Luna spawns use `service_tier=priority`.
- If a Fast Luna spawn with priority is unavailable or rejected, announce it and retry Luna max without `service_tier` as a Standard retry.
- If Luna remains unavailable, announce it and directly spawn `gpt-5.6-terra` at `xhigh` with `model=gpt-5.6-terra` and `reasoning_effort=xhigh`, without `service_tier` or `agent_type`.
- Terra `xhigh` fallback and the Architect remain Standard unless the user separately overrides them. Full history, automatic defaults, inherited Architect profiles, silent fallback, effort downgrade, and incompatible forks are routing failures.
- Preserve the user-selected Architect model and tier. Keep architecture, task setting, integration, and other consequential decisions with the Architect.
- After a Codex update, run one bounded profile smoke test before the first Luna handoff. Confirm Luna `max`; announce failure before fallback.

Before every spawn, resolve role, trigger, mode, authority, exposed models, reachable role thread, label, profile, service tier, handoff, and reporting contract. Reject vague, duplicate, feature-based, counter-based, task-identifier, or arbitrary labels.

## Checkpoint barrier

1. Require all active work children to stop before integration.
2. Architect reviews the combined implementation and scopes.
3. Run any shared source-changing formatter or generator serially; Architect reviews resulting changes.
4. Maintainer synchronizes affected shared docs through an impact-directed pass.
5. Pause all writers and identify the checkpoint by commit or exact working-tree fingerprint as the final checkpoint; require the sidecar to confirm the identity before acting.
6. Verifier checks both acceptance sets for a qualified pair, or the one active acceptance set, plus assigned-path separation, semantic interaction, and documentation parity. Run the full suite only when required by the task or repository contract.
7. Maintainer runs required build, package, deploy, flash, runtime, or smoke operations serially against that exact accepted source checkpoint. Invalidate the result after any relevant source change.

## Return and stop conditions

- Children stop when scope, assumptions, checkpoint, authority, or proof becomes unclear. Only the Architect integrates a return and decides disposition.
- Engineer edits only assigned implementation paths. Maintainer edits only assigned shared-document paths. Verifier and Scout are read-only. No child edits `tasks.csv`.
- The Architect reviews and consumes every return before integration or closeout. Later dependent work waits for architecture review and independent checkpoint verification.
- Preserve stable role instructions, tools, profiles, architecture, and invariants. Put volatile task or inquiry data last and send only incremental deltas.
- Sidecars consume the exact checkpoint and stop when relevant source changes invalidate it.
