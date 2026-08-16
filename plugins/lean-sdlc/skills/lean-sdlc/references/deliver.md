# Deliver

Use Deliver only when the cause, scope, architecture, owned `In Progress` task, visible Plan, measurable acceptance, and proof are settled.

Use [subagents.md](subagents.md) for child triggers, handoffs, and checkpoints.

1. Read the active task with context, acceptance, proof, and affected code.
2. Confirm the visible plan matches one durable task, or both tasks in a qualified pair.
3. Run the structural before-write check and declare allowed paths.
4. Build the smallest cohesive units through narrow contracts and a readable orchestrator. Keep direct code when extraction creates pass-through pieces.
5. Classify plausible boundary cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior.
6. Keep one durable task with one outcome, settled architecture and invariants, related paths, acceptance, proof, and stop conditions.
7. After implementation, the Architect reviews scope, architecture, contract alignment, and the exact checkpoint before Verify.
8. Use the policy checkpoint barrier and send its final source checkpoint to Verify first.
9. Apply [operations.md](operations.md) for required operations and consume Maintainer evidence without repeating accepted source proof.
