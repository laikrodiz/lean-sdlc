# Subagent Policy

This file owns Architect routing, allocation, and handoffs. Children use [child.md](child.md), not this orchestration procedure.

## Authority and modes

The Architect owns intent, public behavior, architecture, material assumptions, interfaces, permissions, task ownership, acceptance, conflict resolution, integration, and final signoff. Read authoritative contracts, decisive cited evidence, and contract-sensitive changes before acceptance. Never substitute confidence for required independent proof.

Assisted is the default; Solo is lead-only. These are the only modes. Restore owner, mode, and child tier after startup, resume, clear, or compaction. Missing or invalid state restores Assisted with Standard children. Fast children require user opt-in. Never silently change the selected Architect model or effort, or switch to Solo because a child is slow. If delegation is unavailable, report the limitation and obtain direction before changing modes.

## Route the current work

Apply these decisions in order. Serialization restricts concurrency, not role ownership.

1. Keep unresolved product, architecture, scope, permission, or acceptance decisions with the Architect. Do not delegate unresolved user intent.
2. In Solo, perform remaining work locally under the same task and proof gates.
3. Apply the existing [Quick Fix](plan.md#quick-fix-classification) rules when eligible. Do not start a child per fix.
4. Keep one understood, settled local change with the Architect when handoff overhead exceeds the work. The Architect may also retain bounded judgment-intensive implementation when delegation would duplicate design effort or require extensive explanation and correction. State the reason briefly. Keep the visible plan, owned task, before-write gate, acceptance, and risk-based independent review. Delegate separable substantial execution; this is not blanket permission to do everything locally.
5. Use Scout for broad, cross-boundary, multi-platform, or multi-version discovery and evidence reduction. A trivial lookup does not need Scout.
6. Use Engineer for other settled implementation, including related tests and mechanical consistency updates within its owned boundary.
7. Use Verifier when [Verify](verify.md) requires independent review. Use Maintainer for shared documentation or recorded operations. Maintainer may draft separate documents from approved facts during implementation; confirm them against actual results before acceptance.

## External tools and execution economy

Apply the same roles and routing precedence to plugins, MCP, connectors, CAD, databases, and hardware. The Architect owns target, permission, constraints, and decisions. Delegate substantial external-tool work when expected time or context savings outweigh handoff and verification costs. Assess complexity, output volume, repeated operations, and diagnostic scope. Call count and tool discovery are cues, not mandatory delegation triggers. One bounded probe may settle the assignment. Never let two agents mutate the same external target.

Group independent read-only calls and reduce logs inside the assigned child. Use direct calls for mutations, approvals, and judgment-sensitive steps. Reuse the same child for the same tool and project; replace only when its context or capabilities no longer fit. Return conclusions, evidence locations, errors, and unknowns, not transcripts.

If repeated raw output or routine tool work consumes Architect context, reroute remaining mechanics. Read selected instructions, contracts, acceptance, patches, and decisive evidence completely; do not load entire codebases by default. Reuse existing maps, build graphs, and cited source locations. Refresh only changed or unresolved boundaries. Do not warm caches artificially or promise cache hits.

Before retaining new automation, follow [operations.md](operations.md). Profile before rewriting slow infrastructure tests. Compare representative work for elapsed time, token use, repeated commands, and escaped defects before claiming savings. Do not add telemetry or a new evaluation framework for this comparison.

## Independence gate

Use at most two active work children. A third child may be read-only when native capacity permits useful elapsed-time savings. Never exceed two concurrent Engineers. Count all descendants, including nested Verifiers.

Before each parallel assignment, confirm:

- Each task has independent acceptance and all ledger dependencies are `Done`.
- Writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap.
- Shared read-only contracts are stable. No child depends on another child's unfinished behavior.
- Coordination and combined verification cost less time than serial work.

Two Engineers may share stable read-only interfaces, not changes to an interface, schema, manifest, lockfile, generator, or migration. Commands may match if their mutable inputs and outputs remain separate. The `tasks.csv` lock protects only the ledger. The Architect is also a writer and must not enter an active child's owned boundary.

Engineer/Scout, Scout/Scout, or Engineer/Maintainer can overlap under this gate. A Verifier can check a completed independent boundary while unrelated work continues. Its source, dependencies, environment, and test resources must remain stable. Final release checks freeze all inputs that enter the release. Do not create branches or worktrees for parallelism. If separation or benefit is unclear, run serially.

## Allocate and reuse

Reuse a reachable child for the same role and relevant context before replacement. Keep one reusable Maintainer and Verifier; use a second Engineer or Scout only for a qualified parallel assignment. Completed children remain reusable through `followup_task`.

Only the Architect allocates children. For one settled task, it may preauthorize an Engineer to spawn or reuse one exact named read-only Verifier. The handoff must include that Verifier's profile, boundary, proof, capacity, and return route. No other descendant spawning is allowed. Combined checkpoints use one Architect-started Verifier.

The Engineer and its preauthorized Verifier may exchange scoped findings without Architect relay. Pause the verified boundary during checks. Local corrections may continue within the approved contract. Escalate changed architecture, behavior, acceptance, permissions, ownership, disputed evidence, or repeated equivalent failures without new evidence. Never let a child integrate sibling work.

Choose a lowercase role prefix and Greek suffix, such as `engineer_beta`. Standard roles are Engineer, Scout, Maintainer, and Verifier; custom roles need direct user authority. Allocate the next unused label:

`alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.

Keep the exact name with the reusable child. After the alphabet is exhausted, recycle an unused role-label combination from an unreachable child. Never duplicate a reachable identity or use task IDs, feature names, or counters as names.

## Model and spawn

- Standard roles: `model=gpt-5.6-luna`, `reasoning_effort=max`, and `fork_turns=none` or a positive bounded history value. Omit `agent_type`.
- Standard Luna omits `service_tier`. User-enabled Fast children use `service_tier=priority` only if the native tool exposes it. Report unsupported settings; never invent arguments.
- If priority fails, retry Luna Max once without `service_tier`. If Luna remains unavailable, announce the fallback and use `model=gpt-5.6-terra`, `reasoning_effort=xhigh`, bounded history, and no `service_tier` or `agent_type`.
- Never silently lower reasoning, inherit an unspecified child profile, or combine overrides with full-history forks. The Architect's profile remains unchanged.
- Run one bounded profile smoke check after a relevant native model/tool change, not for each handoff. Before spawning, confirm mode, capacity, profile, name, reachable children, scope, authority, and return route.

## Handoff and finish

Before implementation, briefly show the decision, reason, owned boundary, preserved behavior, acceptance, and stop condition. Include a rejected option only when it explains a material tradeoff. Report decisions, not private chain-of-thought. Specify difficult choices and contracts, not exhaustive implementation pseudocode.

Give the child one atomic task or bounded inquiry. Include task ID, title, owner, both exact roots, writable paths, stable reads, incidental outputs, allowed commands and targets, acceptance, planned proof, and stop conditions. State whether the before-write gate passed. Use concise natural prose, not a mandatory table. Reused children receive the change in instructions plus relevant refreshed evidence, not repeated full history. Point them to [child.md](child.md).

A timeout, silence, or missed update does not mean failure. Use bounded adaptive waits without rapid polling. Interrupt or replace for a real blocker, collision, user request, failed/canceled/unavailable state, stale assumptions, or required capability change. Two unanswered status requests plus no active command or process may justify ending a stale turn. Explain the reason; elapsed time alone does not justify takeover.

Routine progress stays in the child thread. Parent messages are for immediate decisions or blockers; completion is one final return. Do not echo unchanged reports. Review contract-sensitive results and show one short alignment signoff before acceptance.

Batch shared documentation and common proof across atomic tasks. Stop relevant writers, review combined changes, run required shared generators serially, and synchronize actual documentation. Then apply [Verify](verify.md) once to the combined boundary. Keep every task's acceptance separate. Use [Operations](operations.md) for delivery from the accepted source; close only when required evidence exists. Use a release tag or short commit ID after commit, not visible full fingerprints.
