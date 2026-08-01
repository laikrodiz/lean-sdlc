# Deliver

Use Deliver only when the user has given explicit implementation authority, the intent and visible-plan gates in [Plan](plan.md) are complete, the cause and scope are known, and an owned `In Progress` task matches one durable plan item with measurable acceptance and proof.

Discussion or proposal requests remain read-only. If implementation authority is ambiguous, return to the user before Plan or Deliver.

The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, acceptance, durable task, and checkpoint boundaries. Engineer receives the settled decision envelope and may choose only local implementation mechanics inside it. Without an explicit profile, use Sol `high`; raise it for consequential choices. Execute or delegate only through [subagents.md](subagents.md). User-facing assignments, architecture briefs, progress updates, and sign-offs use natural prose. Internal handoffs and compact returns remain labeled and lossless.

1. Read the active task, context document, acceptance, proof, and affected code.
2. Confirm the lead's visible plan and the task's exact matching durable item from [Plan](plan.md).
3. Run the structural before-write check.
4. Declare the files or boundaries the change may touch.
5. For nontrivial logic, identify coherent transformations and real state, I/O, or failure boundaries. Compose the smallest independently testable units through narrow inputs and outputs, with a readable orchestrator.
6. Keep direct code when extraction would create pass-through pieces. Avoid speculative interfaces, factories, configuration, and future-proofing.
7. Scan plausible changed-boundary cases: missing, empty, malformed, limit values, dependency failure or partial result, interruption, repetition or concurrency, and required invariants.
8. Classify each relevant case as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Follow existing contracts for routine cases; return to Shape or Decide before choosing user-visible, compatibility, safety, or data behavior.
9. Keep one durable task with one outcome, settled architecture and invariants, related allowed paths, explicit acceptance, proof, and stop conditions.
10. Before the Engineer handoff, give the concise natural architecture brief required by [subagents.md](subagents.md). Apply the Engineer trigger only after the visible plan exists and the task matches it. In Assisted mode, delegate one ready durable task beyond the direct fast path to the existing Engineer role thread; otherwise spawn it lazily or execute locally.
11. Keep affected tests, diagnostics, project truth, decisions, and technical documentation in sync.
12. Avoid opportunistic refactors and speculative compatibility.
13. Stop and return to Shape, Decide, or Diagnose when implementation exposes missing truth.
14. After Engineer returns one task checkpoint, inspect its diff and contract alignment, then give the concise natural lead sign-off required by [subagents.md](subagents.md).
15. Accept the checkpoint only after sign-off, or send a concise correction delta to the same Engineer before defining another task.
16. For build, package, deploy, flash, runtime, or smoke work, apply the Maintainer trigger and procedure rules in [operations.md](operations.md).
17. Hand the accepted checkpoint and compact evidence to Verify.

Documentation-only delivery follows the same task and proof gates. Synchronize settled truth; do not make new product or architecture decisions while cleaning documents.

Ready means implementation authority, the visible plan, and the approved slice are small, coherent, testable, diagnosable, and prepared for independent verification.
