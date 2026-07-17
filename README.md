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

Model choice follows task shape: Sol handles high-leverage judgment, Terra handles ordinary engineering, and Luna handles mechanical repeatable work. Reasoning increases when ambiguity, risk, or failed proof justifies it.

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

Initialization creates only missing Lean-SDLC control files and keeps existing files unchanged. The bundled structural checker catches missing files, broken index paths, invalid task states, unknown task parents, and empty acceptance fields.

## Package contents

- `skills/lean-sdlc/SKILL.md` is the single discoverable dispatcher.
- `skills/lean-sdlc/references/` contains the workflow and repository rules loaded only when needed.
- `skills/lean-sdlc/assets/AGENTS.md` is the concise project control-plane template.
- `skills/lean-sdlc/scripts/` contains safe initialization and structural validation tools.
- `scripts/install.sh` installs or upgrades the package.
