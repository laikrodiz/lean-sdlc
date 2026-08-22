# Verify

See [subagents.md](subagents.md) for Verifier trigger.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

## Proof layers

- Targeted proof is the smallest changed-behavior check. Engineer owns the targeted command after a coherent implementation checkpoint and after a permitted correction.
- Acceptance proof checks observable completion. Without independent verification, Architect decides acceptance from existing evidence and runs only a missing acceptance command. With independent verification, Verifier owns acceptance and regression commands.
- Regression proof checks affected-boundary risk, including sibling callers or shared interfaces. Verifier runs one regression command when independent proof is required.
- Each expensive proof command has one owner per checkpoint. No owner reruns an identical command unless independent proof, disputed evidence, or repository policy requires it.

1. Read task, acceptance, proof, selected authoritative contracts, focused patches, and exact evidence. Route broad or cross-boundary source, logs, inventories, and raw output to Scout. Do not require complete broad source reads. Require exact proof or a recorded procedure.
2. For one settled task, Engineer proof plus final Architect review suffices without an independent-proof trigger.
3. Select one optional nested Verifier for one qualifying task. Combined, parallel, release, or final-batch checkpoints use one Architect-started Verifier after writers stop.
4. At verification start, Verifier runs `python3 "<skill-root>/scripts/checkpoint.py" --repo "<repo-root>" PATH [PATH ...]` over explicit task-owned paths and retains the SHA-256 value locally.
5. Verifier is read-only. It never changes tracked source, configuration, documentation, ledger, or state. It may create named temporary or incidental test outputs outside tracked truth. It independently runs acceptance proof for observable completion and one regression command for affected-boundary risk; skip Engineer-only targeted checks. Do not repeat an identical targeted command unless independent proof, disputed evidence, or repository policy requires it.
6. Run the command again over the same explicit task-owned paths. Compare the SHA-256 values locally and block if they differ. Do not persist values, expose full values in routine reports, or make Architect calculate them.
7. Compare acceptance, semantic interaction, documentation parity, and change locality.
8. Run the full suite once under Verifier only for a release, broad shared contracts, migrations or build graphs, an explicit repository requirement, or when no trustworthy selector exists. Trace behavior to owning docs and run the structural checker.
9. Owning lead decides disposition. Close the accepted task through `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" close` with evidence. Direct-user override requires explicit request and recorded reason.
10. Treat task proof as the acceptance anchor. Retain required acceptance, regression, structure, and documentation layers.
11. Stop after all required proof passes. Add an always-on rule only for an observed failure. Use the smallest behavioral evaluation that fails before the rule and passes after it.

For documentation, verify its trigger, semantic unit, links, and `INDEX.md` navigation. Keep `docs/PROJECT.md` as the only mandatory shared project document. If `/archive` exists, verify user authority and inertness in imports, builds, packaging, and normal tests.

Standard final checkpoint reviews pending Quick Fixes through highest listed task in Verifier regression and documentation/interaction review. Close with `--review-through TASK-NNN` only when prefix is `Done`; failed review creates Standard correction task.
