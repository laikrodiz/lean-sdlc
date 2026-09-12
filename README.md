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
    B --> C[Lead implements]
    C --> D[Verifier checks]
    D --> E[Maintainer records]
    E --> F[Lead reconciles]
~~~

The Lead interprets the request, confirms authority, and chooses the technical direction.

The plan divides work into independently accepted tasks with clear acceptance and proof.

Implementation starts only after the plan is ready. Completion requires evidence that matches the original request.

## Conversation and authority

Conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until the user gives implementation authority.

Before the initial task set, new authorized work, or a material scope change, the Lead visibly restates meaningful intent and shows all five plan fields. Later task claims reuse the unchanged visible approved plan.

A plan-only request remains read-only and stops after the plan.

A plan-and-implement request continues within the stated authority without another approval round.

Material ambiguity stops for user direction. A clear request keeps moving.

## Roles

The selected Codex model is the Lead. The Lead remains responsible for the result.

| Role | Work |
| --- | --- |
| Lead | Owns intent, architecture, scope, permissions, tasks, acceptance, integration, and final decisions. Implements code and writes code-local tests. |
| Scout | Maps bounded read-only evidence, contracts, callers, and gaps. |
| Maintainer | Performs routine ledger writes, maintains shared documents and indexes, and replays authorized recorded operations. |
| Verifier | Runs all tests and independent acceptance and regression proof. It does not change tracked files. |

The Lead gives each support role an exact boundary, input, acceptance, proof, and stop condition.

Before launch or reassignment, each support handoff states its purpose and whether work waits or continues. Event-driven waits avoid routine status and log polling. Routine subagent start, acknowledgment, and progress messages are omitted. Report failures, blockers, and required decisions immediately; otherwise return one useful final result without duplicate success messages. Related ledger work may be batched, a next-task Scout may prepare ready work, proof may be consolidated, and Maintainer returns final handoff facts. Routine ledger success stays silent unless IDs, prerequisites, or final reconciliation are needed.

Independent stable scopes may overlap only with stable inputs, separate mutable resources, no unfinished dependency, and meaningful time savings. Shared interfaces and external targets stay serial.

## Planning and task state

The visible plan uses five fields:

- Outcome: the observable result and why it matters.
- Work: independently accepted changes, their grades, and sequencing.
- Acceptance: what must be true.
- Checks: how Verifier establishes those facts.
- Limits: exclusions, unresolved choices, and operation authority.

Each task has one accepted outcome, one proof cluster, and one close decision.

Simple, Normal, and Complex grades describe task complexity. They stay in the visible plan and handoffs. They do not change the ledger schema.

The root tasks.csv ledger is authoritative. It records task IDs, titles, statuses, contexts, dependencies, owners, acceptance, proof, and evidence.

The visible task state uses exact task IDs and titles. It never invents IDs or replaces ledger state with generic progress reports.

The initial table shows all current authorized work, with the first task In Progress. Middle updates show changed rows only. The final table reconciles actual ledger state. After accepted closure, Lead may show Done and continue ready work without waiting for ledger acknowledgment. A failed transaction corrects only affected visible rows. Real IDs, ownership, dependencies, and before-write gates remain prerequisites.

Backlog is parked work. Only direct user authority can add or promote a Backlog item.

## Small changes

An eligible Simple task uses the Quick Fix context and its pending-review markers.

Verifier runs the immediate essential check. Broader regression and documentation review can remain explicitly pending for a shared checkpoint.

Do not defer a known safety failure, required usage instruction, or necessary validation.

## Documentation

Every initialized repository needs:

- AGENTS.md for the workflow entry and project rules.
- docs/PROJECT.md for project purpose, scope, constraints, promise, and exit evidence.
- Root tasks.csv for durable task state.

Optional documents appear only when a concrete trigger needs durable shared detail.

Numbered document families use the matching template in assets/. Each family receives an INDEX.md when its first numbered document exists.

The Maintainer owns shared narrative truth and indexes. The Lead approves meaning and document splits.

Documentation review defaults to affected work and reuses valid review evidence. Broad review applies only for broad impact or missing relevant evidence.

## Verification

Lead writes implementation and test code. Verifier runs the required test and proof commands.

Verification assignments state a specific acceptance question, minimum sufficient checks, and a stop condition. Report unavailable proof; runtime investigation is not automatic. Required proof is not silently waived; reduced acceptance requires user approval.

Verification checks the original user request, the task acceptance, and affected regression risk.

Stable inputs are checked before and after proof. Changed inputs invalidate affected evidence.

The workflow preserves the distinction between actual behavioral checks, structural assertions, and saved-response checks.

## Recorded operations

A first build, package, deployment, flash, runtime, or smoke procedure becomes recorded only after a guided success.

Later Maintainer runs replay the valid procedure against its explicit target and accepted source identity.

Automatic routine discovery and automatic script-creation suggestions are not part of this workflow.

Create a new reusable script only after an explicit user request.

Standing authority can cover the same recorded scope and target. Do not infer publication, deployment, commit, or push authority from an idea or code request.

## Install

Requirements:

- Git
- Python 3
- Codex with plugin support

Install the immutable v1.30.0 release:

~~~bash
git clone --depth 1 --branch v1.30.0 https://github.com/laikrodiz/lean-sdlc.git
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
