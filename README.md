# Lean-SDLC for Codex

Lean-SDLC is an installable Codex plugin for software work with clear intent, owned tasks, and reproducible proof.

## Lanes

The plugin routes each request through the earliest unresolved lane.

| Lane | Purpose |
| --- | --- |
| Shape | Define the problem, user, scope, promise, and observable success. |
| Decide | Record technical choices that need durable agreement. |
| Plan | Create owned tasks and choose a safe execution shape. |
| Diagnose | Bound an uncertain failure before selecting a fix. |
| Deliver | Implement one approved change and synchronize affected truth. |
| Verify | Check acceptance, reconcile repository truth, and close with evidence. |

## Project files

Initialization creates three control files:

- `AGENTS.md` contains durable repository rules.
- `docs/PROJECT.md` contains the problem, scope, promise, and success criteria.
- `tasks.csv` contains the private task overview and changes only through bundled task commands.

The initializer also adds `/tasks.csv` and `/.tasks.lock` to `.gitignore`. Feature, decision, and operations documents remain optional.

## Modes and roles

Assisted mode is the default. It invokes the roles needed for the request. Solo mode keeps execution with the lead under the same task and safety rules. Assisted and Solo are the only orchestration modes.

| Role | Responsibility |
| --- | --- |
| Engineer | Implements an approved task. |
| Maintainer | Runs a recorded operational procedure. |
| Verifier | Checks acceptance independently. |
| Researcher | Collects cited evidence for complex inquiries. |

See the [canonical child-agent policy](plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md) for role lifecycle and communication rules.

## Workflow

Intent becomes a measurable plan and an owned task. The Architect keeps product and architecture decisions. Assisted mode reuses Engineer, Maintainer, Verifier, or Researcher only when triggered. Solo mode follows the same gates locally. Changes close only after independent evidence.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

Install the immutable `v1.8.2` release:

```bash
git clone --depth 1 --branch v1.8.2 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
python3 plugins/lean-sdlc/skills/lean-sdlc/scripts/configure_codex.py
python3 plugins/lean-sdlc/skills/lean-sdlc/scripts/configure_codex.py --check
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
```

The configurator prepares Codex for the plugin. It preserves unrelated settings and backs up changed owned files with a `.bak` suffix. Use `--codex-home` for an alternate Codex home.

Restart Codex after installation. Review and trust the plugin hook. Then begin a new task.

If an older standalone copy exists, move it outside the skills directory after the plugin installs:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/legacy-skills"
mv "${CODEX_HOME:-$HOME/.codex}/skills/lean-sdlc" \
  "${CODEX_HOME:-$HOME/.codex}/legacy-skills/lean-sdlc"
```

## Use

For a new repository:

```text
Use $lean-sdlc to initialize this repository and shape the project.
```

For existing work:

```text
Use $lean-sdlc to continue the project safely.
Use $lean-sdlc to investigate this failing test.
Use $lean-sdlc in solo mode and verify the change.
```

After upgrading an older Lean-SDLC project:

```text
Use $lean-sdlc to upgrade this repository to the current contract.
```

The migration moves `planning/tasks.csv` to root `tasks.csv` under the active task lock.
