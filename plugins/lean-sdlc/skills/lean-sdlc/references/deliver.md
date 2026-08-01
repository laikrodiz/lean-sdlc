# Deliver

Use Deliver only when explicit implementation authority, the visible Plan gate, known cause and scope, an owned `In Progress` task, measurable acceptance, and proof are ready.

Discussion and proposal requests remain read-only. If authority is ambiguous, return to the user before Plan or Deliver.

The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, acceptance, the durable task, and checkpoint boundaries. Engineer receives one settled decision envelope and chooses only local mechanics. Use [subagents.md](subagents.md) for delegation, profiles, handoffs, and reporting. User-facing assignments, architecture briefs, progress updates, and sign-offs use natural prose; internal handoffs remain labeled and lossless.

1. Read the active task, context, acceptance, proof, and affected code.
2. Confirm the visible plan matches one durable task.
3. Run the structural before-write check and declare allowed paths.
4. Build the smallest cohesive units through narrow contracts and a readable orchestrator. Keep direct code when extraction creates pass-through pieces.
5. Scan plausible boundary cases and classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior.
6. Keep one durable task with one outcome, settled architecture and invariants, related paths, acceptance, proof, and stop conditions.
7. In Assisted mode, delegate one ready durable task beyond the direct fast path to the reusable Engineer role. Execute locally when the fast path applies.
8. Keep tests, diagnostics, project truth, decisions, and technical documentation synchronized. Avoid opportunistic refactors and speculative compatibility.
9. After Engineer returns one task checkpoint, inspect scope, diff, and contract alignment. Accept it or send a concise correction delta to the same Engineer.
10. Apply [operations.md](operations.md) for build, package, deploy, flash, runtime, or smoke work. Send the accepted checkpoint and evidence to Verify.
Documentation-only delivery follows the same task and proof gates. Do not make new product or architecture decisions while cleaning documents.
