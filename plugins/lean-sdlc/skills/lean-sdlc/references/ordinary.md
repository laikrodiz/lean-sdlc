# One ordinary fix

Use the startup repository, helpers, owner and tier. Only the Lead writes. Stay inside the user's edit authority; commit, push, install and deploy require separate permission.
Check the project guide for an existing promise. Follow its pointer to the affected code. Inspect callers and fix the cause, not the symptom.
If there is more than one outcome, unclear ownership, a failed gate, a saved-data or interface change, or a need for independent proof, read the full Lead, common, planning and ledger protocols before editing. For an out-of-scope refactor, pause and propose the smallest option. For a direction change or cancellation, stop affected work and confirm processes stopped.
For known contract drift, follow the upgrade rules in ledger.md first. Never auto-repair an unknown block.
Use startup values for the quoted placeholders. Run `overview` once to exclude duplicates. For a new eligible fix:

```sh
python3 "<tasks-helper>" --repo "<repo-root>" start --check --owner "<owner>" --title "<outcome>" --context "Quick Fix" --acceptance "<done when>" --proof "<planned check>"
```

Honor dependencies. Confirm the returned In Progress row and passed gate before editing. A pre-claim reproduction must create no files, including caches.
Make the smallest complete change. Preserve unrelated work. Run focused regression checks. Inspect the result, artifact and required usage notes. Missing essential or safety proof blocks closure. A restored, already documented promise needs no new document.
Only a settled, reversible Simple fix with passing immediate proof may use Quick Fix and defer broader review. Use the exact Quick Fix context and mark the evidence “pending review” and clear it with Verifier at the next shared checkpoint and before release. Otherwise complete required review now.
After inspecting passing evidence, run this command alone with the returned ID:

```sh
python3 "<tasks-helper>" --repo "<repo-root>" close "<task-id>" --owner "<owner>" --evidence "<observed result and limits>"
```

Confirm success. In one short handoff state the result, what actually passed, and any pending review. No table for a single fix.
