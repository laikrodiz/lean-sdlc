# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Apply the mandatory Verifier trigger and profile from [subagents.md](subagents.md). The user-selected lead makes the final accept, correct, continue, close, fail, reopen, or truth-resolution decision. Solo mode follows the same contracts locally.

1. Read the active task, owner, dependencies, acceptance, proof, context, and exact checkpoint. Resolve shorthand tool names before delegation.
2. Require exact proof commands or a recorded procedure.
3. Have the lead inspect architecture, invariant, interface, path, scope, and contract alignment.
4. Compare delivered behavior with every acceptance point.
5. Reuse or start Verifier for acceptance-defining proof. Verifier independently reruns it, adds risk-based regression, and skips Engineer-only targeted checks.
6. Run the full suite once under Verifier unless evidence conflicts. Consume Maintainer evidence instead of repeating the operation.
7. Inspect the diff for unrelated change, stale documentation, oversized tasks, pass-through modules, speculative seams, and boundaries that always change together.
8. Check change locality and give every plausible changed-boundary edge case an explicit disposition.
9. When documentation includes diagrams, confirm the Mermaid view is small, readable, useful, and consistent with repository truth.
10. Trace changed behavior and durable choices to `docs/PROJECT.md` and their owning documents. Run the structural checker.
11. Let the owning lead alone decide task disposition and close through `tasks.py close` with concise evidence. A direct-user override requires an explicit request and recorded reason.

Any source change after the verified checkpoint invalidates its prior result. Done means repository truth agrees with reality and completion rests on reproducible evidence.
