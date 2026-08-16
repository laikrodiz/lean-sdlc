# Verify

See [subagents.md](subagents.md) for Verifier trigger. Resolve shorthand tool names before delegation.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording; replace slots with project facts and omit slot labels.

1. Read active task/checkpoint with acceptance and proof. Require exact proof or a recorded procedure.
2. Compare acceptance, semantic interaction, and documentation parity.
3. Reuse or start Verifier for independent acceptance-defining proof and one planned regression command. The Verifier skips Engineer-only targeted checks.
4. Run the full suite once under Verifier only when the task or repository contract requires it. Check change locality.
5. Trace behavior to owning docs; run structural checker.
6. The owning lead alone decide task disposition and close the accepted task through `tasks.py close` with evidence. A direct-user override requires an explicit request and recorded reason.

Standard final checkpoint reviews pending Quick Fixes through highest listed task in Verifier regression and documentation/interaction review. Close with `--review-through TASK-NNN` only when prefix is `Done`; failed review creates Standard correction task.
