# Verify

Use Verify when completion is claimed, sources disagree, traceability is uncertain, or a task may close.

Apply the mandatory Verifier trigger and profile from [subagents.md](subagents.md). The Architect makes the final task decision.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

1. Read active task, or both qualified-pair tasks, with owners, dependencies, acceptance, proof, context, and exact checkpoint. Resolve shorthand tool names before delegation.
2. Require exact proof commands or a recorded procedure.
3. Architect inspects architecture, invariants, interfaces, paths, scope, and contract alignment.
4. Compare behavior with acceptance points. Check assigned-path separation, semantic interaction, and documentation parity for paired work.
5. Reuse or start Verifier for independent, acceptance-defining proof and one planned regression command. The Verifier skips Engineer-only targeted checks.
6. Run the full suite once under Verifier only when the task or repository contract requires it. Consume Maintainer evidence instead of repeating the operation.
7. Inspect the diff for unrelated change, stale docs, oversized tasks, pass-through modules, speculative seams, and coupled boundaries. Check change locality and give each boundary edge case a disposition.
8. Trace changed behavior and durable choices to `docs/PROJECT.md` and owning documents. Run structural checker.
9. Let the owning lead alone decide task disposition and close the accepted task through `tasks.py close` with evidence. A direct-user override requires an explicit request and recorded reason.
