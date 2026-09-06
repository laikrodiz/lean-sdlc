# Subagent Policy

This file owns Architect routing, allocation, and handoffs. Children use [child.md](child.md), not this orchestration procedure.

## Authority and modes

The Architect owns intent, public behavior, architecture, material assumptions, interfaces, permissions, task ownership, acceptance, conflict resolution, integration, and final signoff. Read authoritative contracts, decisive cited evidence, and contract-sensitive changes before acceptance. Never substitute confidence for required independent proof. The selected Architect model and effort remain unchanged by routing.

Assisted is the default; Solo is lead-only. These are the only modes. Restore owner, mode, and child tier after startup, resume, clear, or compaction. Missing or invalid state restores Assisted with Standard children. Fast children require user opt-in. Never silently change the selected Architect model or effort, or switch to Solo because a child is slow. If delegation is unavailable, report the limitation and obtain direction before changing modes.

## Route the current work

Apply these decisions in order. Serialization restricts concurrency, not role ownership.

1. Keep unresolved product, architecture, scope, permission, or acceptance decisions with the Architect. Do not delegate unresolved user intent.
2. In Solo, perform remaining work locally under the same task and proof gates. Solo remains lead-only.
3. Apply the existing [Quick Fix](plan.md#quick-fix-classification) rules when eligible. Do not start a child per fix.
4. Keep an eligible Routine Quick Fix with the Architect under the Quick Fix rules. The Architect may retain rare, bounded Critical implementation when design and coding coupling risks substantial misunderstanding or repeated redesign during handoff. State the reason briefly. Keep independent proof. Do not absorb surrounding Routine work.
5. Use Scout for broad, cross-boundary, multi-platform, or multi-version discovery and evidence reduction. A trivial lookup does not need Scout.
6. Route settled Routine non-Quick-Fix implementation to Engineer. Route settled Critical implementation by the same risk-benefit choice. Critical risk does not automatically route implementation to the Architect. Include related tests and mechanical consistency updates inside the Engineer's owned boundary.
7. Use Verifier when [Verify](verify.md) requires independent review. Use Maintainer for shared documentation or recorded operations. Maintainer may draft separate documents from approved facts during implementation; confirm them against actual results before acceptance.

## External tools and execution economy

Apply the same roles and routing precedence to plugins, MCP, connectors, CAD, databases, and hardware. The Architect owns target, permission, constraints, and decisions. Delegate substantial external-tool work when expected time or context savings outweigh handoff and verification costs. Assess complexity, output volume, repeated operations, and diagnostic scope. Call count and tool discovery are cues, not mandatory delegation triggers. One bounded probe may settle the assignment. Never let two agents mutate the same external target.

Group independent read-only calls and reduce logs inside the assigned child. Use direct calls for mutations, approvals, and judgment-sensitive steps. Reuse the same child for the same tool and project; replace only when its context or capabilities no longer fit. Return conclusions, evidence locations, errors, and unknowns, not transcripts.

If repeated raw output or routine tool work consumes Architect context, reroute remaining mechanics. Read selected instructions, contracts, acceptance, patches, and decisive evidence completely; do not load entire codebases by default. Reuse existing maps, build graphs, and cited source locations. Refresh only changed or unresolved boundaries. Do not warm caches artificially or promise cache hits.

Before retaining new automation, follow [operations.md](operations.md). Profile before rewriting slow infrastructure tests. Compare representative work for elapsed time, token use, repeated commands, and escaped defects before claiming savings. Do not add telemetry or a new evaluation framework for this comparison.

## Independence gate

Allocate useful children within native runtime capacity. Do not impose a fixed workflow-agent or Engineer count. Count every active descendant, including nested Verifiers. Give each child unique mutable ownership. This capacity rule does not create a coordinator role or permit uncontrolled spawning.

Before each parallel assignment, confirm:

- Each task has independent acceptance and all ledger dependencies are `Done`.
- Writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap.
- Shared read-only contracts are stable. No child depends on another child's unfinished behavior.
- Coordination and combined verification cost less time than serial work.

Two Engineers may share stable read-only interfaces, not changes to an interface, schema, manifest, lockfile, generator, or migration. Commands may match if their mutable inputs and outputs remain separate. The `tasks.csv` lock protects only the ledger. The Architect is also a writer and must not enter an active child's owned boundary.

Engineer/Scout, Scout/Scout, or Engineer/Maintainer can overlap under this gate. A Verifier can check a completed independent boundary while unrelated work continues. Its source, dependencies, environment, and test resources must remain stable. Final release checks freeze all inputs that enter the release. Do not create branches or worktrees for parallelism. If separation or benefit is unclear, run serially.

## Allocate and reuse

Reuse a reachable child for the same role and relevant context before replacement. Keep reusable Maintainer and Verifier children when they remain reachable and useful. Allocate another Engineer or Scout only for a qualified assignment. Completed children remain reusable through `followup_task`.

Only the Architect allocates children. For one settled task, it may preauthorize an Engineer to spawn or reuse one exact named read-only Verifier. The handoff must include that Verifier's profile, boundary, proof, capacity, and return route. No other descendant spawning is allowed. Combined checkpoints use one Architect-started Verifier.

The Engineer and its preauthorized Verifier may exchange scoped findings without Architect relay. Pause the verified boundary during checks. Local corrections may continue within the approved contract. Escalate changed architecture, behavior, acceptance, permissions, ownership, disputed evidence, or repeated equivalent failures without new evidence.

Do not integrate active, unaccepted, or unassigned sibling work. An explicitly assigned integration outcome may combine accepted pieces within its owned boundary. Never take arbitrary ownership.

Choose a lowercase role prefix and Greek suffix, such as `engineer_beta`. Standard roles are Engineer, Scout, Maintainer, and Verifier; custom roles need direct user authority. Allocate the next unused label:

`alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.

Keep the exact name with the reusable child. After the alphabet is exhausted, recycle an unused role-label combination from an unreachable child. Never duplicate a reachable identity or use task IDs, feature names, or counters as names.

## Model and spawn

- Standard roles: `model=gpt-5.6-luna`, `reasoning_effort=max`, and `fork_turns=none` or a positive bounded history value. Omit `agent_type`. Preserve the selected Architect model and effort.
- Standard Luna omits `service_tier`. User-enabled Fast children use `service_tier=priority` only if the native tool exposes it. Report unsupported settings; never invent arguments.
- If priority fails, retry Luna Max once without `service_tier`. If Luna remains unavailable, announce the fallback and use `model=gpt-5.6-terra`, `reasoning_effort=xhigh`, bounded history, and no `service_tier` or `agent_type`.
- Never silently lower reasoning, inherit an unspecified child profile, or combine overrides with full-history forks. The Architect's profile remains unchanged.
- Run one bounded profile smoke check after a relevant native model/tool change, not for each handoff. Before spawning, confirm mode, capacity, profile, name, reachable children, scope, authority, and return route.

## Handoff and finish

Before implementation, give a short public brief with the decision, reason, owned boundary, acceptance, and material risks. Do not repeat the complete child contract in that brief. Report decisions, not private chain-of-thought.

Give the child one atomic task or bounded inquiry. Put the precise task contract in the child assignment once. Include task ID, title, owner, both exact roots, writable paths, stable reads, incidental outputs, allowed commands, and targets. State relevant code, responsibilities, interfaces, data flow, mandatory sequencing, failure behavior, invariants, exclusions, decisions versus suggestions, Engineer freedom, acceptance, planned proof, and stop conditions. Include one concrete example or the reason for any choice where misunderstanding would matter. State whether the before-write gate passed. Use concise natural prose, not a mandatory table. Reused children receive the change in instructions plus relevant refreshed evidence, not repeated full history. Point them to [child.md](child.md).

For a small settled assignment, do not send routine Architect updates. For larger or uncertain work, split the assignment or define a specific decision or risk checkpoint before delegation. Do not use time or percentage thresholds for reporting.

A timeout, silence, or missed update does not mean failure. Use bounded adaptive waits without rapid polling. Interrupt or replace for a real blocker, collision, user request, failed/canceled/unavailable state, stale assumptions, or required capability change. Two unanswered status requests plus no active command or process may justify ending a stale turn. Explain the reason; elapsed time alone does not justify takeover.

Routine progress stays in the child thread. Parent messages are for immediate decisions or blockers; completion is one final return. Do not echo unchanged reports. Review contract-sensitive results and show one short alignment signoff before acceptance.

Critical acceptance requires independent verification, including when the Architect writes the implementation. See [verify.md](verify.md) for the Solo missing-proof gate.

Batch shared documentation and common proof across atomic tasks. Stop relevant writers, review combined changes, run required shared generators serially, and synchronize actual documentation. Then apply [Verify](verify.md) once to the combined boundary. Keep every task's acceptance separate. Use [Operations](operations.md) for delivery from the accepted source; close only when required evidence exists. Use a release tag or short commit ID after commit, not visible full fingerprints.
