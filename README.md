# Lean-SDLC for Codex

Lean-SDLC is a small workflow that turns a stated user need into an owned, reviewable repository change. It connects:

- Why: the beneficiary, situation, desired progress, and established reason.
- What: observable behavior and constraints that must hold.
- How: the chosen approach and rationale, covering architecture and implementation.
- Proof: the checks, evidence limits, and remaining risk.

It keeps work proportional, reuses settled context, and requires evidence for completion claims.

## Why

Repository work can lose intent, ownership, or proof even when implementation is fast. Lean-SDLC keeps the reason visible, records only the needed work, and closes with evidence that matches the request. It does not invent business benefits for technical work.

## What

Lean-SDLC follows one lifecycle from intent through owned work, proof, documentation, operations, and closeout.

The visible plan has five fields:

- Outcome: who needs what progress, in which situation, and why it matters, using established context.
- Work: independently accepted changes, grades, sequence, approach, and rationale. How covers architecture and implementation.
- Acceptance: observable behavior and constraints.
- Checks: evidence needed, its limits, and who checks it.
- Limits: exclusions, unresolved choices, and operation authority.

Each task delivers a result that can be checked separately. Simple work uses narrow checks. Uncertain or cross-system work needs more investigation and proof. Simple, Normal, and Complex grades describe task complexity. They remain in the visible plan, handoffs, and multi-task tables.

## How

Before the initial task set, new authorized work, or a material scope change, Lead visibly restates the intent and all five fields. Later work reuses the approved plan. A plan-only request remains read-only and stops after the plan. A plan-and-implement request continues within its authority without another approval round.

Reuse settled context, decisions, and suitable architecture. Ask only about missing facts that could change the solution. Explain consequential choices through requirements and tradeoffs in Work. Compare alternatives only when they could change the choice. Material ambiguity waits for user direction.

Lead is accountable for the result and implements the change. Scout investigates bounded uncertainty. Maintainer updates assigned shared documentation. Verifier provides independent acceptance and regression proof when needed.

Support is conditional. Handoffs state their purpose and whether work waits or continues. Stable independent work continues while dependent work waits. Shared resources stay serial. Support roles cannot widen scope or change decisions.

Users track meaningful changes, decisions with reasons, evidence limits, and risk. Progress reports show results, decisions, or blockers, not command logs. Report failures, collisions, unsafe conditions, changed assumptions, and required decisions immediately.

Lead runs immediate focused checks. Verifier runs assigned independent proof. For eligible Simple work, broader regression or documentation reviews can remain explicitly pending for a shared checkpoint. Do not defer safety failures, required usage instructions, or essential validation. Changed inputs invalidate affected evidence and require rechecking.

Proof separates demonstrated behavior and constraints from expected effects. If Acceptance requires measured impact, missing proof blocks closure. Otherwise report the effect as unproven and do not invent a business benefit. Completion needs executed evidence that matches the request; a dispatched action, saved response, structural assertion, or unexecuted command is not enough. An accepted verified conclusion can close work without repeating the same verification.

## Authority and progress

The user controls scope and explicitly authorizes changes, commits, pushes, publication, and deployment. Clear requests do not need repeated approval. Conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until implementation authority exists.

Users see meaningful changes, decisions, evidence limits, and risk. Stable independent work continues while dependent work waits. Original requirements, safety, and missing proof remain binding.

## Documentation

The project keeps its purpose and limits in one shared document and tracks agreed work. Add separate documentation only when a behavior, decision, or procedure needs a lasting explanation.

A first guided build, package, deployment, flash, runtime, or smoke success adds its procedure to `docs/OPERATIONS.md`. Existing procedures replay exact commands against explicit targets and accepted source identities, with valid authority, safe recovery, and redacted output. Lead is the default executor. An assigned Verifier may execute one procedure as independent proof.

## Install

Requirements:

- Git
- Python 3
- Codex with plugin support

Install the immutable v1.32.0 release:

~~~bash
git clone --depth 1 --branch v1.32.0 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
~~~

Restart Codex after installation. Then start a new thread.

## Use

Discuss an idea without repository changes:

~~~text
Use $lean-sdlc to discuss this idea without changing files.
~~~

Create a plan only:

~~~text
Use $lean-sdlc to make a plan only.
~~~

Plan and implement an authorized change:

~~~text
Use $lean-sdlc to plan and implement this change.
~~~

Continue existing work:

~~~text
Use $lean-sdlc to continue this repository task.
~~~

Upgrade an older Lean-SDLC repository:

~~~text
Use $lean-sdlc to upgrade this repository to the current contract.
~~~

## Detailed rules

The following documents define exact behavior:

- [Conversation](plugins/lean-sdlc/skills/lean-sdlc/references/conversation.md)
- [Plan](plugins/lean-sdlc/skills/lean-sdlc/references/plan.md)
- [Ledger](plugins/lean-sdlc/skills/lean-sdlc/references/ledger.md)
- [Documentation](plugins/lean-sdlc/skills/lean-sdlc/references/documentation.md)
- [Operations](plugins/lean-sdlc/skills/lean-sdlc/references/operations.md)
- [Recorded release check](docs/OPERATIONS.md)
- [Shared protocol](plugins/lean-sdlc/skills/lean-sdlc/protocols/common.md)
- [Lead protocol](plugins/lean-sdlc/skills/lean-sdlc/protocols/lead.md)
- [Maintainer protocol](plugins/lean-sdlc/skills/lean-sdlc/protocols/maintainer.md)
- [Scout protocol](plugins/lean-sdlc/skills/lean-sdlc/protocols/scout.md)
- [Verifier protocol](plugins/lean-sdlc/skills/lean-sdlc/protocols/verifier.md)
