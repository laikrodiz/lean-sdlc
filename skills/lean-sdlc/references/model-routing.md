# Model Routing

Choose models by failure cost and ambiguity. Optimize total cost, including retries, review, and integration.

## User Authority

Explicit user model and reasoning requests override automatic routing.

Use these modes:

- `strict`: keep the selected model and reasoning level for the complete task; do not delegate unless the user asks. Requested workers inherit that model and reasoning level unless the user approves another route.
- `lead`: keep the selected model for decisions, integration, verification, and final output; allow cheaper workers only for bounded support.
- `economy`: route automatically across Sol, Terra, and Luna.

When the user names a model or reasoning level without granting delegation, use `strict`. Treat Max as `strict` by default. Treat Ultra or an explicit request for parallel agents as permission for multi-agent work. Never silently lower an explicit model or reasoning request. If the requested model is unavailable, stop and explain the closest available options.

The main agent keeps the selected model throughout the turn. A different model requires a subagent. Same-model workers are also allowed when the user requests them or automatic routing permits them, subject to [agent-coordination.md](agent-coordination.md).

## Baseline Roles

| Work | Model | Reasoning |
| --- | --- | --- |
| Main coordination, repository routing, and integration | `gpt-5.6-sol` | `medium` |
| High-leverage product, scope, architecture, root-cause, version, or closeout decisions | `gpt-5.6-sol` | `high` |
| Security, concurrency, migration, irreversible architecture, or unusually subtle diagnosis | `gpt-5.6-sol` | `xhigh` |
| Ordinary scoped engineering, exploration, tests, refactoring, and semantic documentation | `gpt-5.6-terra` | `medium` or `high` |
| Exact mechanical edits, inventories, extraction, test execution, and concise summaries | `gpt-5.6-luna` | `low` or `medium` |

Start mechanical work at `low`. Do not spend `xhigh` on simple work. Prefer Terra `high` when a task is difficult enough to require substantial reasoning. Use Luna `xhigh` only for a benchmarked, narrow transformation with exact ownership and strong automated proof.

Use only models exposed by the current Codex surface. When automatic routing is allowed and Luna is unavailable, use Terra at the lowest safe effort. Preserve the work class and disclose substitutions.

## Workflow Defaults

| Workflow | Default | Escalate when |
| --- | --- | --- |
| Router or bootstrap | Sol `medium` | Sol `low` is sufficient only when state is obvious |
| Brainstorm | Sol `high` | Use `xhigh` only for unusually high-stakes framing |
| Refine | Sol `high` | Use Terra for bounded contradiction inventory |
| Architecture | Sol `high` | Use `xhigh` for security, concurrency, migrations, or expensive irreversible choices |
| Task planning | Sol `medium` | Use `high` for cross-cutting dependencies; Luna may write an agreed CSV |
| Execution routing | Terra `medium` or Sol `low` | Escalate when ownership or integration risk is unclear |
| Debugging | Terra `high` for ordinary faults | Luna collects evidence; Sol `high/xhigh` classifies subtle root causes |
| Implementation | Terra `high` | Luna `low/medium` for exact edits; Sol `high/xhigh` for risky or complex code |
| Verification | Luna `low` collects proof | Terra interprets failures; Sol `medium/high` decides close, fail, or reopen |
| Traceability | Terra `medium` inventories links | Sol `medium/high` resolves contradictory truth |
| Versioning | Sol `high` | Escalate only when the business choice is unusually consequential |
| Documentation maintenance | Luna `low` for exact synchronization | Terra `high` for semantic cleanup; Sol when meaning changes |
