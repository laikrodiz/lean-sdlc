# Subagent Policy

## Scope and modes

- The Architect is the sole authority for product intent, public behavior, architecture, assumptions, acceptance, permissions, task ownership, conflict resolution, and final signoff. The Architect always owns intent, public behavior, architecture, tasks, acceptance, integration, and closeout. It retains those decisions through every child handoff and reviews contract-sensitive semantic changes before integration.
- The Architect reads authoritative intent and contracts, decisive cited evidence, and focused final changes before integration.
- The Architect never sends unresolved user input to a child, writes inside an active child boundary, accepts unreviewed output, or replaces independent proof with confidence.
- The standard child roles are Engineer, Maintainer, Verifier, and Scout. Custom roles need direct user authority. Standard spawn profile enforcement does not cover custom roles.
- Assisted mode normally delegates routine discovery, evidence, implementation, checks, documentation, and recorded operations. Assisted mode is the default.
- Solo mode is lead-only. Assisted and Solo are the only orchestration modes.
- Missing or invalid state restores Assisted with Standard children. Lifecycle restoration restores owner, mode, and tier after startup, resume, clear, or compaction.
- Fast children need user opt-in.
- The Architect is the user-selected lead. An explicit user Architect profile controls it. Apply the required child profile before delegation; if unavailable, use Solo.
- The Architect direct path is one bounded mechanical exception with one narrow proof command. Settled separable work remains Engineer work; Solo keeps execution with the Architect under the same rules.

## Quick Fix

- Quick Fix follows [plan.md](plan.md). Architect may execute it in either mode. Do not spawn Engineer, Maintainer, or Verifier per Quick Fix; shared batch may use Verifier when triggered.

## Role-routing precedence

Apply this stage-aware chain before the first command. The first matching condition wins:

1. Keep unresolved product, architecture, scope, permission, or acceptance decisions with the Architect.
2. Force work with a shared mutable resource to run serially, then apply this chain to its current stage.
3. Route broad, read-only, multi-platform, multi-version, or cross-boundary evidence inquiries to Scout.
4. Route settled mutable implementation with paths, interfaces, acceptance, proof, and no open decision to Engineer.
5. Route independent proof to Verifier only at a proof checkpoint.
6. Route shared documentation or recorded operations to Maintainer only after accepted implementation, or when documentation-only or operation work is the current stage.
7. Use the narrow Architect direct path or Solo for all remaining bounded work.

Use the one bounded mechanical exception above or keep remaining bounded work with the Architect in Solo.

Before each child handoff, the Architect posts a visible pre-handoff design brief. It states the reason, selected decision, affected ownership, interfaces, and invariants, any material rejected option when useful, child decision limits, acceptance, proof, and stop. It reports the decision and relevant grounds, never chain-of-thought.

## Independence gate

- At most two active children run after a resource gate passes. This is universal independence gate, and descendants count toward the limit. Each child has exclusive scope and settled contract; all dependencies are `Done`; elapsed time should decrease.
- Two Engineers require separate mutable code and test paths, stable read paths, incidental outputs or caches, commands, services, ports, devices, and external targets; no shared public interface, schema, manifest, lockfile, generator, migration, or mutable fixture; independent acceptance and proof.
- Immediately before a parallel Engineer spawn, the Architect revalidates the resource boundary: separate mutable resources, no unfinished dependency, and meaningful elapsed-time savings after coordination and verification. If conditions changed, fall back to serial execution.
- The Architect is a writer and must not edit child-owned paths. One Architect writer group owns a worktree. The `tasks.csv` lock protects only the ledger.
- Engineer/Engineer requires strict isolation. Engineer/Scout requires a stable separate read boundary. Scout/Scout may overlap stable sources for independent questions. A Scout may overlap one Verifier or Maintainer only for future work with separate resources.
- Maintainer and Verifier stay serial with writers. Project-native command/test parallelism stays inside one child when safe.
- Apply every role trigger before the first command. Assisted delegation is mandatory beyond the Architect direct path.
- One-task writers continue through implementation and targeted proof. For combined, parallel, release, or final-batch checkpoints, implementation writers stop before integration; no writer overlaps documentation synchronization, verification, or stateful operations. Shared tests, docs, generators, and operations run serially. One Verifier checks the combined checkpoint.

## External tools

- External-tool routing starts before substantial plugin, MCP, connector, CAD, database, deployment, or similar work. Architect keeps target, permissions, constraints, architecture, decisions, and final acceptance. Architect may make one bounded probe; delegate remaining routine work after it.
- Delegate before work when more than three external calls are expected; large schemas/logs/inventories/search results; one operation repeats across objects; tool discovery is required; error recovery needs several diagnostic calls; or output needs reduction before a decision.
- Route read-heavy discovery and reduction to Scout, including cross-boundary source and log evidence; route approved mutations to Engineer, repeated build/export/import/deploy/flash procedures to Maintainer, and independent checks to Verifier.
- Use bounded programmatic tool calling for deterministic reads or reductions. Inside the assigned child, use direct calls for mutations, approvals, or judgment-sensitive steps. Routine mutation calls belong to the assigned Engineer or Maintainer, not the Architect.
- One agent owns each mutable external target. Never let two agents mutate the same project, database, deployment, or hardware target.
- Child returns conclusions, errors, artifact paths or IDs, and unresolved questions, not a raw transcript. Reuse the same child for the same tool and project. Replace after a material tool or target change.
- Token-waste signals include compaction during tool work, several direct routine calls, repeated large output, two failed tool attempts, or the Architect summarizing data instead of deciding. Reroute remaining work to Luna Max or bounded programmatic calls. Mention optimization only when routing changes.

## Execution economy

- Group independent read-only discovery into bounded calls. Use follow-ups only for unresolved questions.
- Bound output only when shape or presence is enough. Require complete reads for selected skill instructions, contracts, acceptance, proof, patches, and exact evidence.
- Permit one grouped read-only environment probe before setup. Setup and installation require owned authority. Never install dependencies automatically.
- Use bounded adaptive waits. Avoid rapid polling.
- Route repeated equivalent failures to Diagnose. Stop patch loops.

## Child lifecycle

- Keep at most one reusable Verifier and at most one reusable Maintainer. The Architect may reuse or start Engineer, Verifier, Maintainer, or read-only Scout; an authorized Engineer may start or reuse only the exact preauthorized Verifier. Send a follow-up to a reachable role thread before replacement.
- Before delegation, the Architect uses the visible pre-handoff design brief and confirms authority, task or inquiry, paths or source boundary, acceptance, proof, and stop. A child cannot widen a trigger, choose role, or hand work to a sibling. Solo applies locally.
- Keep one reachable child thread for each role.
- A qualified pair may use two Engineers, two Scouts, or one of each only when no sidecar is active; every Verifier or Maintainer descendant counts toward the same two-child limit.
- The Architect controls child allocation and redirection. It allocates and preauthorizes the exact named Verifier. An authorized Engineer may spawn or reuse that one read-only Verifier for its single settled task. No other child may spawn, and the Verifier cannot spawn or hand work to a sibling.
- The Architect owns each child name at spawn time. A valid name uses one lowercase role prefix and one Greek suffix. The Architect allocates the next never-used label from `alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.
- The Architect supplies the exact `task_name` and keeps it with the reusable thread. Use `task_name=engineer_beta` for beta Engineer. A child never chooses or changes its task name. A replacement takes the next label.
- After all 24 labels, recycle the earliest label from an unreachable thread. No duplicates. Rehydrate an allowed replacement from role, task or inquiry, procedure, checkpoint, and latest unresolved result.
- A running lifecycle state means available. A parent wait timeout, missed update, or silence is not failure. The Architect may request status and wait again. Routine progress stays in the child thread. A completed child sends one final return and ends its active turn. The completed thread remains reachable for later `followup_task` reuse.
- Interrupt or replace only for an explicit blocker or an explicit conflict, user reset or request, system failed/canceled/unavailable state, stale assumptions, or required tool, permission, or runtime change. After two unanswered status requests and no reported active command or process, the Architect may interrupt a stale turn. Elapsed time alone is not failure. Announce role, identity, context reset reason, and replacement action.

## Shared handoff envelope

- Arrow sequence is fact order, not output wording: `<task or inquiry> -> <outcome> -> <owned boundary> -> <contract> -> <proof> -> <stop>`. Each child handoff begins with a short settled purpose and concise natural prose; replace slots with project facts and omit slot labels. Writer handoffs name mutable paths, stable read paths, incidental output/cache, commands, external targets, and stop conditions.
- Every implementation child receives task facts: task ID, title, owner, acceptance, proof, assigned paths, repository root, and skill root. Children do not locate repositories, skill roots, `tasks.csv`, or packaged helpers. Children do not run `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" <command>`, `python3 "<skill-root>/scripts/lean_check.py" "<repo-root>" <options>`, or `python3 "<skill-root>/scripts/session_state.py" --owner OWNER <options>`; the Architect runs those commands with the resolved roots.
- Engineer handoffs state focused semantic changes and targeted check results. Scout handoffs state reduced source, log, inventory, or cross-boundary evidence and citations. Verifier handoffs state acceptance and regression results with checkpoint equality or a stop reason. Maintainer handoffs state the recorded failure signal and authorized recovery status.
- Children call the lead Architect. The Architect speaks as I. Payloads come from the Architect; children do not infer decisions, public behavior, acceptance, or paths.
- For one task, Engineer continues through implementation and targeted proof. After the final Engineer return, Architect reviews it with one short visible alignment signoff covering architecture, scope, and contract alignment without echoing unchanged child facts. Review earlier only when immediate Architect action is required for a decision, blocker, collision, scope change, or proof mismatch.

## Communication

- Each child update stays 1–3 natural sentences. State the current action, why it matters, observed result or next action.
- Routine progress stays in the child thread and creates no explicit parent message. This includes the start restatement. Send an explicit parent message only when immediate Architect action is required for a blocker, collision, scope change, proof mismatch, or decision. At completion, send exactly one final return and no separate completion message.
- The Architect does not echo unchanged child facts.
- No child update includes greetings, role repetition, raw logs, full fingerprints, or scripted phrases. Keep communication concise. Do not create rigid templates.
- Routine user commentary, child return messages, and final answers omit full checkpoint fingerprints. Report abstract status facts: source identity without full fingerprint, running/passed/stopped state, mismatch reason, and next action. Do not repeat the full fingerprint in the visible return. Show details only for explicit audit or debugging.
- The Verifier retains local checkpoint values only. Do not persist values or expose full values in routine reports.

## Role-specific rules

### Engineer

- Engineer cannot start until the visible plan exists; the task matches one durable plan item. It receives one task and settled decision envelope.
- Engineer begins with a short visible natural restatement of the outcome, boundary, preserved behavior, proof, and stop condition. Engineer proceeds without an approval pause unless ambiguity exists.
- Engineer owns targeted development checks and code-local truth. Targeted proof is the smallest check for the changed behavior, run after a coherent implementation checkpoint and after a permitted correction. For one settled task, Engineer owns targeted proof and returns focused semantic changes and targeted check results. Engineer may fix only implementation defects that preserve settled behavior, architecture, interfaces, acceptance, paths, and permissions. Escalate any change to those items or when the same proof failure repeats.
- Approved scripts follow the operation contract in [operations.md](operations.md). A script does not grant authority.

### Scout

- The Architect supplies a question and source boundary without a preferred answer. Scout is read-only and never edits repository files.
- Scout supports bounded repo or contract mapping, research, reproduction or log reduction, broad source, log, inventory, or cross-boundary evidence reduction, change impact, edge-case or test candidates, and task-size or architecture contradiction review. Avoid Scout for a trivial one-file lookup.
- For a broad inquiry, the Architect names platform and version dimensions. Scout maps shared core, variants, affected coverage, cited evidence, and unknowns before broad reads. Architect reads decisive contracts and cited paths, expands one unresolved boundary at a time, and stops when decision evidence is sufficient. Scout returns source coverage, citations, conflicts, unknowns, decision impact, and sources. Reuse existing build graphs, manifests, and maps before creating anything. Architect decides. No task until findings require a write.

### Maintainer

- Maintainer replays guided or recorded procedures exactly. It never repairs source, invents targets, changes procedures, or retries state-changing failure without authority.
- Maintainer may classify a failure only when it matches a recorded operation failure signal. It may run only an already-authorized recorded recovery.
- Unknown, ambiguous, source-changing, or new retry behavior stops and routes to Diagnose/Scout and Architect.
- Maintainer owns each recorded operation run and returns evidence once. Follow [operations.md](operations.md) for automation candidates and record/replay after accepted implementation. After Engineers stop and Architect review, Maintainer synchronizes affected shared narrative documents before final checkpoint.
- For documentation-only work or accepted checkpoints with shared-document impact, Maintainer owns shared narrative truth and indexes.
- Maintainer runs an impact-directed synchronization and detects missing triggers, stale documents, and oversized semantic units. Maintainer never invents product or architecture.
- Architect approves meaning and document splits before Maintainer records them.

### Verifier

- Each expensive proof command has one owner per checkpoint. Engineer owns the targeted command after a coherent implementation checkpoint and after a permitted correction. Without independent verification, Architect decides acceptance from existing evidence and runs only a missing acceptance command. With independent verification, Verifier owns acceptance and regression commands. No owner reruns an identical command unless independent proof, disputed evidence, or repository policy requires it.
- The Architect allocates and preauthorizes the exact named Verifier. An authorized Engineer may spawn or reuse that one read-only Verifier for its single settled task when risk-based independent proof is required. Verifier receives acceptance and the settled source boundary. Verifier never changes tracked source, configuration, documentation, the ledger, or state. It may create named temporary or incidental test outputs outside tracked truth. Before and after proof, Verifier runs `python3 "<skill-root>/scripts/checkpoint.py" --repo "<repo-root>" PATH [PATH ...]` over the same explicit task-owned paths and compares the returned SHA-256 values locally. An Engineer stops writing while its nested read-only Verifier checks. Engineer may resume only for permitted implementation corrections, then reruns proof. The Verifier independently runs acceptance proof for observable completion and one planned regression proof for affected-boundary risk, then skips Engineer-only targeted checks. It must not repeat an identical targeted command unless the repetition supplies independent proof, resolves disputed evidence, or repository policy requires it.
- Verifier blocks if the local values differ. It does not persist values or expose full values in routine reports. Do not make the Architect calculate them. Named temporary or incidental test outputs remain outside tracked truth.
- Run the full suite only for a release, broad shared contracts, migrations or build graphs, an explicit repository requirement, or when no trustworthy selector exists. Consume Maintainer evidence.

## Model and spawn

- Standard child roles use direct native routing. Set `model=gpt-5.6-luna`, `reasoning_effort=max`, and non-full-history `fork_turns`. Omit `agent_type`.
- Luna Max uses Standard service by default, so normal spawns omit `service_tier`; never use `low` or silently reduce the requested model or effort.
- When user explicitly enables Fast children, record preference and use `service_tier=priority` for new or replaced Luna spawns. A priority failure must retry Luna max without `service_tier` as a Standard retry.
- If Luna remains unavailable, directly spawn `gpt-5.6-terra` at `xhigh` with non-full-history `fork_turns`, `model=gpt-5.6-terra`, and `reasoning_effort=xhigh`, without `service_tier` or `agent_type`.
- Terra `xhigh` fallback and Architect remain Standard unless overridden. Full history, automatic defaults, inherited profiles, silent fallback, effort downgrade, and incompatible forks are routing failures.
- After a Codex update, run one bounded profile smoke test before Luna handoff. Confirm Luna `max`; announce failure before fallback.
- Before every spawn, resolve role, trigger, mode, authority, models, reachable thread, label, profile, service tier, handoff, and reporting contract. Reject vague, duplicate, feature-based, counter-based, task-identifier, or arbitrary labels.

## Checkpoint barrier

1. For combined, parallel, release, or final-batch checkpoints, require all active work children to stop before integration.
2. Architect reviews the combined implementation and scopes.
3. Run any shared source-changing formatter or generator serially; Architect reviews resulting changes.
4. Maintainer synchronizes affected shared docs through an impact-directed pass.
5. Pause all writers for machine verification. The Verifier runs the packaged checkpoint helper before and after proof over the same explicit task-owned paths, then compares values locally. Do not persist values or expose full values in routine reports. For combined, parallel, release, or final-batch checkpoints, the Architect starts one Verifier after writers stop.
6. The Verifier checks both acceptance sets, assigned-path separation, semantic interaction, and documentation parity. It blocks when the local checkpoint values differ.
7. After commit, use the release tag or short commit ID for later source identity.
8. Maintainer runs required build, package, deploy, flash, runtime, or smoke operations serially against that accepted source checkpoint. Invalidate the result after any relevant source change.

## Return and stop conditions

- Children stop when scope, assumptions, checkpoint, authority, or proof is unclear. Only Architect integrates returns and decides disposition.
- Engineer edits only assigned implementation paths. Maintainer edits only assigned shared-document paths; Verifier and Scout are read-only. No child edits `tasks.csv` or runs Git operations.
- Architect reviews returns before integration or closeout. Dependent work waits for architecture and checkpoint verification. Sidecars stop after source change.
- On overlap, stop before the shared resource and report the collision and checkpoint. Pause affected writers; Architect serializes or revises scope; invalidate read findings after a source change. A child never integrates sibling work.
