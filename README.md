# Lean-SDLC for Codex/T3 Code

Lean-SDLC gives Codex a lightweight way to work in your repository without a formal architecture board, a default interview, or extra paperwork.

## How to ask

You control how far Codex goes on every turn:

- **Discuss, diagnose, or ask for a plan** and Codex leaves your files untouched and creates no saved tasks. It asks a follow-up question only when a missing fact would actually change the solution.
- **Ask to implement** (or **plan and implement**) and Codex creates owned tasks with clear outcomes and checks. There is no separate "saved task" mode. Tasks exist for authorized implementation work.
- **Keep a backlog only if you want one.** You can explicitly ask to record an idea in the backlog, though you never have to; you can just ask for the change when you are ready.

Asking for edits does **not** authorize a commit, push, installation, publication, or deployment. Ask directly for the delivery steps you want.

## Follow a change

Before inspecting the project, Codex explains who needs the change, why, and what must stay true. For one small fix, it opens with the change and its check in one sentence. Multi-step work has a visible task plan. Each task has an outcome, completion criteria, a grade (`Simple`, `Normal`, or `Complex`), and a status (`Planned`, `In Progress`, or `Done`).

One **Lead** handles your request one task at a time in your checkout by default. When a task benefits from focused help, the Lead calls on specialists one at a time:

- **Lead** owns the work from start to finish: shapes the plan, implements code and small shared-doc edits, runs immediate checks and authorized procedures, updates the task ledger, and makes the final acceptance call.
- **Scout** investigates substantial open questions in read-only mode. It searches local files, traces callers, contracts, tests, and usage, and consults authoritative online sources when relevant and in scope. It returns sources, concrete findings, and unresolved gaps without editing files or implementing changes.
- **Maintainer** handles substantial shared documentation updates once behavior or decisions settle, and investigates significant mismatches between accepted work and task records. It does not handle generic code upkeep, implement features, run tests, or write to the ledger.
- **Verifier** provides an independent check when risk or acceptance calls for it. It checks the result against your original request, contracts, and evidence, and runs checks on frozen inputs as needed. It never patches code or edits tracked files; if something fails, it reports the failure back to the Lead to fix.

## Reading "Done"

At handoff, the Lead reports what changed, confirmed task states, what actually ran, and any gaps or unverified effects. Checks that were not run are never reported as passed.

For one simple fix, you get the result, what passed, and anything pending. No table is needed. If a Verifier finds a defect in completed work, the Lead claims a correction linked to the original task before editing and rechecks the repair.

Only eligible small, reversible tasks (those with settled boundaries and a passing immediate check) may defer broader regression or documentation/interaction review. When deferred, that review stays **explicitly marked as pending** (never implied fully reviewed) and is checked by Verifier at the next shared checkpoint, and before release. Essential checks, safety proof, known documentation defects, and required usage instructions cannot wait.

## Project memory and docs

Lean-SDLC keeps project memory in three core files:

- `AGENTS.md`: a small workflow entry point plus your repository's own custom rules.
- `docs/PROJECT.md`: the one required shared project document (purpose, scope, constraints, observable success, and current stage and version).
- `tasks.csv`: a local, gitignored ledger at the repository root tracking task IDs, owners, dependencies, acceptance criteria, proof, and evidence.

Lean-SDLC does **not** create a new document for every task. Every durable fact belongs in one authoritative place. Small doc edits happen alongside code under the Lead; substantial shared-doc work goes to the Maintainer. Optional documents are added only when a subject needs lasting shared detail: feature specs (`docs/features/FEAT-*.md`), technical decisions (`docs/decisions/DEC-*.md`), architecture notes (`docs/ARCHITECTURE.md` or `docs/architecture/ARCH-*.md`), or shared contracts for interfaces, data, and state machines. Operational instructions (`docs/OPERATIONS.md` or `docs/operations/OPS-*.md`) are recorded only after a build, package, deploy, or smoke procedure actually succeeds, never as unverified guesses. See the [documentation rules](plugins/lean-sdlc/skills/lean-sdlc/references/documentation.md) for the full layout.

To check an existing project, ask: `Use $lean-sdlc to review storage in this project.` [Storage Review](plugins/lean-sdlc/skills/lean-sdlc/references/storage-review.md) investigates what takes space and proposes specific cleanup batches. It makes no changes and needs no project setup.

## When Parallel Engineers help

Parallel work is opt-in for the current request only. If you ask for or offer **Parallel Engineers** (for example, by adding "use multiple Engineers if useful"), the plan states the chosen count (including `0`) and why before work begins.

Your requested number is a cap, not a quota. Tasks that depend on each other or touch the same files are sequenced, while other independent assignments can still run concurrently, with each Engineer working in its own isolated git worktree. When there is no useful parallel work, the Lead picks zero and works sequentially without worktrees. The Lead alone integrates their changes, resolves conflicts when safe, and checks the combined result before delivery. If a conflict cannot be resolved safely, the Lead stops. See the [parallel rules](plugins/lean-sdlc/skills/lean-sdlc/protocols/parallel.md) for details.

In T3, the trusted Lean-SDLC hook checks names on the direct agent launcher. Support names use the role and one Greek letter. An Engineer’s name must match an active task owned by the Lead. The launcher must request a separate worktree. Start Engineers from the project’s repository root without a project or environment override.

After accepting a T3 Engineer’s work and recording its checks, the Lead archives its verified Codex chat. The result stays available in T3. If the Lead cannot confirm the chat’s identity, it leaves the chat visible.

## Install and use

Requirements: Git, Python 3, and Codex with plugin support.

These commands install the immutable v1.41.0 release:

~~~bash
git clone --depth 1 --branch v1.41.0 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
~~~

After installation or an upgrade, review the Lean-SDLC hooks in Codex. Trust the reviewed hooks, restart Codex, and start a new chat in your project. An untrusted launch hook cannot block an agent.

Begin with `Use $lean-sdlc to` and say what you need: discuss an idea, make a plan, or plan and implement a change. In an existing Lean-SDLC project, you can ask to continue a task or [upgrade the project](plugins/lean-sdlc/skills/lean-sdlc/references/ledger.md#initialization-and-upgrade); upgrades preserve your project documents, custom rules, and task history.

## Details

- [Project scope and release status](docs/PROJECT.md)
- [Skill entry](plugins/lean-sdlc/skills/lean-sdlc/SKILL.md) (links to planning, documentation, operations, and role rules)
- [Recorded release check](docs/OPERATIONS.md) for validating a release candidate
