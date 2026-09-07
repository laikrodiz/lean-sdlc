# Verify

This file owns proof selection, reuse, checkpoints, and closeout. Child allocation stays in the selected mode reference.
Checkpoint inputs must stay inside the repository. Check external toolchain identity separately; do not pass interpreter or system paths to `checkpoint.py`.

## Plan proof once

The original request and accepted changes define acceptance. Compare them with task facts and delivered work; a task summary can omit requirements.
Record command owner, proof purpose, and invalidation inputs in the existing task or handoff. Do not create a proof registry.

- Targeted proof checks changed behavior; the implementation owner normally owns it.
- Acceptance proof checks observable completion against the task.
- Regression proof checks affected-boundary risk, including sibling callers and shared interfaces.

These are purposes, not three mandatory commands. One command may satisfy multiple proof purposes. Independent review checks the conclusion and supporting evidence; it does not automatically repeat execution.
The Lead can run early checks for useful implementation feedback. Do not schedule the same final gate separately for both roles.

For one settled Routine task, implementation-owner evidence and final Architect review suffice. Critical acceptance requires independent verification, including when the Architect writes the implementation. Use an independent Verifier for Critical, architecture-sensitive, or cross-boundary behavior, disputed evidence, combined parallel work, releases, or required repository checks.

In Solo, do not accept Critical work without independent evidence. Request authorization for a reviewer or a mode change. Do not spawn a reviewer automatically. Do not self-certify. Do not silently change mode.

Reuse proof only while relevant source, dependencies, configuration, environment, toolchain, and target inputs remain valid. Record these inputs at the useful boundary, not the entire repository by default. Repeat affected checks after relevant changes, disputed evidence, or a specific need for independent reproduction. A changed dependency invalidates proof even if task-owned files have not changed.

If a planned full gate contains the focused checks, run that gate without a duplicate preliminary suite. Earlier targeted feedback remains useful when it prevents further work on a defect. Run the full suite once for a release, broad shared contracts, migrations, build-graph changes, explicit repository requirements, or when no trustworthy selector exists. Otherwise use relevant checks.

## Check a stable boundary

1. Read the original request, accepted changes, task acceptance, selected contracts, actual changes, and exact prior evidence. Identify omitted requirements before judging proof.
2. Identify complete verification inputs and mutable test resources. Stop writers touching them, including dependencies. Unrelated stable-boundary work may continue. Final release checks cover every release input.
3. Verifier runs `python3 "<skill-root>/scripts/checkpoint.py" --repo "<repo-root>" PATH [PATH ...]` over explicit source and configuration inputs. Take one checkpoint before the first review read or check and one after all review and checks for that revision. Do not wrap each individual read or command in another checkpoint pair. Compare returned SHA-256 values locally and block on mismatch. A source correction starts a new review revision and invalidates affected proof. Hash equality detects file changes; it does not prove unchanged environment, toolchain, or external state. Check those separately when relevant.
4. Independently assess acceptance, semantic interaction, assigned-path separation, documentation parity, and affected-boundary risks. Run only missing or invalidated checks. Batch common regression across atomic tasks without merging their acceptance decisions.
For independent review, the Verifier inspects the contract, actual code, relevant failure cases, and test adequacy directly. It does not only endorse implementation-owner conclusions.
Check required literal text and examples in their requested location. A passing test that omits a requirement does not prove completion.
For runnable documentation, require successful evidence for the exact documented command in its stated environment. A substitute interpreter or argument needs a documented, verified alternative.
Each blocking finding must cite a requirement, safety invariant, or demonstrated regression. Separate optional hardening from required acceptance.
A type annotation alone does not specify an error contract. Confirm the authoritative requirement before demanding additional runtime rejection behavior.
Do not dismiss a demonstrated trust-boundary vulnerability as unsupported input. Keep concrete security failures blocking.
5. Collect independent safe failures together. Skip checks whose prerequisite failed. Return actionable findings in one report. In Delegating, a preauthorized Engineer may correct local defects and return only changed evidence. Material decisions go to Architect.
6. Stop after all required review and proof pass. Return the final result directly; passing statements need source paths, not another line-number inventory. Do not repeat reads or successful tests to prepare the completion response. Keep exact failed logs available by path; omit successful raw logs and full fingerprints from routine reports. Do not persist checkpoint hashes or make the Architect calculate them.

## Architect acceptance loop

The Architect reads actual changes and relevant surrounding code and callers. A summary alone is not sufficient.

Assess architecture, behavior, failure cases, test adequacy, unnecessary complexity, documentation, and integration. Reuse valid proof when its inputs still match.

- Accept when the contract and proof pass.
- Revise when concrete defects remain. Return each defect to the same assigned team with correction evidence.
- Redesign when the contract is flawed or a new requirement changes the outcome. Correct the contract before dependent work continues.

Batch independently identifiable findings. Give each finding a location, violated requirement or quality concern, and correction evidence. Distinguish a new requirement from a defect. The Architect does not patch delegated Routine work in Delegating. The Architect does not demand a workaround for its own flawed design.

Verifier does not edit tracked source, configuration, documents, ledger, or session state. Incidental test outputs must respect assigned resources and remain outside tracked truth. A standard release command may include structural checks; do not run the same structural check again separately.
Prevent incidental outputs where practical, or direct them to an assigned temporary location. Do not inspect or clean unrelated generated files.

## Close once

The Architect reviews contract-sensitive changes and gives one visible alignment signoff. Shared documentation may be synchronized once per completed batch. Each task must satisfy its own acceptance before `Done`; pending required shared proof prevents closure.

For changed documents, verify triggers, semantic units, links, and `INDEX.md` navigation. `docs/PROJECT.md` remains the only mandatory shared project document. If `/archive` exists, check user authority and inertness in imports, builds, packaging, and normal tests.

Review pending Quick Fixes during the next Standard or final batch checkpoint. Use `--review-through TASK-NNN` only after that review and when the prefix is `Done`. Failed review creates a Standard correction task.

Only the owning Architect closes through `python3 "<skill-root>/scripts/tasks.py" --repo "<repo-root>" close` with evidence. Direct-user override requires an explicit request and recorded reason. Follow [operations.md](operations.md) for required delivery evidence before claiming the complete outcome.

Checkpoint fact order: `<alignment> -> <checks> -> <deviation or risk> -> <next Architect action>`.

Closeout fact order: `<outcome> -> <acceptance> -> <regression> -> <documentation> -> <remaining risk> -> <release or next action>`.

Arrow sequence is fact order, not output wording. Replace slots with project facts and omit slot labels. Add a permanent rule only for an observed failure, with the smallest useful check that catches it.
