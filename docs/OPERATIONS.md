# Operations

## Release and install

- Status: Established from the verified `v1.25.1` execution. Each release run uses current task evidence.
- Maintenance owner: Maintainer.
- Purpose: Release one approved numeric version, install that tagged plugin, and upgrade only the approved repository when required.
- Exact targets: this repository's `main`, its configured `origin`, tag `v<version>`, marketplace entry `lean-sdlc`, installed plugin `lean-sdlc`, and the selected repository for any ledger upgrade.
- Control ownership: Architect owns ledger, commit, annotated tag, and push actions. Maintainer may run explicitly assigned installation and other recorded non-Git operations.

### Prerequisites

- The Architect approved the release task, version, changed files, acceptance, and proof.
- `main` contains only approved task changes. Release inputs are frozen. No unrelated changes are present.
- `README.md`, `docs/PROJECT.md`, and the plugin manifest contain one matching numeric version.
- The configured marketplace entry `lean-sdlc` points to this repository. Do not rewrite marketplace configuration.
- The `codex` command on `PATH` matches the active app configuration. If it rejects `config.toml` feature maps, use the compatible app-bundled CLI. Do not edit configuration files.
- Resolve `<skill-creator-root>` and `<plugin-creator-root>` from the local configured tool roots. Do not record absolute machine paths.
- This procedure does not run benchmarks, live evaluations, or model trials, or add their outputs. A separate request governs such work.

### Ordered steps

1. Architect confirms the task gate, approved task changes on `main`, remote identity, version consistency, and source freeze.
2. Verifier computes a read-only initial checkpoint over every approved release input. Pass one explicit file or directory argument per input. Do not pass the repository root:

   ```text
   python3 plugins/lean-sdlc/skills/lean-sdlc/scripts/checkpoint.py --repo . <approved-release-inputs>
   ```

3. Run the portable gate from the repository root:

   ```text
   python3 scripts/release_check.py --install-smoke
   ```

4. Run the configured skill and plugin validators:

   ```text
   python3 -B <skill-creator-root>/scripts/quick_validate.py plugins/lean-sdlc/skills/lean-sdlc
   python3 -B <plugin-creator-root>/scripts/validate_plugin.py plugins/lean-sdlc
   ```

5. After proof and final review, Verifier repeats the checkpoint. Continue only when both values match. Architect reviews the reported stable result.
6. Run `git diff --check`. Stop if any check fails.
7. Architect stages only approved release files and commits them with the approved release message.
8. Architect creates an annotated tag:

   ```text
   git tag -a v<version> -m "Lean-SDLC <version>"
   ```

9. Architect pushes the commit and tag atomically. Never force-push or replace an existing tag:

   ```text
   git push --atomic origin main refs/tags/v<version>
   ```

10. Architect confirms the local `HEAD`, annotated tag target, remote branch, and remote peeled tag identify the same release commit. Confirm that the working tree and plugin package have no changes or untracked additions:

   ```text
   git cat-file -t refs/tags/v<version>
   git rev-parse HEAD refs/tags/v<version>^{}
   git ls-remote origin refs/heads/main refs/tags/v<version> refs/tags/v<version>^{}
   git status --short --untracked-files=all
   ```

11. Maintainer installs the configured local marketplace source with the compatible `codex` CLI. `plugin add` uses that source; it does not select a Git tag:

   ```text
   codex plugin add lean-sdlc@lean-sdlc --json
   ```

   Confirm the installed package with:

   ```text
   codex plugin list --marketplace lean-sdlc --json
   ```

   Confirm that `lean-sdlc` is enabled at `<version>`. Do not record unrelated plugin entries.

12. Maintainer compares the installed and verified released source package file sets. Require equal file sets and byte equality for every corresponding file.
13. Architect runs the installed helper context check. Confirm the expected owner, mode, tier, and paths.
14. If the selected repository needs ledger migration, Architect runs the installed helper only for that repository:

    ```text
    python3 <installed-skill-root>/scripts/tasks.py --repo <repository-root> upgrade --task TASK-ID --owner OWNER
    ```

### Success signal

The portable gate, validators, checkpoint comparison, and diff check pass. The annotated tag and remote peeled tag identify the release commit. The working tree is clean before installation. The configured local source installs successfully, and the installed package matches the verified released source byte-for-byte. The helper context is correct. Any repository upgrade changes only its selected ledger.

### Failure and recovery

Stop on an unknown failure, a source change between checkpoints, a remote mismatch, an existing tag, package changes or untracked additions, a marketplace mismatch, or an installed-file mismatch. Keep failed logs as temporary artifacts and report their paths. Discard successful raw logs.

If the shell `codex` rejects feature-map parsing, switch to the compatible app-bundled CLI. Do not change `config.toml`, marketplace state, or global configuration. Do not retry a state-changing failure without an approved recovery rule. No forced push, tag replacement, or automatic rollback is authorized.

### Last verified context

The `v1.25.1` baseline was verified on `main` at short commit `f09e1ab`. The current host's compatible app-bundled CLI is `0.153.4` and supports `plugin list`. Each new release uses current task evidence; do not claim `v1.26.0` verification before its proof completes. Update this record only when the procedure or its verified context changes; do not make a post-release documentation change only for a timestamp.
