# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Use Luna `xhigh` or Terra `high` to execute and summarize checks. Use Sol `medium` or `high` for the final close, fail, reopen, or truth-resolution decision.

1. Read the active task, owner, dependencies, acceptance, proof, parent truth, and checkpoint identity.
2. Compare the delivered behavior with every acceptance point.
3. Have the Verifier run the promised checks against that exact checkpoint; run them locally in Solo mode.
4. For artifact or operational work, have the Operator confirm artifact identity, target, result, and smoke signal.
5. Inspect the diff for unrelated change and stale documentation.
6. Trace changed behavior or durable choices back to `docs/PROJECT.md` and any optional owning document.
7. Resolve contradictions in the authoritative source, then synchronize only affected representations.
8. Keep the task open when acceptance, evidence, diagnostics, dependencies, or parity is incomplete.
9. Run the structural checker.
10. Let the owning lead close through `tasks.py close` with concise evidence. Use a recorded direct-user override only when the user explicitly requests it.

Any source change after the verified checkpoint invalidates its prior result.

Done means repository truth agrees with reality and completion rests on reproducible evidence.
