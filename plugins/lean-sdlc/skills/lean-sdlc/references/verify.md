# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Apply the mandatory Verifier trigger and explicit profile from [subagents.md](subagents.md). The user-selected lead makes the final accept, correct, continue, close, fail, reopen, or truth-resolution decision.

1. Read the active task, owner, dependencies, acceptance, proof, context document, and checkpoint identity.
2. Require exact proof commands or a recorded procedure. Resolve shorthand tool names before delegation.
3. Have the lead inspect the delivered task checkpoint for architecture, invariant, interface, path, and scope compliance.
4. Compare the delivered behavior with every acceptance point.
5. Reuse the existing Verifier role thread, or spawn it lazily. Have Verifier independently rerun acceptance-defining proof against the exact checkpoint and add risk-based regression.
6. Have the Verifier skip Engineer-only targeted checks. Run the full suite once under Verifier unless evidence conflicts.
7. Have the Maintainer apply its canonical operation contract for artifact or operational work.
8. Have the Verifier consume Maintainer evidence instead of repeating the operation.
9. Have the lead avoid repeating child commands except in Solo mode or to resolve conflicting evidence.
10. Inspect the diff for unrelated change, stale documentation, oversized tasks, pass-through modules, speculative seams, and boundaries that always change together.
11. Check change locality: a meaningful task can be tested or replaced through its contract without unrelated repository surgery.
12. Confirm every material changed-boundary edge case has an explicit disposition and that accepted behavior has proof.
13. When documentation includes diagrams, confirm the Mermaid view is small, readable, useful, and consistent with repository truth.
14. Trace changed behavior or durable choices back to `docs/PROJECT.md` and any optional owning document.
15. Resolve contradictions in the authoritative source, then synchronize only affected representations.
16. Keep the task open when acceptance, evidence, diagnostics, dependencies, or parity is incomplete.
17. Run the structural checker.
18. Let the owning lead alone decide task disposition and close through `tasks.py close` with concise evidence. Use a recorded direct-user override only when the user explicitly requests it.

Any source change after the verified checkpoint invalidates its prior result.

Done means repository truth agrees with reality and completion rests on reproducible evidence.
