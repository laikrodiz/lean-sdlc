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

All child-agent rules live in one editable policy: `references/subagents.md`. Before delegation, Codex tells the user the mode, child action, active task or inquiry, and reason in one or two short sentences.

Assisted mode is the default. The user-selected lead keeps architecture, interfaces, task setting, integration, and closeout. Each lead Codex task lazily creates at most one `executor`, `researcher`, `verifier`, and `operator` thread. Codex reuses each role across repository tasks and inquiries. Task identifiers stay inside handoffs and returns. Codex gives one durable task beyond the direct fast path to Executor. Executor performs local implementation and fast targeted checks. Executor returns one task checkpoint. The lead reviews architecture, scope, and diff once per returned checkpoint. Corrections return as concise deltas to the same Executor.

Before every child handoff, the lead tells the user the role, task or inquiry, intended result, and proof. This visible assignment provides startup visibility. After work finishes or blocks, the child sends one labeled final-result report. Children send no periodic progress updates. Internal handoffs use labeled multiline fields. User-facing orchestration uses normal prose.

Verifier independently reruns acceptance-defining proof against the exact checkpoint. It adds risk-based regression and skips Executor-only targeted checks. It normally runs the full suite once. Operator runs guided or recorded build, package, CI, deploy, flash, runtime, and smoke operations. Verifier consumes Operator evidence instead of repeating the operation. Researcher is read-only and handles substantial multi-source, multi-repository, large-document, data, log, or noisy evidence collection. `focused mode` keeps triggered sidecars, including Researcher when its trigger applies, and disables Executor. `solo mode` runs the same contracts locally.

Every primary child uses the named `lean_sdlc_luna` profile. The profile pins Luna `max`. The spawn supplies the Executor, Researcher, Verifier, or Operator role in its handoff. Primary Luna spawns use `agent_type=lean_sdlc_luna`. They omit direct model and reasoning fields. They also use non-full-history context. Terra `xhigh` is the direct fallback when the profile is unavailable, unexposed, or rejected. The lead announces the fallback before it spawns Terra.

Lean-SDLC applies the applicable ASD-STE100 Issue 9 rules to generated English technical prose. It uses active voice and one term for one meaning. It limits procedural sentences to 20 words. It limits descriptive sentences to 25 words. It puts a condition before its action. It preserves exact code, commands, paths, identifiers, protocol fields, quotations, and required domain terms. It does not claim certified or full controlled-dictionary compliance without an ASD-STE100 checker.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

Install the immutable `v1.6.0` release:

```bash
git clone --depth 1 --branch v1.6.0 https://github.com/laikrodiz/lean-sdlc.git
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
- `plugins/lean-sdlc/skills/lean-sdlc/scripts/` contains initialization, task transactions, profile configuration, owner generation, and structural checks.
