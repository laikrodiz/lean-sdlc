# Lean-SDLC for Codex

## Why

Before Codex changes code, you should be able to tell whether it understood your goal. Afterward, you should be able to see what changed and how it was checked. Lean-SDLC connects those two questions.

## What

You choose how far Codex goes. Ask a question or request a plan, and Codex leaves your files unchanged. Ask it to implement, and you get a plan you can follow: who needs the change, what should improve, and how Codex proposes to do it.

Each task has a result you can recognize and a check that shows whether it works. You can see which tasks are planned, in progress, or done.

## How

One **Lead** handles your request. By default, the Lead works on one task at a time in your project. It checks the result against your original request and tells you what passed and what remains unverified.

The Lead calls on specialists when needed. A **Scout** investigates an open question. A **Maintainer** updates shared project documents. A **Verifier** provides an independent check.

If you ask for or offer **Parallel Engineers**, the plan states how many the Lead will use and why. Your limit is a maximum. If the tasks depend on each other, the Lead can choose zero. Otherwise, Engineers can work on independent tasks in separate working directories. The Lead combines their changes and checks the result as a whole. See the [parallel rules](plugins/lean-sdlc/skills/lean-sdlc/protocols/parallel.md) for details.

Asking for edits does not authorize a commit, push, installation, publication, or deployment. Ask for the delivery steps you want.

## Install

Requirements: Git, Python 3, and Codex with plugin support.

These commands install the immutable v1.37.1 release.

~~~bash
git clone --depth 1 --branch v1.37.1 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
~~~

Restart Codex. Then start a new chat.

## Use

In your own project, start with `Use $lean-sdlc to` and say what you need. Ask to discuss an idea, make a plan, or plan and implement a change. To allow parallel work, add “use multiple Engineers if useful.”

For an existing Lean-SDLC project, you can ask to continue a task or [upgrade the project](plugins/lean-sdlc/skills/lean-sdlc/references/ledger.md#initialization-and-upgrade). Upgrades preserve project documents, custom rules, and task history.

## Details

See the [project scope and release status](docs/PROJECT.md) and the [skill entry](plugins/lean-sdlc/skills/lean-sdlc/SKILL.md). The skill entry links to the planning, documentation, operations, and role rules. See the [recorded release check](docs/OPERATIONS.md) when you need to validate a release candidate.
