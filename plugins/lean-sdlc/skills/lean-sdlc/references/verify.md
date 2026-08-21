# Verify

See [subagents.md](subagents.md) for Verifier trigger. Resolve shorthand tool names before delegation.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

1. Read task, acceptance, proof, selected authoritative contracts, focused patches, and exact evidence completely. Route broad or cross-boundary source, logs, inventories, and raw output to Scout. Do not require complete broad source reads. Require exact proof or a recorded procedure.
2. For one settled task, Engineer proof plus final Architect review suffices without an independent-proof trigger.
3. Select one optional nested Verifier for a qualifying single task. Combined, parallel, release, or final-batch checkpoints use one Architect-started Verifier after writers stop.
4. When verification begins, Verifier independently computes a candidate checkpoint fingerprint and retains it locally.
5. Verifier independently runs acceptance-defining proof and one planned regression command; skip Engineer-only targeted checks. Never duplicate evidence unless repository policy requires it.
6. Recompute the fingerprint before return. Block if it changed. Do not persist fingerprints or make Architect calculate them.
7. Compare acceptance, semantic interaction, documentation parity, and change locality.
8. Run the full suite once under Verifier only when the task or repository contract requires it. Trace behavior to owning docs and run the structural checker.
9. The owning lead alone decides task disposition. Close the accepted task through `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" close` with evidence. A direct-user override requires an explicit request and recorded reason.
10. Treat task proof as the acceptance anchor. Retain required acceptance, regression, structure, and documentation layers.
11. Stop after all required proof passes. Add an always-on rule only for an observed failure. Use the smallest behavioral evaluation that fails before the rule and passes after it.

For documentation work, verify the concrete trigger, one semantic unit, current links, and `INDEX.md` navigation. Verify that `docs/PROJECT.md` remains the only mandatory shared project document. If `/archive` exists, verify explicit user authority and inertness from imports, builds, packaging, and normal tests.

Standard final checkpoint reviews pending Quick Fixes through highest listed task in Verifier regression and documentation/interaction review. Close with `--review-through TASK-NNN` only when prefix is `Done`; failed review creates Standard correction task.
