# Lean-SDLC Delegation Policy

## Purpose

Use sub-agents as a planned execution mode after task truth is clean.

Do not delegate vague work. Do not delegate the whole problem. Do not keep everything local by habit either.

## Delegate Profiles

Use `gpt-5.4-mini` everywhere by default, then choose reasoning effort by task shape:

- `medium` for file inventory, simple search, straightforward trace lookup, and short summaries
- `high` for ordinary analysis, bounded triage, routine worker edits, and most explorer tasks
- `xhigh` for subtle failures, cross-artifact contradictions, architecture tradeoffs, and risky bounded edits

Do not spend `xhigh` on grep-grade work. Do not spend local context on work a mini worker can handle cleanly.

## Agent Types

Use `explorer` for:

- bounded repo questions,
- traceability audits,
- ambiguity checks,
- test-log or failure summarization,
- architecture alternatives.

Use `worker` for:

- bounded implementation with explicit file ownership,
- disjoint test additions,
- isolated doc maintenance,
- independent refactor slices.

## Spawn Triggers

Spawn an `explorer` when:

1. a bounded question can be answered independently,
2. the answer is useful but not on the immediate critical path,
3. a quick parallel read can reduce main-agent context.

Spawn a `worker` when:

1. the write scope is clear and disjoint,
2. the task materially advances the active work,
3. the main agent can continue non-overlapping work while it runs.

## Mandatory Dispatch Rules

1. If one ready task blocks the next main-agent step, do it locally.
2. If two or more ready tasks are disjoint in write scope, spawn workers in parallel.
3. If the work is diagnosis and still unbounded, spawn an explorer before any worker edit.
4. If the ready queue is larger than three disjoint tasks, use batch execution with checkpoints.

## Do Not Spawn When

Do not spawn when:

1. the very next main-agent step is blocked on the result,
2. the task is too vague to assign cleanly,
3. the write scope overlaps heavily with ongoing local work,
4. the task is trivial enough to do faster directly.

## Prompt Shape

Delegation prompts must include:

1. the exact question or deliverable,
2. the ownership boundary,
3. the expected output form,
4. a reminder not to redo unrelated work,
5. a reminder to accommodate concurrent work instead of reverting it.

## Merge Rules

The main agent remains responsible for:

- user dialogue,
- scope control,
- final decisions,
- final integration,
- final parity of docs, tasks, code, tests, and diagnostics.

Delegated output must be reconciled into repository truth in the same session.

After worker output, run a lightweight review pass for:

- acceptance fit
- scope creep
- missing proof
- missing doc parity
