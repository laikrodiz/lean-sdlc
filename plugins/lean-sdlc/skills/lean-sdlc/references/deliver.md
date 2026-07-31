# Deliver

Use Deliver only when cause and scope are known and an owned `In Progress` task has measurable acceptance and proof.

Use Terra `high` for general implementation. Use Sol `high` or `xhigh` when implementation itself carries major decision or failure risk. Delegate only through the profiles and eligibility rules in [subagents.md](subagents.md).

1. Read the active task, parent truth, acceptance, proof, and affected code.
2. Run the structural before-write check.
3. Declare the files or boundaries the change may touch.
4. For nontrivial logic, identify coherent transformations and real state, I/O, or failure boundaries. Compose the smallest independently testable units through narrow inputs and outputs, with a readable orchestrator.
5. Keep direct code when extraction would create pass-through pieces. Avoid speculative interfaces, factories, configuration, and future-proofing.
6. Scan plausible changed-boundary cases: missing, empty, malformed, limit values, dependency failure or partial result, interruption, repetition or concurrency, and required invariants.
7. Classify each relevant case as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Follow existing contracts for routine cases; return to Shape or Decide before choosing user-visible, compatibility, safety, or data behavior.
8. Implement the smallest approved slice.
9. Keep affected tests, diagnostics, project truth, decisions, and technical documentation in sync.
10. Avoid opportunistic refactors and speculative compatibility.
11. Stop and return to Shape, Decide, or Diagnose when implementation exposes missing truth.
12. At each coherent checkpoint, apply the Verifier trigger in [subagents.md](subagents.md).
13. For build, package, deploy, flash, runtime, or smoke work, apply the Operator trigger in [subagents.md](subagents.md) and procedure rules in [operations.md](operations.md).
14. Hand the checkpoint and compact evidence to Verify.

Documentation-only delivery follows the same task and proof gates. Synchronize settled truth; do not make new product or architecture decisions while cleaning documents.

Ready means the approved slice is small, coherent, testable, diagnosable, and prepared for independent verification.
