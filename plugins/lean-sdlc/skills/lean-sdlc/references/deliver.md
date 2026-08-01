# Deliver

Use Deliver only when explicit implementation authority, the visible Plan gate, known cause and scope, an owned `In Progress` task, measurable acceptance, and proof are ready.

Discussion and proposal requests remain read-only. If authority is ambiguous, return to the user before Plan or Deliver.

The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, acceptance, the durable task, and checkpoint boundaries. Use [subagents.md](subagents.md) for child triggers, scheduling, profiles, handoffs, checkpoints, and reporting. User-facing assignments, architecture briefs, progress updates, and sign-offs use natural prose.

1. Read the active task, or both active tasks in a qualified pair, with context, acceptance, proof, and affected code.
2. Confirm the visible plan matches one durable task, or both tasks in a qualified pair.
3. Run the structural before-write check and declare allowed paths.
4. Build the smallest cohesive units through narrow contracts and a readable orchestrator. Keep direct code when extraction creates pass-through pieces.
5. Scan plausible boundary cases and classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior.
6. Keep one durable task with one outcome, settled architecture and invariants, related paths, acceptance, proof, and stop conditions.
7. Use the policy checkpoint barrier after implementation. Send its final source checkpoint to Verify first.
8. Apply [operations.md](operations.md) for required operations and consume Maintainer evidence without repeating accepted source proof.
Documentation-only delivery follows the same task and proof gates. Do not make new product or architecture decisions while cleaning documents.
