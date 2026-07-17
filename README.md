# Lean-SDLC for Codex

Lean-SDLC is a small set of Codex skills for taking a software project from a rough idea to verified implementation without losing the link between intent, tasks, code, tests, and documentation.

The basic flow is:

`idea -> scope -> architecture -> tasks -> implementation -> verification`

Codex selects the relevant skill automatically. You can also request one directly, for example: `Use $lean-brainstorm to shape this idea.`

## Skills

| Skill | Purpose |
| --- | --- |
| `lean-sdlc-core` | Defines the shared lifecycle, repository structure, traceability rules, and document contracts used by the whole bundle. |
| `lean-brainstorm` | Turns a rough idea into a clear project brief, scope, and first feature definitions. |
| `lean-refine` | Removes ambiguity, splits oversized features, and defines how each feature will be proved. |
| `lean-architecture` | Chooses the simplest defensible system structure, technology boundaries, and durable technical decisions. |
| `lean-task-planning` | Converts approved features and decisions into small, traceable implementation tasks. |
| `lean-execution` | Chooses how ready tasks should be executed: locally, by delegated agents, or in controlled batches. |
| `lean-debugging` | Reproduces and isolates failures, identifies the root cause, and decides what project truth must change. |
| `lean-implementation` | Implements an approved task while keeping code, tests, diagnostics, and documentation aligned. |
| `lean-verification` | Checks completed work against acceptance criteria and evidence before a task is closed. |
| `lean-traceability` | Audits and repairs links between scope, features, decisions, tasks, code, tests, and diagnostics. |
| `lean-versioning` | Keeps project stage and version framing current as a delivery slice closes or the business context changes. |
| `lean-doc-maintenance` | Removes stale documentation, repairs drift, and splits documents only when complexity justifies it. |

## Install

Requirements: Git and Codex.

```bash
git clone https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
./scripts/install.sh
```

Restart Codex after installation.

The installer copies every bundled skill into `${CODEX_HOME:-$HOME/.codex}/skills`. It refuses to overwrite an existing installation. To replace an older version intentionally:

```bash
git pull
./scripts/install.sh --force
```

## Use

Start with a plain request such as:

```text
Use Lean-SDLC to turn my project idea into a small, implementable plan.
```

For an existing project, ask Codex to use `$lean-sdlc-core` to set up or audit the repository. The other skills will guide the next stage when their work is needed.

## Package contents

- `skills/` contains only the Lean-SDLC Codex skills and their required metadata and references.
- `scripts/install.sh` installs the complete bundle locally.

