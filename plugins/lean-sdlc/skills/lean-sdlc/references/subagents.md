# Subagent Policy

## Scope and modes

- The Architect is the sole authority for product intent. The Architect always owns intent, public behavior, architecture, tasks, acceptance, integration, and closeout.
- The Architect never sends unresolved user input to a child, writes inside an active child boundary, accepts unreviewed output, or replaces independent proof with confidence.
- The standard child roles are Engineer, Maintainer, Verifier, and Scout. Custom roles need direct user authority.
- Assisted mode normally delegates routine discovery, evidence, implementation, checks, documentation, and recorded operations. Assisted mode is the default.
- Solo mode is lead-only. Assisted and Solo are the only orchestration modes.
- Missing or invalid state restores Assisted with Standard children. Lifecycle restoration restores owner, mode, and tier after startup, resume, clear, or compaction.
- Fast children need user opt-in.
- The Architect is the user-selected lead. An explicit user Architect profile controls it. Apply the required child profile before delegation; if unavailable, use Solo.
- The Architect may implement under these exceptions: Solo mode; mechanical direct path; small architecture-bearing experiment or inseparable seam; after explicit user direction that the Architect itself implement; or after the required child and fallback are unavailable. Settled separable work remains Engineer work.

## Quick Fix

- Quick Fix follows [plan.md](plan.md). Architect may execute it in either mode. Do not spawn Engineer, Maintainer, or Verifier per Quick Fix; shared batch may use Verifier when triggered.

## Role-trigger matrix

| Role | Trigger | Contract |
| --- | --- | --- |
| Engineer | An owned ready implementation task has settled design, paths, proof, and no decision. | Task and checkpoint. |
| Maintainer | A guided or recorded build, package, CI, deploy, flash, runtime, or smoke operation is ready; an accepted checkpoint has shared-document impact; or documentation-only work is ready. | Replay; return evidence. |
| Verifier | Changed code, configuration, schema, generated artifacts, or behavior reaches a proof checkpoint, or proof has multiple commands or noisy output. | Independent proof; regression command. |
| Scout | A named Architect decision requires distinct source sets or enough material, data, or logs to pollute lead context. | Read-only evidence. |

Use the Engineer direct path only for one mechanical bounded change with one narrow proof command.

## Independence gate

- At most two active children run after a resource gate passes. This is universal independence gate. Each child has exclusive scope and settled contract; all dependencies are `Done`; elapsed time should decrease.
- Two Engineers require separate mutable code and test paths, stable read paths, incidental outputs or caches, commands, services, ports, devices, and external targets; no shared public interface, schema, manifest, lockfile, generator, migration, or mutable fixture; independent acceptance and proof.
- The Architect is a writer and must not edit child-owned paths. One Architect writer group owns a worktree. The `tasks.csv` lock protects only the ledger.
- Engineer/Engineer requires strict isolation. Engineer/Scout requires a stable separate read boundary. Scout/Scout may overlap stable sources for independent questions. A Scout may overlap one Verifier or Maintainer only for future work with separate resources.
- Maintainer and Verifier stay serial with writers. Project-native command/test parallelism stays inside one child when safe.
- Apply every role trigger before the first command. Assisted delegation is mandatory beyond the Engineer direct path.
- Implementation writers stop before integration. No writer overlaps documentation synchronization, verification, or stateful operations. Shared tests, docs, generators, and operations run serially. One Verifier checks the combined checkpoint.

## External tools

- External-tool routing starts before substantial plugin, MCP, connector, CAD, database, deployment, or similar work. Architect keeps target, permissions, constraints, architecture, decisions, and final acceptance. Architect may make one bounded probe; delegate remaining routine work after it.
- Delegate before work when more than three external calls are expected; large schemas/logs/inventories/search results; one operation repeats across objects; tool discovery is required; error recovery needs several diagnostic calls; or output needs reduction before a decision.
- Route read-heavy discovery and reduction to Scout, approved mutations to Engineer, repeated build/export/import/deploy/flash procedures to Maintainer, independent checks to Verifier.
- Use bounded programmatic tool calling for deterministic reads or reductions. Inside the assigned child, use direct calls for mutations, approvals, or judgment-sensitive steps. Routine mutation calls belong to the assigned Engineer or Maintainer, not the Architect.
- One agent owns each mutable external target. Never let two agents mutate the same project, database, deployment, or hardware target.
- Child returns conclusions, errors, artifact paths or IDs, and unresolved questions, not a raw transcript. Reuse the same child for the same tool and project. Replace after a material tool or target change.
- Token-waste signals include compaction during tool work, several direct routine calls, repeated large output, two failed tool attempts, or the Architect summarizing data instead of deciding. Reroute remaining work to Luna Max or bounded programmatic calls. Mention optimization only when routing changes.

## Child lifecycle

- Keep at most one reusable Verifier and at most one reusable Maintainer. Reuse or start Engineer, Verifier, Maintainer, or read-only Scout. Send a follow-up to a reachable role thread before replacement.
- Before delegation, confirm authority, task or inquiry, paths or source boundary, acceptance, proof, and stop. A child cannot widen a trigger, choose role, or hand work to a sibling. Solo applies locally.
- Keep one reachable child thread for each role.
- A qualified pair may use two Engineers, two Scouts, or one of each; sidecars remain one each.
- Only Architect spawns or redirects; children never spawn or hand work to siblings.
- The Architect owns each child name at spawn time. A valid name uses one lowercase role prefix and one Greek suffix. The Architect allocates the next never-used label from `alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.
- The Architect supplies the exact `task_name` and keeps it with the reusable thread. Use `task_name=engineer_beta` for beta Engineer. A child never chooses or changes its task name. A replacement takes the next label.
- After all 24 labels, recycle the earliest label from an unreachable thread. No duplicates. Rehydrate an allowed replacement from role, task or inquiry, procedure, checkpoint, and latest unresolved result.
- Replace a role only for unavailability, stale assumptions after correction, user reset, or required tool, permission, or runtime change. Announce role, identity, context reset reason, and replacement action.

## Shared handoff envelope

- Arrow sequence is fact order, not output wording: `<task or inquiry> -> <outcome> -> <owned boundary> -> <contract> -> <proof> -> <stop>`. Each child handoff begins with a short settled purpose and natural prose; replace slots with project facts and omit slot labels. Writer handoffs name mutable paths, stable read paths, incidental output/cache, commands, external targets, and stop conditions.
- Children call the lead Architect. The Architect speaks as I. Payloads come from the Architect; children do not infer decisions, public behavior, acceptance, or paths.
- After each checkpoint, the Architect reviews the diff, architecture, scope, and contract alignment in concise natural prose.

## Communication

- Every child update starts with work or current state. Report material phase changes. Use at most two useful heartbeats at two-minute intervals for silent commands.
- Routine user commentary, child updates, child return messages, and final answers omit full checkpoint fingerprints. Report abstract status facts: source identity without full fingerprint, running/passed/stopped state, mismatch reason, and next action. Show details only for explicit audit or debugging.

## Role-specific rules

### Engineer

- Engineer cannot start until the visible plan exists; the task matches one durable plan item. It receives one task and settled decision envelope.
- Engineer owns targeted development checks and code-local truth. Stop for missing architecture, interface, dependency, behavior, acceptance, path, or scope.

### Scout

- The Architect supplies a question and source boundary without a preferred answer. Scout is read-only and never edits repository files.
- Scout supports bounded repo or contract mapping, research, reproduction or log reduction, change impact, edge-case or test candidates, and task-size or architecture contradiction review. Avoid Scout for a trivial one-file lookup.
- Scout returns citations, conflicts, unknowns, decision impact, and sources. Architect decides. No task until findings require a write.

### Maintainer

- Maintainer replays guided or recorded procedures exactly. It never repairs source, invents targets, changes procedures, or retries state-changing failure without authority.
- Maintainer owns each recorded operation run and returns evidence once. After Engineers stop and Architect review, Maintainer synchronizes affected shared narrative documents before final checkpoint.

### Verifier

- Verifier receives acceptance and the exact checkpoint. It independently reruns acceptance proof and one planned regression command, skips Engineer-only targeted checks, and may repeat only a disputed operation.
- Run the full suite only when the task or repository contract requires it. Consume Maintainer evidence.

## Model and spawn

- Standard child roles use direct native routing. Set `model=gpt-5.6-luna`, `reasoning_effort=max`, and non-full-history `fork_turns`. Omit `agent_type`.
- Luna Max uses Standard service by default, so normal spawns omit `service_tier`; never use `low` or silently reduce the requested model or effort.
- When user explicitly enables Fast children, record preference and use `service_tier=priority` for new or replaced Luna spawns. A priority failure must retry Luna max without `service_tier` as a Standard retry.
- If Luna remains unavailable, directly spawn `gpt-5.6-terra` at `xhigh` with non-full-history `fork_turns`, `model=gpt-5.6-terra`, and `reasoning_effort=xhigh`, without `service_tier` or `agent_type`.
- Terra `xhigh` fallback and Architect remain Standard unless overridden. Full history, automatic defaults, inherited profiles, silent fallback, effort downgrade, and incompatible forks are routing failures.
- After a Codex update, run one bounded profile smoke test before Luna handoff. Confirm Luna `max`; announce failure before fallback.
- Before every spawn, resolve role, trigger, mode, authority, models, reachable thread, label, profile, service tier, handoff, and reporting contract. Reject vague, duplicate, feature-based, counter-based, task-identifier, or arbitrary labels.

## Checkpoint barrier

1. Require all active work children to stop before integration.
2. Architect reviews the combined implementation and scopes.
3. Run any shared source-changing formatter or generator serially; Architect reviews resulting changes.
4. Maintainer synchronizes affected shared docs through an impact-directed pass.
5. Pause all writers and identify the checkpoint by commit or exact working-tree fingerprint for machine verification. The Architect hands that exact identity to the Verifier; require the sidecar to confirm the identity before acting and machine-check equality. After commit, use the release tag or short commit ID.
6. One Verifier confirms checkpoint equality without repeating the full fingerprint in the visible return, then checks both acceptance sets, assigned-path separation, semantic interaction, and documentation parity.
7. Maintainer runs required build, package, deploy, flash, runtime, or smoke operations serially against that accepted source checkpoint. Invalidate the result after any relevant source change.

## Return and stop conditions

- Children stop when scope, assumptions, checkpoint, authority, or proof is unclear. Only Architect integrates returns and decides disposition.
- Engineer edits only assigned implementation paths. Maintainer edits only assigned shared-document paths; Verifier and Scout are read-only. No child edits `tasks.csv` or runs Git operations.
- Architect reviews returns before integration or closeout. Dependent work waits for architecture and checkpoint verification. Sidecars stop after source change.
- On overlap, stop before the shared resource and report the collision and checkpoint. Pause affected writers; Architect serializes or revises scope; invalidate read findings after a source change. A child never integrates sibling work.
