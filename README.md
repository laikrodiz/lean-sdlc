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
- `tasks.csv` contains the human-readable task overview and changes only through bundled task commands. Use `tasks.py open` for current work or `tasks.py show TASK-ID` for one task plus recursive dependencies instead of loading full `Done` history.

The initializer also adds `/tasks.csv` and `/.tasks.lock` to `.gitignore`. Feature, decision, and operations documents remain optional.

## Modes and roles

Assisted mode is the default and persists until the user selects Solo. Solo mode keeps execution with the lead under the same task and safety rules. Assisted and Solo are the only orchestration modes.

Session state restores the owner, mode, and child tier after lifecycle events. Missing or invalid state restores Assisted with Standard children. Luna uses Standard service by default. Fast children are opt-in; new or normally replaced Luna children use the priority tier after that choice, while reachable threads remain available.

| Role | Responsibility |
| --- | --- |
| Engineer | Implements an approved task. |
| Maintainer | Synchronizes affected shared documents and runs recorded operational procedures. |
| Verifier | Checks acceptance independently. |
| Scout | Collects bounded, cited evidence for non-trivial inquiries. |

See the [canonical child-agent policy](plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md) for role lifecycle and communication rules.

Assisted mode delegates bounded independent work through the canonical child-agent policy. Solo mode keeps execution with the Architect. The Maintainer keeps shared documents current and runs recorded procedures.

The Architect owns intent, architecture, task boundaries, acceptance, integration, proof, and closeout.

## Workflow

1. Before changes, the Architect confirms why -> what -> how -> proof. This covers user or business value, outcome and boundaries, technical approach, and acceptance evidence.
2. Plan and tasks turn approved intent into measurable work, owned task rows, and reproducible proof. The human-readable `tasks.csv` remains authoritative.
3. Each ledger task maps to one Engineer checkpoint under the [Plan contract](plugins/lean-sdlc/skills/lean-sdlc/references/plan.md). Keep tests and attached Maintainer or Verifier work in the task unless independently deliverable.
4. Assisted mode uses bounded Scout evidence for non-trivial inquiries. At most two independent children may work in the same worktree only after one resource gate passes. Solo stays with the Architect.
5. Children stop before integration. The Architect reviews accepted work for scope and contract alignment.
6. The Maintainer synchronizes affected shared documents.
7. Integration and verification run serially. Verification runs acceptance proof and one planned regression command. The full suite runs only when required.
8. Operations replay required recorded build, package, deploy, flash, runtime, or smoke procedures against accepted source.
9. Closeout resolves evidence, updates repository truth, and closes the owned task.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

Install the immutable `v1.13.0` release:

```bash
git clone --depth 1 --branch v1.13.0 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
```

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
