# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Apply the mandatory Verifier trigger and explicit profile from [subagents.md](subagents.md). The user-selected lead makes the final accept, correct, continue, close, fail, reopen, or truth-resolution decision.

1. Read the active task, owner, dependencies, acceptance, proof, parent truth, and checkpoint identity.
2. Have the lead inspect the delivered task checkpoint for architecture, invariant, interface, path, and scope compliance.
3. Compare the delivered behavior with every acceptance point.
4. Reuse the existing `verifier` thread, or spawn it lazily. Have Verifier independently rerun acceptance-defining proof against the exact checkpoint and add risk-based regression.
5. Have the Verifier skip Executor-only targeted checks. Run the full suite once under Verifier unless evidence conflicts.
6. Have the Operator apply its canonical operation contract for artifact or operational work.
7. Have the Verifier consume Operator evidence instead of repeating the operation.
8. Have the lead avoid repeating child commands except in Solo mode or to resolve conflicting evidence.
9. Inspect the diff for unrelated change, stale documentation, oversized tasks, pass-through modules, speculative seams, and boundaries that always change together.
10. Check change locality: a meaningful task can be tested or replaced through its contract without unrelated repository surgery.
11. Confirm every material changed-boundary edge case has an explicit disposition and that accepted behavior has proof.
12. When documentation includes diagrams, confirm the Mermaid view is small, readable, useful, and consistent with repository truth.
13. Trace changed behavior or durable choices back to `docs/PROJECT.md` and any optional owning document.
14. Resolve contradictions in the authoritative source, then synchronize only affected representations.
15. Keep the task open when acceptance, evidence, diagnostics, dependencies, or parity is incomplete.
16. Run the structural checker.
17. Let the owning lead alone decide task disposition and close through `tasks.py close` with concise evidence. Use a recorded direct-user override only when the user explicitly requests it.

Any source change after the verified checkpoint invalidates its prior result.

Done means repository truth agrees with reality and completion rests on reproducible evidence.
