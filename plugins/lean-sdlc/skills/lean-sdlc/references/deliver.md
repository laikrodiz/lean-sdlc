# Deliver

Use Deliver only when cause, scope, architecture, owned `In Progress` task, visible Plan, acceptance, and proof are settled.

See [subagents.md](subagents.md) for child triggers and checkpoints.

1. Read task, context, acceptance, proof, code. Confirm plan matches one task or pair.
3. Run the structural check before the first non-control write.
4. Build the smallest cohesive units through narrow contracts and a readable orchestrator.
5. Classify boundary cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`.
6. After implementation, the Architect reviews scope, architecture, contract alignment before Verify.
7. Quick Fix: review diff and run narrow proof before close. No child per fix; shared batches may use Verifier under its normal trigger.
8. Apply the checkpoint barrier; send the final source checkpoint to Verify.
9. Apply [operations.md](operations.md).
