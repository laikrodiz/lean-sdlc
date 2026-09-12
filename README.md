# Lean-SDLC for Codex

Lean-SDLC helps Codex build projects of any size through a controlled and understandable process. It turns user intent into clear tasks, uses safe parallel work when useful, verifies every result, and grows documentation with the project.

It keeps four things connected:

- Why the change matters.
- What result the user expects.
- How the work will be done.
- What evidence proves the result.

This reduces accidental scope growth, forgotten decisions, oversized tasks, repeated work, and unsupported completion claims.

## How it works

Lean-SDLC has one workflow. It has no mode selector and no Engineer role.

~~~mermaid
flowchart LR
    A[Understand the request] --> B[Show the plan]
    B --> C[Lead implements and runs focused checks]
    C --> D{Independent proof needed?}
    D -->|yes| E[Verifier checks]
    D -->|no| F[Lead records and closes]
    E --> F
~~~

The Lead interprets the request, confirms authority, and chooses the technical direction.

The plan divides work into independently accepted tasks with clear acceptance and proof.

Implementation starts only after the plan is ready. Completion requires evidence that matches the original request.

## Conversation and authority

Conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until the user gives implementation authority.

Before the initial task set, new authorized work, or a material scope change, the Lead visibly restates meaningful intent and shows all five plan fields. Later task claims reuse the unchanged visible approved plan.

A plan-only request remains read-only and stops after the plan.

A plan-and-implement request continues within the stated authority without another approval round.

Task creation and ownership complete before the Lead announces a task start.

Material ambiguity stops for user direction. A clear request keeps moving.

## Roles

The selected Codex model is the Lead. The Lead remains responsible for the result.

| Role | Work |
| --- | --- |
| Lead | Owns intent, architecture, scope, permissions, tasks, acceptance, integration, and final decisions. Owns every task transaction and write through `tasks.py`, and performs recorded-operation replay, including built-in checks. Implements code, writes code-local tests, and runs immediate focused checks. |
| Scout | Maps bounded read-only evidence, contracts, callers, and gaps when substantial uncertainty exists. |
| Maintainer | Updates assigned shared documents or investigates and reports substantial reconciliation discrepancies. It does not perform routine ledger writes or recorded-operation replay. Lead applies accepted ledger corrections. |
| Verifier | Runs substantial independent acceptance and regression checks when assigned. It does not change tracked files. |

The Lead gives each support role an exact boundary, input, acceptance, proof, and stop condition.

Use support roles only when their bounded work is needed. Do not impose an agent quota. Before launch or reassignment, each support handoff states its purpose and whether work waits or continues. The process line in a single-task start announcement can satisfy that support-launch announcement. Do not repeat it. Event-driven waits avoid routine status and log polling. Routine subagent start, acknowledgment, and progress messages are omitted. Report failures, blockers, and required decisions immediately; otherwise return one useful final result without duplicate success messages.

Independent stable scopes may overlap only with stable inputs, separate mutable resources, no unfinished dependency, and meaningful time savings. Shared interfaces and external targets stay serial.

## Planning and task state

The visible plan uses five fields:

- Outcome: the observable result and why it matters.
- Work: independently accepted changes, their grades, and sequencing.
- Acceptance: what must be true.
- Checks: how Lead and, when assigned, Verifier establish those facts.
- Limits: exclusions, unresolved choices, and operation authority.

Each task has one accepted outcome, one proof cluster, and one close decision.

Simple, Normal, and Complex grades describe task complexity. They stay in the visible plan and handoffs, and in tables for multiple tasks. They do not change the ledger schema.

The root tasks.csv ledger is authoritative. It records task IDs, titles, statuses, contexts, dependencies, owners, acceptance, proof, and evidence. Lead owns every task transaction and write through `tasks.py`. All roles may read task facts.

The visible task state uses exact task IDs and titles. It never invents IDs or replaces ledger state with generic progress reports.

For one task, announce `Starting <real ID>: <exact title>.` Then show `Optimal process: <actual work/roles>.` Complete real task creation and ownership before the announcement. For one changed task, even within a multi-task workload, use a short status line. For multiple simultaneous changes, show changed rows only. Keep initial and final tables for multiple tasks. After accepting proof, Lead closes the task directly through the helper, confirms success, and shows Done. A failed transaction corrects only affected visible rows. Real IDs, ownership, dependencies, and before-write gates remain prerequisites.

Lead may continue independent ready work while verification runs when inputs are stable and the work has no unfinished dependency. Dependent work waits. Closure uses the verified conclusion without repeating verification. Original requirements, safety, authority, and missing proof remain binding.

Backlog is parked work. Only direct user authority can add or promote a Backlog item.

## Small changes

An eligible Simple task uses the Quick Fix context and its pending-review markers.

Lead runs the immediate focused check. Verifier runs substantial independent acceptance and regression checks when assigned. Broader regression and documentation/interaction reviews can remain explicitly pending for a shared checkpoint.

Do not defer a known safety failure, required usage instruction, or necessary validation.

## Documentation

Every initialized repository needs:

- AGENTS.md for the workflow entry and project rules.
- docs/PROJECT.md for project purpose, scope, constraints, promise, and exit evidence.
- Root tasks.csv for durable task state.

Optional documents appear only when a concrete trigger needs durable shared detail.

Numbered document families use the matching template in assets/. Each family receives an INDEX.md when its first numbered document exists.

The Maintainer owns shared narrative truth and indexes. The Lead approves meaning and document splits.

The Maintainer engages only for actual shared-document changes or substantial reconciliation investigation and reporting. There is no mandatory per-task assessment stage, no-document-change reason, or final bookkeeping. Documentation review defaults to affected work and reuses valid review evidence. Broad review applies only for broad impact or missing relevant evidence.

## Verification

Lead writes implementation and test code and runs immediate focused checks. Verifier runs substantial independent acceptance and regression checks when assigned.

Verification assignments state a specific acceptance question, minimum sufficient checks, and a stop condition. Report unavailable proof; runtime investigation is not automatic. Required proof is not silently waived; reduced acceptance requires user approval.

Verification checks the original user request, the task acceptance, and affected regression risk.

Stable inputs are checked before and after proof. Changed inputs invalidate affected evidence.

The workflow preserves the distinction between actual behavioral checks, structural assertions, and saved-response checks.

## Recorded operations

A first build, package, deployment, flash, runtime, or smoke procedure becomes recorded only after a guided success.

Lead runs and replays valid recorded procedures, including their built-in checks, against explicit targets and accepted source identities. An explicitly assigned Verifier may execute one recorded check once as the designated executor for required independent proof; do not duplicate that gate. Lead remains the default executor for ordinary operation replay. The Maintainer updates operation documents only when shared documentation changes and reports substantial reconciliation discrepancies; Lead applies accepted ledger corrections.

Automatic routine discovery and automatic script-creation suggestions are not part of this workflow.

Create a new reusable script only after an explicit user request.

Standing authority can cover the same recorded scope and target. Do not infer publication, deployment, commit, or push authority from an idea or code request.

## Install

Requirements:

- Git
- Python 3
- Codex with plugin support

Install the immutable v1.31.0 release:

~~~bash
git clone --depth 1 --branch v1.31.0 https://github.com/laikrodiz/lean-sdlc.git
cd lean-sdlc
codex plugin marketplace add .
codex plugin add lean-sdlc@lean-sdlc
~~~

Restart Codex after installation. Then start a new thread.

For release validation, run:

~~~bash
python3 scripts/release_check.py
~~~

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
