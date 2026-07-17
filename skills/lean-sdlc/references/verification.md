# Verification Workflow

Use whenever implementation claims completion or a task may move to `done`.

Use Luna at `low` to run checks and collect evidence, Terra at `high` to interpret failures or edge cases, and Sol at `medium` or `high` for the final close, fail, or reopen decision.

## Workflow

1. Read the active task, owner, proof, and linked feature, decision, or maintenance parent.
2. Compare implemented behavior with every acceptance point.
3. Run promised tests, smoke paths, or alternative proof.
4. Confirm promised diagnostics and failure signals exist and are useful.
5. Check that features, decisions, indexes, and technical docs match reality at the correct level.
6. Record concise evidence in the task ledger.
7. Run `scripts/lean_check.py --task TASK-ID` for structural integrity when standard files exist.
8. Keep the task open when acceptance, evidence, diagnostics, or parity is incomplete.
9. Let only the main agent move the task to `done` after all gates pass.
10. State the resulting status and evidence explicitly.

Route uncertain source-of-truth conflicts to traceability. Route settled mechanical cleanup to documentation maintenance before closeout.

Success means completion rests on evidence and repository truth agrees with implemented reality.
