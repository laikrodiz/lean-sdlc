# Lean-SDLC for Codex

Lean-SDLC is one Codex skill that routes software work from a rough idea to verified delivery while keeping intent, tasks, code, tests, and documentation connected.

The normal flow is:

`idea -> scope -> architecture -> tasks -> implementation -> verification`

You invoke one entry point, `$lean-sdlc`. It inspects the repository state and selects the smallest relevant workflow.

## Workflows

| Workflow | Meaning |
| --- | --- |
| Brainstorm | Turn a rough idea into a brief, scope, and first small feature definitions. |
| Refine | Remove ambiguity, split oversized features, and define acceptance and failure signals. |
| Architecture | Choose the simplest defensible stack, boundaries, and durable technical decisions. |
| Task planning | Convert approved features and decisions into small traceable tasks. |
| Execution | Decide whether ready tasks should stay local or use bounded parallel workers. |
| Debugging | Reproduce and isolate an uncertain failure before choosing a fix. |
| Implementation | Execute one approved task without expanding its scope. |
| Verification | Prove acceptance and documentation parity before closing work. |
| Traceability | Resolve conflicts and broken links between intent, tasks, code, tests, and diagnostics. |
| Versioning | Keep project stage, release promise, and exit criteria honest. |
| Documentation maintenance | Apply approved cleanup and synchronization after the correct truth is known. |

Model choice follows task shape: Sol handles high-leverage judgment, Terra handles ordinary engineering, and Luna handles mechanical repeatable work. Explicit user model and reasoning requests always take precedence.

## Model and agent control

- `strict` keeps the selected model for the complete task without delegation unless you request it. It is the default when you request a model or Max reasoning.
- `lead` keeps the selected model for decisions and integration while allowing cheaper bounded support.
- `economy` lets Lean-SDLC route automatically across available GPT-5.6 models.

Lean-SDLC defaults to no subagents and at most two when independent work justifies their cost. It reuses a worker only while task, role, owned files, and assumptions remain stable. Workers return concise evidence to the main agent, which performs integration and closeout.

Cache reuse is treated as a measured optimization. Instructions stay stable, variable task data stays at the end, and agents receive file references and incremental updates. Lean-SDLC never creates work merely to warm a cache.

## Tracked changes

Every repository file mutation requires one owned `In Progress` task with measurable acceptance and proof. This includes code, documentation, configuration, tests, generated files, and small maintenance edits. Read-only work needs no task. Atomically inserting the row that authorizes upcoming work is the only routine pre-task file mutation.

Feature work links to `FEAT-*`, durable technical work links to `DEC-*`, and maintenance uses `REPO`. Initialization creates the ledger and active `TASK-000` atomically under the one-time `BOOTSTRAP` parent.

When upgrading an existing ledger, replace `planned`, `in_progress`, and `done` with `Planned`, `In Progress`, and `Done`.

## Install

Requirements: Git, Python 3, and Codex.

```bash
git clone https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
./scripts/install.sh
```

Restart Codex after installation.

The installer copies `lean-sdlc` into `${CODEX_HOME:-$HOME/.codex}/skills`. It refuses to overwrite an existing installation or leave legacy multi-skill installations active.

To replace an older version intentionally:

```bash
git pull
./scripts/install.sh --force
```

The forced upgrade removes only the former Lean-SDLC skill directories and replaces them with the single dispatcher skill.

## Use

For a new project:

```text
Use $lean-sdlc to initialize this repository and shape my project idea.
```

For existing work:

```text
Use $lean-sdlc to continue this project safely.
```

You can also state the outcome directly:

```text
Use $lean-sdlc to investigate why this test fails.
Use $lean-sdlc to turn the approved feature into implementation tasks.
Use $lean-sdlc to verify and close the active task.
```

Initialization creates only missing Lean-SDLC control files and keeps existing files unchanged. The bundled checker validates the active task before writes and catches missing files, broken index paths, invalid task states, unknown parents, missing owners, empty acceptance or proof, and completed tasks without evidence.

## Package contents

- `skills/lean-sdlc/SKILL.md` is the single discoverable dispatcher.
- `skills/lean-sdlc/references/` contains the workflow and repository rules loaded only when needed.
- `skills/lean-sdlc/assets/AGENTS.md` is the concise project control-plane template.
- `skills/lean-sdlc/scripts/` contains safe initialization and structural validation tools.
- `planning/tasks.csv` tracks changes to this package itself.
- `scripts/install.sh` installs or upgrades the package.
