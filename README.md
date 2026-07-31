# Lean-SDLC for Codex

Lean-SDLC is one installable Codex plugin that keeps a software repository tied to clear intent, owned work, and proof without turning process into a second product.

It bundles one skill, `$lean-sdlc`, with six lanes:

| Lane | Meaning |
| --- | --- |
| Shape | Clarify the problem, user, scope, version promise, and observable success. |
| Decide | Record only durable technical choices that are costly to reverse or easy to forget. |
| Plan | Create small owned tasks and choose the cheapest safe execution shape. |
| Diagnose | Reproduce or bound an uncertain failure before selecting a fix. |
| Deliver | Implement one approved slice and keep affected documentation in sync. |
| Verify | Prove acceptance, reconcile repository truth, and close the task with evidence. |

The router enters the earliest unresolved lane and may continue through later gates in the same task. It does not run every lane mechanically.

## Engineering style

Lean-SDLC builds the smallest cohesive units that can be understood, tested, and replaced through narrow contracts. Architecture grows from real responsibility, change, state, I/O, failure, or replacement pressure instead of project-size labels or speculative abstractions.

Changed boundaries receive a short plausible edge-case scan with explicit `Handle`, `Reject`, `Defer`, or `Impossible by invariant` treatment. Useful visual explanations use compact Mermaid diagrams, mappings use tables, and simple relationships stay in prose.

## What it adds to a project

Initialization creates only three Lean-SDLC control files:

- `AGENTS.md` — durable repository rules;
- `docs/PROJECT.md` — problem, scope, current promise, and success;
- `tasks.csv` — a private, human-readable task overview.

It also creates or extends `.gitignore` with `/tasks.csv` and `/.tasks.lock`. Feature, decision, and operations documents are optional. They appear only when durable shared knowledge justifies them. The ledger may be changed only through the bundled atomic task command.

## Agents

All child-agent rules live in one editable policy: `references/subagents.md`. Before delivery or the first delegated read-only operation, Codex must state:

`Mode | Required sidecars | Eligible Workers | Reason`

Assisted mode is the default. Verifier is mandatory for code or behavior checkpoints and multi-command or noisy proof. Operator is mandatory when a guided or recorded build, package, CI, deploy, flash, runtime, or smoke operation is ready. Workers are allowed only for bounded independent deliverables with explicit ownership, settled decisions, known proof, and a net context or time saving. One Worker is normal; a second requires disjoint work.

`focused mode` keeps the lead and mandatory sidecars. `solo mode` runs the same workflow with the lead alone. Every Luna child uses Luna `max`; unavailable Luna profiles fall back explicitly to Terra `high`. Every spawn specifies model, reasoning, and bounded context. The lead retains decisions, integration, task state, and closeout.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

Install the immutable `v1.2.0` release:

```bash
codex plugin marketplace add laikrodiz/lean-sdlc --ref v1.2.0
codex plugin add lean-sdlc@lean-sdlc
```

Restart Codex, review and trust the plugin hook, then begin a new task.

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

Codex verifies and closes the one-time bootstrap task. Restart or resume afterward so the plugin hook supplies the stable numeric owner for normal work.

For existing work:

```text
Use $lean-sdlc to continue the project safely.
Use $lean-sdlc to investigate this failing test.
Use $lean-sdlc in focused mode to implement the active task.
Use $lean-sdlc in solo mode and verify the change.
```

After upgrading an older Lean-SDLC project, ask:

```text
Use $lean-sdlc to upgrade this repository to the current contract.
```

That migration moves `planning/tasks.csv` to root `tasks.csv` under the active task lock.

## Package layout

- `.agents/plugins/marketplace.json` exposes the repository marketplace.
- `plugins/lean-sdlc/.codex-plugin/plugin.json` defines the versioned plugin.
- `plugins/lean-sdlc/hooks/hooks.json` provides the stable task owner at session start and after compaction.
- `plugins/lean-sdlc/skills/lean-sdlc/SKILL.md` is the single dispatcher.
- `plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md` is the canonical child-agent policy.
- `plugins/lean-sdlc/skills/lean-sdlc/references/` also contains the six lanes and other shared policies.
- `plugins/lean-sdlc/skills/lean-sdlc/scripts/` contains initialization, task transactions, owner generation, and structural checks.
