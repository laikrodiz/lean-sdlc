# Deliver

Use Deliver only when cause and scope are known and an owned `In Progress` task has measurable acceptance and proof.

Use Terra `high` for general implementation. Use Luna `xhigh` for narrow mechanical changes with exact boundaries and strong automated proof. Use Sol `high` or `xhigh` when implementation itself carries major decision or failure risk.

1. Read the active task, parent truth, acceptance, proof, and affected code.
2. Run the structural before-write check.
3. Declare the files or boundaries the change may touch.
4. Implement the smallest approved slice.
5. Keep affected tests, diagnostics, project truth, decisions, and technical documentation in sync.
6. Avoid opportunistic refactors and speculative compatibility.
7. Stop and return to Shape, Decide, or Diagnose when implementation exposes missing truth.
8. At a coherent checkpoint, ask the Verifier sidecar to run the narrow affected checks.
9. Use the Operator sidecar for build, package, deploy, flash, runtime, or smoke procedures under [operations.md](operations.md).
10. Hand the checkpoint and compact evidence to Verify.

Documentation-only delivery follows the same task and proof gates. Synchronize settled truth; do not make new product or architecture decisions while cleaning documents.

Ready means the approved slice is small, coherent, testable, diagnosable, and prepared for independent verification.
