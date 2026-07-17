# Lean-SDLC Repository Contracts

## Mandatory Core

Every real project should have:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_BRIEF.md`
- `docs/SCOPE.md`
- `docs/FEATURE_INDEX.csv`
- `docs/DECISION_INDEX.csv`
- `docs/features/FEAT-xxx-*.md`
- `docs/decisions/DEC-xxx-*.md`
- `planning/tasks.csv`

## AGENTS.md

Keep it short. It is the control plane, not the knowledge base.

It must define:

- authority order
- reading order
- lifecycle model
- change routing
- required sequence
- doc spawn triggers
- parity rule
- task linkage rule
- approval checkpoints
- before-task-creation gate
- before-code gate
- before-done gate
- debug path
- review path
- stop conditions
- Occam rule
- Socratic challenge rule
- file split rule
- delegation rule
- rule: do not invent undocumented scope

Use the copy-ready [AGENTS template](../assets/AGENTS.md) as the baseline shape.

## PROJECT_BRIEF.md

Keep it short. Include:

- problem
- target user or operator
- intended outcome
- value
- constraints
- non-goals
- success criteria

## SCOPE.md

Include:

- in scope
- out of scope
- assumptions
- known limitations
- deferred ideas
- current stage
- current version
- version goal
- version exit criteria
- stage exit criteria

## FEATURE_INDEX.csv

Keep it mechanical. Recommended columns:

- `feature_id`
- `name`
- `status`
- `actor`
- `outcome`
- `value_summary`
- `file`
- `version`
- `notes`

## DECISION_INDEX.csv

Keep it mechanical. Recommended columns:

- `decision_id`
- `name`
- `status`
- `type`
- `impact_scope`
- `reversal_cost`
- `scope_ref`
- `file`
- `date`
- `notes`

## Feature Files

Every feature gets its own file. Each file must contain:

- `feature_id`
- `name`
- `status`
- `reason / value`
- `business context`
- `behavior`
- `constraints`
- `exclusions`
- `acceptance criteria`
- `verification approach`
- `diagnostics / failure signals`
- `related decisions`
- `related tasks`

Functional requirements belong mostly here.

Feature files are durable behavior interfaces, not scratchpads for implementation churn.

Feature boundary rules:

- one feature equals one independently valuable behavior slice
- one feature should be independently acceptable and independently deferrable
- one feature should serve one clear actor outcome
- split the feature when the file starts covering several outcomes or acceptance clusters

Split triggers:

- more than one distinct outcome
- more than one actor goal
- more than one real acceptance cluster
- repeated "and also" behavior
- tasks naturally split into independent deliveries
- part of the behavior could be deferred without killing the rest
- the file reads like a capability area or roadmap bucket

## Decision Files

Every decision gets its own file. Each file must contain:

- `decision_id`
- `name`
- `status`
- `type`
- `context`
- `decision`
- `consequences`
- `related features`
- `related tasks`
- `related docs`

Decisions are durable chosen paths that shape the system and can spawn tasks.
They are not recipe files for runtime detail, helper names, or tuning notes.

Decision sync rule:

- if implementation introduced a durable chosen path that is costly to reverse or easy to forget, create or update a decision before closeout

## tasks.csv

Use these columns:

- `task_id`
- `title`
- `status`
- `parent_ref`
- `depends_on`
- `acceptance`

Allowed statuses:

- `planned`
- `in_progress`
- `done`

Task rules:

- insert new tasks at the top of the file, directly below the header
- keep one intentional change per task
- create or confirm the task before touching code
- write clear, measurable acceptance before implementation starts
- keep the task open until acceptance is satisfied
- move a task to `done` only after acceptance is met and evidence exists
- check feature fit before task creation; create a new feature or split an old one first if the change does not fit exactly
- check decision fit before closeout; create or update a decision first if the work introduced a durable chosen path

Whenever task status changes, state the transition explicitly in user-facing communication.

## Abstraction Hygiene

Run one level check before any feature or decision edit, task creation, or code change:

- project why or success meaning -> `PROJECT_BRIEF.md`
- temporary boundary, prototype constraint, or deferred idea -> `SCOPE.md`
- actor-facing behavior -> feature file
- durable chosen path -> decision file
- shared system shape or flow -> `ARCHITECTURE.md`
- mappings, file layouts, route tables, commands, channel numbers, protocol field maps -> `INTERFACES.md` or `docs/maps/*.md`
- low-level implementation strategy or algorithm detail -> code, tests, or high-level architecture notes only if broadly shared

Exactly one owner should win.

If a statement fits multiple owners, split it.
