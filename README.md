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

Each ledger row uses `Context` to name durable project truth. Use `Project`, `FEAT-*`, `DEC-*`, or `Bootstrap`. Dependencies keep task sequencing.

## Agents

All child-agent rules live in one editable policy: `references/subagents.md`. Before delegation, Codex gives the user a concise natural update that starts with the work or current state and states the child action, task or inquiry, intended result, useful boundaries, and proof. Codex mentions the mode only when it matters, changes, or the user asks.

Every user-facing lead message starts with outcome, work, or current state. The lead avoids repeating its role, model, mode, internal field labels, greetings, praise, filler, or roleplay unless clarity requires the information. Internal control data remains structured.

Children call the primary agent Architect in visible commentary, handoffs, returns, and decision requests. The primary agent speaks as I. Keep lead for internal policy wording where useful.

Assisted mode is the default. The user-selected lead acts as principal engineer and owns product intent, architecture, interfaces, invariants, task boundaries, integration, and task disposition. Each lead Codex task lazily creates at most one `engineer_david`, `maintainer_emily`, `verifier_michael`, and `researcher_sarah` thread. Codex reuses each role across repository tasks and inquiries. Task identifiers stay inside handoffs and returns. Codex gives one durable task beyond the direct fast path to Engineer. Engineer receives a settled decision envelope and chooses only local mechanics. The lead reviews architecture, scope, diff, and contract alignment once per returned checkpoint.

The task title and the lead's first assignment are the primary identity signal. The lead names the child on the first assignment and again only after replacement or when clarity requires it. Before every child handoff, the lead gives a natural assignment update with the required facts. At the first visible update for each newly assigned durable task or inquiry, a child may use one concise greeting and identity. After that first update, child commentary omits the greeting, name, and role unless replacement or genuine ambiguity requires identity. Use a natural `Hi, <identity> here. Starting...` variant. The robotic form `I am <role/name>` is disfavored. Later updates start with the current fact or action. Children report only material phase changes. Silent commands may receive at most two brief heartbeats at two-minute intervals. Internal handoffs use labeled multiline fields. User-facing orchestration uses natural prose. Lead messages and later child updates avoid repeated names, roles, fixed labels, ceremonial headings, greetings, praise, filler, and theatrical roleplay.

Standard child identities are Engineer David / `engineer_david`, Maintainer Emily / `maintainer_emily`, Verifier Michael / `verifier_michael`, and Researcher Sarah / `researcher_sarah`. Each child writes short plain-language commentary inside its own agent task at work start, implementation or evidence completion with proof starting, blocked state, and final result. Lead reports stay compact.

Discussion and proposal requests remain read-only. Explicit implementation wording or clear confirmation to proceed against an agreed recoverable proposal permits Plan and Deliver. Before task creation and implementation, the lead applies the natural intent and visible-plan contract in `references/plan.md`. A one-item plan is valid. `tasks.csv` is the only durable task plan, and each durable item maps to one task while implementation steps remain transient.

Before every Engineer handoff, the lead gives a concise visible architecture brief in natural prose with the task, decision, boundaries and invariants, non-goals, and proof. Fixed headings are not required in visible speech. After each checkpoint, the lead inspects the diff and contract alignment, then gives a natural sign-off with alignment, deviation, and next action. Internal handoffs and compact returns remain labeled and lossless. Verifier receives acceptance and the exact checkpoint, then independently reruns proof. Maintainer replays guided or recorded build, package, CI, deploy, flash, runtime, and smoke procedures without repairing source. Researcher receives a question and source boundary without a preferred answer. Assisted mode uses every triggered role. Solo mode uses lead-only execution under the same contracts. Assisted and Solo are the only orchestration modes.

Every primary child uses the named `lean_sdlc_luna` profile. Fast service maps to `service_tier=priority`. Primary Luna spawns use `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history context. If priority is unavailable or rejected, the lead announces the failure and retries Luna Max without `service_tier`. Terra `xhigh` and Sol omit `service_tier` unless the user explicitly overrides it. The lead preserves the user-selected lead model and tier.

Lean-SDLC applies the applicable ASD-STE100 Issue 9 rules to generated English technical prose. It uses active voice and one term for one meaning. It limits procedural sentences to 20 words. It limits descriptive sentences to 25 words. It puts a condition before its action. It preserves exact code, commands, paths, identifiers, protocol fields, quotations, and required domain terms. It does not claim certified or full controlled-dictionary compliance without an ASD-STE100 checker.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

Install the immutable `v1.8.1` release:

```bash
git clone --depth 1 --branch v1.8.1 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
python3 plugins/lean-sdlc/skills/lean-sdlc/scripts/configure_codex.py
python3 plugins/lean-sdlc/skills/lean-sdlc/scripts/configure_codex.py --check
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
```

The configurator registers the Luna profile and enables the required Multi-Agent V2 route. It keeps unrelated settings. It backs up changed owned files with a `.bak` suffix. Use `--codex-home` for an alternate Codex home.

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

Codex verifies and closes the one-time bootstrap task. Restart or resume afterward so the plugin hook supplies the stable numeric owner for normal work.

For existing work:

```text
Use $lean-sdlc to continue the project safely.
Use $lean-sdlc to investigate this failing test.
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
- `plugins/lean-sdlc/skills/lean-sdlc/scripts/` contains initialization, task transactions, profile configuration, owner generation, and structural checks.
