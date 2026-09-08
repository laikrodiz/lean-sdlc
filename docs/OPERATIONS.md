# Recorded operations

This document records the first guided release-check procedure.

## Candidate release validation

### Status

Active as a recorded procedure. Each release candidate requires a fresh run. The last result applies only to its recorded inputs.

### Maintenance Owner

Maintainer records and coordinates this procedure. Verifier owns test execution. Lead accepts the result.

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
- Verifier owns test execution. Maintainer records the result.
- The required inputs exist and the candidate source is frozen.
- The command runs from the selected repository root.
- Python 3 and the repository test environment are available.
- This procedure has no publication, installation, commit, tag, or push authority.

### Steps

1. Confirm the selected repository root and required inputs.
2. Confirm that source, tests, scripts, instructions, project documents, manifest, and ledger remain frozen.
3. From the selected repository root, run the canonical command.
4. Verifier confirms the exit status and every reported check layer.
5. Maintainer records the result and keeps successful logs ephemeral.

### Outputs and Artifacts

- Process exit status and terminal result.
- Unit-test, structural, saved-fixture, and release-check results.
- No retained generated artifact is required.
- Do not record successful raw logs or secret values.

### Success

The guided command exited with status 0. That result included 122 unit tests, the structural check, 60 saved-fixture assertions, and release checks.

Later test and documentation changes invalidate that checkpoint. The final accepted candidate must pass a fresh run.

This procedure validates the selected local candidate only. It does not establish a commit, remote identity, tag, push, installation, or installed/source equality.

### Failure and Recovery

If a check fails, an input is missing, the target changes, or the command exits non-zero, stop and return the actual evidence to Lead.

Do not repair source files, retry automatically, or claim a successful replay. Lead may authorize a correction or environment repair for the exact failure. Run a fresh validation after the correction with frozen inputs.

If cancellation occurs, confirm that the underlying Python process stopped. Keep the target blocked when termination is uncertain.

### Identity and Invalidation

The historical guided checkpoint covered candidate version 1.28.0 before a commit identity was available. This record does not assert the current candidate's commit identity.

The earlier guided result does not cover the changed final candidate.

Invalidate this record after any change to source, tests, scripts, AGENTS.md, README.md, docs/PROJECT.md, the plugin manifest, tasks.csv, Python or test dependencies, release-check logic, or the selected repository target.

### Last Verified

2026-09-08. The historical candidate version was 1.28.0. The selected repository passed 122 unit tests, the structural check, 60 saved-fixture assertions, and release checks. This local procedure does not establish publication or installation.
