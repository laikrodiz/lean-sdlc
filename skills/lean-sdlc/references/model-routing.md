# Model and Delegation Routing

Choose models by the work's failure cost and ambiguity. Optimize total cost, including retries and review, rather than token price alone.

## Baseline Roles

| Work | Model | Reasoning |
| --- | --- | --- |
| Main coordination, repository routing, and integration | `gpt-5.6-sol` | `medium` |
| High-leverage product, scope, architecture, root-cause, version, or closeout decisions | `gpt-5.6-sol` | `high` |
| Security, concurrency, migration, irreversible architecture, or unusually subtle diagnosis | `gpt-5.6-sol` | `xhigh` |
| Ordinary scoped engineering, exploration, tests, refactoring, and semantic documentation work | `gpt-5.6-terra` | `medium` or `high` |
| Exact mechanical edits, inventories, extraction, test execution, and concise summaries | `gpt-5.6-luna` | `low` or `medium` |

Start mechanical work at `low`. Do not spend `xhigh` on simple work. Luna at `xhigh` is an experimental exception for a narrow, repeatable transformation with exact ownership and strong automated proof; prefer Terra `high` when the task is genuinely difficult.

Use only models exposed by the current Codex surface. If Luna is unavailable, use Terra at the lowest safe effort. If a requested model is unavailable, preserve the work class and explain the substitution; never silently fall back to an older generation.

## Workflow Defaults

| Workflow | Default | Escalate when |
| --- | --- | --- |
| Router or bootstrap | Sol `medium` | Sol `low` is sufficient only when state is obvious |
| Brainstorm | Sol `high` | Use `xhigh` only for unusually high-stakes framing |
| Refine | Sol `high` | Use Terra for bounded contradiction inventory |
| Architecture | Sol `high` | Use `xhigh` for security, concurrency, migrations, or expensive irreversible choices |
| Task planning | Sol `medium` | Use `high` for cross-cutting dependencies; Luna may write an agreed CSV |
| Execution routing | Terra `medium` or Sol `low` | Escalate only if ownership or integration risk is unclear |
| Debugging | Terra `high` for ordinary faults | Luna collects evidence; Sol `high/xhigh` classifies subtle root causes |
| Implementation | Terra `high` | Luna `low/medium` for exact edits; Sol `high/xhigh` for risky or complex code |
| Verification | Luna `low` collects proof | Terra interprets failures; Sol `medium/high` decides close, fail, or reopen |
| Traceability | Terra `medium` inventories links | Sol `medium/high` resolves contradictory truth |
| Versioning | Sol `high` | Escalate only when the business choice is unusually consequential |
| Documentation maintenance | Luna `low` for exact synchronization | Terra `high` for semantic cleanup; Sol when meaning changes |

## Delegation Gate

Delegate only when parallel work saves meaningful wall time or keeps substantial supporting context out of the main agent.

Keep work local when:

1. the next main step blocks on the result,
2. the task is a quick read or one-step edit,
3. ownership overlaps current work,
4. explaining and rechecking costs about as much as doing it,
5. the task still contains a decision the main agent must make.

Use explorers for bounded evidence collection. Use workers for approved execution with disjoint ownership. Keep user dialogue, scope, decisions, integration, and closeout with the main agent.

Every assignment must state the exact deliverable, owned paths, acceptance, proof command, forbidden unrelated work, and a concise return contract. Give the smallest useful context. Review all output for acceptance fit, scope creep, evidence, and documentation parity.
