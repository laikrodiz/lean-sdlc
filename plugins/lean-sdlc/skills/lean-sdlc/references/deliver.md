# Deliver

Use Deliver only when cause, scope, architecture, owned `In Progress` task, visible Plan, acceptance, and proof are settled.

See [subagents.md](subagents.md) for child triggers and checkpoints.

1. Read task, acceptance, proof, and source material completely. Group read-only discovery into bounded calls. Use follow-ups only for unresolved questions.
2. Run the structural check before the first non-control write.
3. Build the smallest cohesive units through narrow contracts and a readable orchestrator.
4. Classify boundary cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`.
5. After implementation, the Architect reviews scope, architecture, contract alignment before Verify.
6. Quick Fix: review diff and run narrow proof before close. No child per fix; shared batches may use Verifier under its normal trigger.
7. Apply the checkpoint barrier; send the final source checkpoint to Verify.
8. Apply [operations.md](operations.md).
