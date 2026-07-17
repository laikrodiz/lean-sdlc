# Lean-SDLC Delegation Policy

Use sub-agents only after the task, ownership boundary, and proof target are clear.

## Model Profiles

| Work | Model | Effort |
| --- | --- | --- |
| Planning, architecture, task slicing, root-cause classification, reconciliation, and final verification decisions | `gpt-5.6-sol` | `low` by default; raise to `high` or `xhigh` only for material ambiguity or risk |
| Bounded implementation with exact acceptance, owned files, and a proof path | `gpt-5.6-luna` | `xhigh` |
| Mechanical search, inventory, extraction, and concise summaries | `gpt-5.6-luna` | `low` |

Never select `none` or `minimal`. Keep `low` as the minimum effort.

Sol owns decisions. Luna executes clear, repeatable work. Luna must not own scope, architecture, root-cause classification, acceptance changes, or final closeout.

Before dispatch, use only models exposed by the current Codex surface. When Luna is unavailable, use `gpt-5.6-terra` at the same effort. When neither Luna nor Terra is available, use the current GPT-5.6 model at the lowest safe effort or keep the work local. Never fall back to an older model silently.

## Cost Gate

Delegate only when parallel work saves meaningful wall time or keeps substantial supporting context out of the main agent.

Keep work local when:

1. the next main step blocks on the result,
2. the task is a quick read or one-step edit,
3. ownership overlaps current work,
4. explaining and rechecking the task costs as much as doing it,
5. the task still contains a decision the main agent must make.

Several disjoint tasks make delegation possible. They do not make it mandatory.

## Agent Roles

Use an explorer for bounded evidence collection: repository questions, trace inventory, logs, ambiguity scans, or option research.

Use a worker for bounded execution: implementation, tests, isolated documentation edits, or independent refactor slices.

The main agent keeps user dialogue, scope, decisions, integration, and closeout.

## Context Budget

Give each delegate the smallest useful context:

1. Prefer no history or the smallest recent-turn fork supported by the current surface.
2. Pass the exact task, owned paths, acceptance, proof command, and relevant source files.
3. Avoid copying the complete project history or every Lean-SDLC document.
4. Reuse an existing delegate for corrections when practical instead of spawning a replacement.

## Assignment Contract

Every assignment must state:

1. exact deliverable,
2. owned files or read boundary,
3. acceptance and proof expectations,
4. forbidden unrelated work,
5. required concise return: result, changed files, evidence, and blockers.

## Integration

Review delegate output for acceptance fit, scope creep, proof, and documentation parity. Reconcile accepted output into repository truth before closeout.
