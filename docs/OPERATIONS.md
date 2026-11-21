# Recorded operations

This document records the first guided release-check procedure.

## Candidate release validation

### Status

Active as a recorded procedure. Each release candidate requires a fresh run. The last result applies only to its recorded inputs.

### Maintenance Owner

Lead is the default executor and records this procedure, including its built-in checks. An explicitly assigned Verifier may execute the canonical check once as the designated independent executor; do not duplicate the gate. Maintainer updates this document only for an actual shared-document change and reports substantial reconciliation discrepancies. Lead applies accepted ledger corrections and accepts the result.

### Purpose and Target

Validate the candidate source before release.

Run from the selected repository root that contains scripts/release_check.py. Do not use another checkout, an installed package, or a temporary copy.

### Canonical Command

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/release_check.py
~~~

### Inputs and Defaults

- Source files in the selected repository.
- The tests/ and scripts/ directories.
- AGENTS.md, README.md, and docs/PROJECT.md.
- Python 3 and the current root tasks.csv ledger.
- The plugin manifest and package structure at the selected repository state.
- PYTHONDONTWRITEBYTECODE=1 prevents bytecode output.
- Keep all listed inputs frozen during the run.
- Remote commits, tags, and installed packages are not inputs to this local procedure.

### Prerequisites

- Lead authorizes validation of this selected repository and candidate.
- Lead owns direct recording. Maintainer does not replay the procedure.
- The required inputs exist and the candidate source is frozen.
- The command runs from the selected repository root.
- Python 3 and the repository test environment are available.
- This procedure has no publication, installation, commit, tag, or push authority.

### Steps

1. Confirm the selected repository root and required inputs.
2. Confirm that source, tests, scripts, instructions, project documents, manifest, and ledger remain frozen.
3. From the selected repository root, the designated executor runs the canonical command.
4. The designated executor confirms the exit status and every reported check layer. Lead records the result directly.
5. Do not run the same canonical check again only to duplicate the designated executor's proof.
6. Maintainer updates this record only when shared documentation changes and reports substantial reconciliation discrepancies. Lead applies accepted ledger corrections. Keep successful logs ephemeral.

### Outputs and Artifacts

- Process exit status and terminal result.
- Unit-test, structural, saved-fixture, and release-check results.
- No retained generated artifact is required.
- Do not record successful raw logs or secret values.

### Success

The canonical command must exit with status 0 for the unchanged candidate. All unit tests, structural checks, saved-fixture assertions, and release checks must pass.

This result covers only the selected local candidate. It does not establish publication or installation.

### Failure and Recovery

If a check fails, an input is missing, the target changes, or the command exits non-zero, stop and return the actual evidence to Lead.

Do not repair source files, retry automatically, or claim a successful replay. Lead may authorize a correction or environment repair for the exact failure. Run a fresh validation after the correction with frozen inputs.

If cancellation occurs, confirm that the underlying Python process stopped. Keep the target blocked when termination is uncertain.

### Identity and Invalidation

A change to source, tests, scripts, AGENTS.md, README.md, docs/PROJECT.md, the plugin manifest, tasks.csv, Python or test dependencies, release-check logic, or the selected repository target invalidates the previous result because an input changed. It does not invalidate this procedure by itself.

Invalidate this procedure when its canonical command, prerequisites, ordered steps, success or failure contract, authority, or target contract changes.

### Last Verified

Historical guided run, 2026-09-08: candidate v1.28.0 passed 122 unit tests, the structural check, 60 saved-fixture assertions, and release checks. No commit identity was available. This result does not cover later candidates.
