# Lean-SDLC for Codex

## Why

Fast code is not useful if it solves the wrong problem or no one can show that it works. Lean-SDLC keeps the user's purpose, the owner, and the evidence visible from request to result.

## What

Lean-SDLC gives Codex one workflow for discussion, planning, and authorized changes. You can discuss an idea or ask for a plan without changing files or creating tasks. A request to plan and implement lets Codex proceed within the agreed limits.

The Lead starts in plain prose. The opening explains who needs the change, what must improve, and why. It states the proposed approach, shared limits, and important unknowns. No fixed headings are required.

Each task has one result that the Lead can accept on its own. It states what must be true when done and which checks will show it. The Lead checks every candidate for separate outcomes before grading it, even when it looks Normal. One sizing pass settles the boundaries and assigns Simple, Normal, or Complex. Related steps stay with their result. A genuinely Complex task stays together, with a short reason why another split would not help.

## How

The Lead owns the result and works on one task at a time by default. Before changes start, the task must have an owner and pass the required check. If another outcome appears during work, the Lead separates it before implementing it. The original task still needs its unfinished requirements and proof.

The Lead makes small documentation edits and runs focused checks. A Scout investigates important uncertainty. A Maintainer updates shared documents when the change is substantial. A Verifier provides required independent proof or checks material risk. The Lead uses support only as needed and waits for each assignment before doing more work.

The Lead checks that valid evidence covers the request and examines gaps or exceptions. The Lead does not repeat an accepted review. Essential checks, safety proof, and required usage instructions cannot wait. Eligible Simple work can defer broader review only if the Lead marks that review as pending.

The user controls what may change and which delivery actions are authorized. A source change does not authorize a commit, push, installation, publication, or deployment. If work is canceled, the Lead confirms that its process stopped before work resumes on that target.

### Parallel Engineers

Ask for Parallel Engineers in the current request to let independent tasks run at the same time. The requested count is a maximum. The Lead uses only as many Engineers as the work and available resources support. The Lead starts queued tasks when slots are free and their accepted inputs are available.

Each Engineer uses the Lead model and reasoning effort in a separate checkout. The Lead combines the accepted changes and checks the combined result before delivery. If the user authorizes a push, the Lead pushes the accepted destination once. The Lead does not publish Engineer branches.

The Lead removes only recorded temporary checkouts after their processes stop and their results are retained. The Lead keeps unfinished or disputed work for recovery. See the [parallel rules](plugins/lean-sdlc/skills/lean-sdlc/protocols/parallel.md).

## Install

Requirements: Git, Python 3, and Codex with plugin support.

These commands install the immutable v1.36.0 release.

~~~bash
git clone --depth 1 --branch v1.36.0 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
~~~

Restart Codex. Then start a new chat.

## Use

Start with `Use $lean-sdlc to`, then say what you want:

- Discuss this idea without changing files.
- Make a plan only.
- Plan and implement this change.
- Plan and implement this change with up to three Parallel Engineers.
- Continue this repository task.
- Upgrade this repository to the current contract.

Upgrades preserve existing project documents, custom rules, and task history. See the [upgrade rules](plugins/lean-sdlc/skills/lean-sdlc/references/ledger.md#initialization-and-upgrade).

## Details

See the [project scope and release status](docs/PROJECT.md) and the [skill entry](plugins/lean-sdlc/skills/lean-sdlc/SKILL.md). The skill entry links to the planning, documentation, operations, and role rules. See the [recorded release check](docs/OPERATIONS.md) when you need to validate a release candidate.
