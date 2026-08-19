# Verify

See [subagents.md](subagents.md) for Verifier trigger. Resolve shorthand tool names before delegation.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

1. Read the active task and source boundary with acceptance and proof. Require exact proof or a recorded procedure.
2. When verification begins, Verifier independently computes a candidate checkpoint fingerprint and retains it locally.
3. Reuse or start Verifier for independent acceptance-defining proof and one planned regression command. Verifier skips Engineer-only targeted checks.
4. Recompute the fingerprint before return. Block if it changed. Do not persist fingerprints or make Architect calculate them.
5. Compare acceptance, semantic interaction, documentation parity, and change locality.
6. Run the full suite once under Verifier only when the task or repository contract requires it. Trace behavior to owning docs and run the structural checker.
7. The owning lead alone decides task disposition. Close the accepted task through `tasks.py close` with evidence. A direct-user override requires an explicit request and recorded reason.

For documentation work, verify the concrete trigger, one semantic unit, current links, and `INDEX.md` navigation. Verify that `docs/PROJECT.md` remains the only mandatory shared project document. If `/archive` exists, verify explicit user authority and inertness from imports, builds, packaging, and normal tests.

Standard final checkpoint reviews pending Quick Fixes through highest listed task in Verifier regression and documentation/interaction review. Close with `--review-through TASK-NNN` only when prefix is `Done`; failed review creates Standard correction task.
