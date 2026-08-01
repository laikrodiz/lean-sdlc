# Deliver

Use Deliver only when explicit implementation authority, the visible Plan gate, known cause and scope, an owned `In Progress` task, measurable acceptance, and proof are ready.

Discussion and proposal requests remain read-only. If authority is ambiguous, return to the user before Plan or Deliver.

The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, acceptance, the durable task, and checkpoint boundaries. Engineer receives one settled decision envelope and chooses only local mechanics. Use [subagents.md](subagents.md) for delegation, profiles, handoffs, and reporting. User-facing assignments, architecture briefs, progress updates, and sign-offs use natural prose; internal handoffs remain labeled and lossless.

1. Read the active task, or both active tasks in a qualified parallel group, with context, acceptance, proof, and affected code.
2. Confirm the visible plan matches one durable task normally, or both tasks in a qualified parallel group.
3. Run the structural before-write check and declare allowed paths.
4. Build the smallest cohesive units through narrow contracts and a readable orchestrator. Keep direct code when extraction creates pass-through pieces.
5. Scan plausible boundary cases and classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior.
6. Keep one durable task normally with one outcome, settled architecture and invariants, related paths, acceptance, proof, and stop conditions. A qualified group keeps two independently accepted tasks under one Architect owner, with exactly one task per Engineer.
7. In Assisted mode, delegate one ready implementation task beyond the direct fast path. Route a documentation-only task directly to Maintainer. Lazily reuse a second Engineer only for a qualified parallel group.
8. Keep Engineer code-local truth current. After Engineers stop, Architect reviews the combined implementation.
9. Maintainer synchronizes affected shared narrative documents after Architect review and before the final checkpoint. When two writers return, send one correction delta if needed.
10. Send the final source checkpoint to Verify first. Then apply [operations.md](operations.md) for required operations and consume Maintainer evidence without repeating accepted source proof.
Documentation-only delivery follows the same task and proof gates. Do not make new product or architecture decisions while cleaning documents.
