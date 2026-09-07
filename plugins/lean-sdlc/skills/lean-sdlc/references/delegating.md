# Delegating Orchestration

Load this file only for Delegating. It owns legacy Engineer routing, allocation, and handoffs. Children use [child.md](child.md), not this orchestration procedure.

Load [mode-common.md](mode-common.md) and [support.md](support.md) with this file. The selected mode controls whether this file is loaded.

## Authority and routing

The Architect owns intent, public behavior, architecture, material assumptions, interfaces, permissions, task ownership, acceptance, conflict resolution, integration, and final signoff. Read authoritative contracts, decisive evidence, and contract-sensitive changes before acceptance. Never substitute confidence for required independent proof.

Delegating preserves the legacy Engineer routing. Restore owner, mode, and child tier after startup, resume, clear, or compaction. Legacy saved Assisted state maps to Delegating. Never silently change the selected Architect model or effort, or switch modes because a child is slow. If delegation is unavailable, report the limitation and obtain direction before changing modes.

Apply these decisions in order. Serialization restricts concurrency, not role ownership.

1. Keep unresolved product, architecture, scope, permission, or acceptance decisions with the Architect. Do not delegate unresolved user intent.
2. Apply the existing [Quick Fix](plan.md#quick-fix-classification) rules when eligible. Do not start a child per fix. Keep an eligible Routine Quick Fix with the Architect.
3. Retain rare, bounded Critical implementation only when design and coding coupling risks substantial misunderstanding or repeated redesign during handoff. State the reason briefly, keep independent proof, and do not absorb surrounding Routine work.
4. Use Scout for broad, cross-boundary, multi-platform, or multi-version discovery and evidence reduction. A trivial lookup does not need Scout.
5. Route settled Routine non-Quick-Fix implementation to Engineer. Route settled Critical implementation by the same risk-benefit choice. Critical risk does not automatically route implementation to the Architect. Include related tests and mechanical consistency updates inside the Engineer's owned boundary.
6. Use Verifier when [Verify](verify.md) requires independent review. Use Maintainer for shared documentation or recorded operations. Confirm Maintainer drafts against actual results before acceptance.

## External tools and execution economy

Apply the same routing precedence to plugins, MCP, connectors, CAD, databases, and hardware. The Architect owns target, permission, constraints, and decisions. Delegate substantial external-tool work when expected time or context savings outweigh handoff and verification costs. Assess complexity, output volume, repeated operations, and diagnostic scope. One bounded probe may settle the assignment. Never let two agents mutate the same external target.

Group independent read-only calls and reduce logs inside the assigned child. Use direct calls for mutations, approvals, and judgment-sensitive steps. Reuse the same child for the same tool and project while its context remains relevant. Return conclusions, evidence locations, errors, and unknowns, not transcripts.

Read selected instructions, contracts, acceptance, patches, and decisive evidence completely. Do not load entire codebases by default. Reuse existing maps, build graphs, and cited source locations. Refresh only changed or unresolved boundaries. Before retaining new automation, follow [operations.md](operations.md). Profile before rewriting slow infrastructure tests. Do not add telemetry or a new evaluation framework for comparisons.

## Parallel assignment gate

Allocate useful children within native runtime capacity. Count every active descendant, including nested Verifiers. Give each child unique mutable ownership. Before each parallel assignment, confirm:

- Each task has independent acceptance and all ledger dependencies are `Done`.
- Writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap.
- Shared read-only contracts are stable. No child depends on another child's unfinished behavior.
- Coordination and combined verification cost less time than serial work.

Two Engineers may share stable read-only interfaces, not changes to an interface, schema, manifest, lockfile, generator, or migration. Commands may match when mutable inputs and outputs remain separate. The `tasks.csv` lock protects only the ledger. The Architect must not enter an active child's owned boundary.

Engineer/Scout, Scout/Scout, or Engineer/Maintainer can overlap under this gate. A Verifier can check a completed independent boundary while unrelated work continues. Its source, dependencies, environment, and test resources must remain stable. Freeze all inputs for final release checks. Do not create branches or worktrees for parallelism. If separation or benefit is unclear, run serially.

Do not integrate active, unaccepted, or unassigned sibling work. An explicitly assigned integration outcome may combine accepted pieces within its owned boundary. Never take arbitrary ownership.

## Delegating handoffs

Only the Architect allocates children. Reuse a reachable child for the same role and relevant context before replacement. Use [support.md](support.md) for native profiles, capacity, names, and reuse. For one settled task, the Architect may preauthorize an Engineer to spawn or reuse one exact named read-only Verifier. The handoff must include that Verifier's profile, boundary, proof, capacity, and return route. No other descendant spawning is allowed.

Before implementation, give a short public brief with the decision, reason, owned boundary, acceptance, and material risks. Do not repeat the complete child contract in that brief. Report decisions, not private chain-of-thought.

Give the Engineer one atomic task or bounded inquiry. Put the precise task contract in the child assignment once. Include task ID, title, owner, both exact roots, writable paths, stable reads, incidental outputs, allowed commands, targets, responsibilities, interfaces, data flow, sequencing, failure behavior, invariants, exclusions, decisions versus suggestions, freedom, acceptance, proof, and stop conditions. Include one concrete example or the reason for any choice where misunderstanding would matter. State whether the before-write gate passed. Point to [child.md](child.md) and [delegating-child.md](delegating-child.md).

For a small settled assignment, do not send routine Architect updates. For larger or uncertain work, split the assignment or define a specific decision or risk checkpoint before delegation. Do not use time or percentage thresholds for reporting. A timeout, silence, or missed update does not mean failure.

The Engineer and its preauthorized Verifier may exchange scoped findings without Architect relay. Pause the verified boundary during checks. Resolve permitted findings within the approved contract. Escalate changed architecture, behavior, acceptance, permissions, ownership, disputed evidence, or repeated equivalent failures without new evidence.

Review contract-sensitive results and show one short alignment signoff before acceptance. Critical acceptance requires independent verification, including Architect-written work. Batch shared documentation and common proof across atomic tasks. Stop relevant writers, review combined changes, run shared generators serially, and synchronize actual documentation. Then apply [Verify](verify.md) once to the combined boundary. Keep every task's acceptance separate. Use [Operations](operations.md) for delivery from the accepted source; close only when required evidence exists.
