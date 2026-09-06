# Deliver

Use Deliver only when cause, scope, architecture, owned `In Progress` task, visible Plan, acceptance, and proof are settled.

See [subagents.md](subagents.md) for child triggers and checkpoints.

1. Read task, acceptance, proof, selected authoritative contracts, focused patches, and exact evidence completely. Route broad or cross-boundary source, logs, inventories, and raw output to Scout. Do not require complete broad source reads.
2. Run the structural check before the first non-control write.
3. Build the smallest cohesive units through narrow contracts and a readable orchestrator.
4. Confirm the one-time `Routine` or `Critical` classification for each independently accepted task or plan piece. Classify boundary cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. Risk classification informs proof and sequencing; it does not determine ownership.
5. Engineer shows visible restatement. After the final Engineer return, Architect reviews scope, architecture, contract alignment in one short visible alignment signoff. Review earlier only for decision, blocker, collision, scope change, or proof mismatch.
6. Quick Fix: review diff and run narrow proof before close. No child per fix; shared batches may use Verifier under its normal trigger.
7. Stop writers touching the checkpoint inputs or resources; unrelated stable-boundary work may continue. Apply [verify.md](verify.md) before acceptance. Critical acceptance requires independent verification, including Architect-written work. Follow its Solo missing-proof gate.
8. Apply [operations.md](operations.md).
