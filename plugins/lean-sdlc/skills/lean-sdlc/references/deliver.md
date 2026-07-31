# Deliver

Use Deliver only when cause and scope are known and an owned `In Progress` task has measurable acceptance and proof.

The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, acceptance, durable task, and checkpoint boundaries. Executor receives the settled decision envelope and may choose only local implementation mechanics inside it. Without an explicit profile, use Sol `high`; raise it for consequential choices. Execute or delegate only through [subagents.md](subagents.md).

1. Read the active task, context document, acceptance, proof, and affected code.
2. Run the structural before-write check.
3. Declare the files or boundaries the change may touch.
4. For nontrivial logic, identify coherent transformations and real state, I/O, or failure boundaries. Compose the smallest independently testable units through narrow inputs and outputs, with a readable orchestrator.
5. Keep direct code when extraction would create pass-through pieces. Avoid speculative interfaces, factories, configuration, and future-proofing.
6. Scan plausible changed-boundary cases: missing, empty, malformed, limit values, dependency failure or partial result, interruption, repetition or concurrency, and required invariants.
7. Classify each relevant case as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Follow existing contracts for routine cases; return to Shape or Decide before choosing user-visible, compatibility, safety, or data behavior.
8. Define one durable task with one outcome, settled architecture and invariants, related allowed paths, explicit acceptance, proof, and stop conditions.
9. Before the Executor handoff, show the concise architecture brief required by [subagents.md](subagents.md). Apply the Executor trigger. In Assisted mode, delegate one ready durable task beyond the direct fast path to the existing `executor` thread; otherwise spawn it lazily or execute locally.
10. Keep affected tests, diagnostics, project truth, decisions, and technical documentation in sync.
11. Avoid opportunistic refactors and speculative compatibility.
12. Stop and return to Shape, Decide, or Diagnose when implementation exposes missing truth.
13. After Executor returns one task checkpoint, inspect its diff and contract alignment, then send the concise lead sign-off required by [subagents.md](subagents.md).
14. Accept the checkpoint only after sign-off, or send a concise correction delta to the same Executor before defining another task.
15. For build, package, deploy, flash, runtime, or smoke work, apply the Maintainer trigger and procedure rules in [operations.md](operations.md).
16. Hand the accepted checkpoint and compact evidence to Verify.

Documentation-only delivery follows the same task and proof gates. Synchronize settled truth; do not make new product or architecture decisions while cleaning documents.

Ready means the approved slice is small, coherent, testable, diagnosable, and prepared for independent verification.
