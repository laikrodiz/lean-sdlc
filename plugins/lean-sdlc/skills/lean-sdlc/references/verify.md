# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Apply the mandatory Verifier trigger and explicit profile from [subagents.md](subagents.md). The Sol `medium` or `high` lead makes the final close, fail, reopen, or truth-resolution decision.

1. Read the active task, owner, dependencies, acceptance, proof, parent truth, and checkpoint identity.
2. Compare the delivered behavior with every acceptance point.
3. Have the Verifier apply its canonical checkpoint contract to the promised checks against that exact checkpoint. Run checks locally in Solo mode.
4. For artifact or operational work, have the Operator apply its canonical operation contract.
5. Inspect the diff for unrelated change, stale documentation, oversized units, pass-through modules, speculative seams, and boundaries that always change together.
6. Check change locality: a meaningful unit can be tested or replaced through its contract without unrelated repository surgery.
7. Confirm every material changed-boundary edge case has an explicit disposition and that accepted behavior has proof.
8. When documentation includes diagrams, confirm the Mermaid view is small, readable, useful, and consistent with repository truth.
9. Trace changed behavior or durable choices back to `docs/PROJECT.md` and any optional owning document.
10. Resolve contradictions in the authoritative source, then synchronize only affected representations.
11. Keep the task open when acceptance, evidence, diagnostics, dependencies, or parity is incomplete.
12. Run the structural checker.
13. Let the owning lead alone decide task disposition and close through `tasks.py close` with concise evidence. Use a recorded direct-user override only when the user explicitly requests it.

Any source change after the verified checkpoint invalidates its prior result.

Done means repository truth agrees with reality and completion rests on reproducible evidence.
