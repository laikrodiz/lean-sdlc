# Verify

This file owns proof selection, reuse, checkpoints, and closeout. Child allocation stays in [subagents.md](subagents.md).

## Plan proof once

Task proof is the acceptance anchor. Record command owner, proof purpose, and invalidation inputs in the existing task or handoff. Do not create a proof registry.

- Targeted proof checks changed behavior; the Engineer normally owns it.
- Acceptance proof checks observable completion against the task.
- Regression proof checks affected-boundary risk, including sibling callers and shared interfaces.

These are purposes, not three mandatory commands. One command may satisfy multiple proof purposes. Independent review checks the conclusion and supporting evidence; it does not automatically repeat execution.

For one settled low-risk task, Engineer evidence and final Architect review suffice. Use an independent Verifier for architecture-sensitive or cross-boundary behavior, disputed evidence, combined parallel work, releases, or required repository checks. The same trigger applies when the Architect implements directly.

Reuse proof only while relevant source, dependencies, configuration, environment, toolchain, and target inputs remain valid. Record these inputs at the useful boundary, not the entire repository by default. Repeat affected checks after relevant changes, disputed evidence, or a specific need for independent reproduction. A changed dependency invalidates proof even if task-owned files have not changed.

If a planned full gate contains the focused checks, run that gate without a duplicate preliminary suite. Earlier targeted feedback remains useful when it prevents further work on a defect. Run the full suite once for a release, broad shared contracts, migrations, build-graph changes, explicit repository requirements, or when no trustworthy selector exists. Otherwise use relevant checks.

## Check a stable boundary

1. Read acceptance, selected authoritative contracts, focused changes, and exact prior evidence. Use Scout for unresolved broad evidence, not a second complete source review.
2. Identify complete verification inputs and mutable test resources. Stop writers touching them, including dependencies. Unrelated stable-boundary work may continue. Final release checks cover every release input.
3. Verifier runs `python3 "<skill-root>/scripts/checkpoint.py" --repo "<repo-root>" PATH [PATH ...]` over explicit source and configuration inputs before and after proof. Compare returned SHA-256 values locally. Block on mismatch. Hash equality detects file changes; it does not prove unchanged environment, toolchain, or external state. Check those separately when relevant.
4. Independently assess acceptance, semantic interaction, assigned-path separation, documentation parity, and affected-boundary risks. Run only missing or invalidated checks. Batch common regression across atomic tasks without merging their acceptance decisions.
5. Collect independent safe failures together. Skip checks whose prerequisite failed. Return actionable findings in one report. A preauthorized Engineer may correct local defects and return only changed evidence; material decisions go to Architect.
6. Stop after all required proof passes. Keep exact failed logs available by path; omit successful raw logs and full fingerprints from routine reports. Do not persist checkpoint hashes or make the Architect calculate them.

Verifier does not edit tracked source, configuration, documents, ledger, or session state. Incidental test outputs must respect assigned resources and remain outside tracked truth. A standard release command may include structural checks; do not run the same structural check again separately.

## Close once

The Architect reviews contract-sensitive changes and gives one visible alignment signoff. Shared documentation may be synchronized once per completed batch. Each task must satisfy its own acceptance before `Done`; pending required shared proof prevents closure.

For changed documents, verify triggers, semantic units, links, and `INDEX.md` navigation. `docs/PROJECT.md` remains the only mandatory shared project document. If `/archive` exists, check user authority and inertness in imports, builds, packaging, and normal tests.

Review pending Quick Fixes during the next Standard or final batch checkpoint. Use `--review-through TASK-NNN` only after that review and when the prefix is `Done`. Failed review creates a Standard correction task.

Only the owning Architect closes through `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" close` with evidence. Direct-user override requires an explicit request and recorded reason. Follow [operations.md](operations.md) for required delivery evidence before claiming the complete outcome.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording. Replace slots with project facts and omit slot labels. Add a permanent rule only for an observed failure, with the smallest useful check that catches it.
