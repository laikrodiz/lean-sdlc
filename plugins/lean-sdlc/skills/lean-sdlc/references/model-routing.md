# Model Routing

Choose models by ambiguity and failure cost. Count retries, review, and integration in total cost.

## User authority

An explicit user model or reasoning request pins the lead. A request that all work use that model applies to every agent; use Solo mode when the same model cannot be supplied to children. Never silently reduce the requested model or reasoning. Explain any unavailable-model substitution.

Model choice and orchestration mode are independent.

## Profiles

Never use `low` reasoning.

| Work | Required model | Reasoning |
| --- | --- | --- |
| Routing, integration, and ordinary closeout | GPT-5.6 Sol | `medium` |
| Product, scope, architecture, subtle diagnosis, or consequential closeout | GPT-5.6 Sol | `high` |
| Security, concurrency, migrations, irreversible choices, or unusually subtle diagnosis | GPT-5.6 Sol | `xhigh` |
| General implementation or exploration | GPT-5.6 Terra | `high` |

All child profiles, fallbacks, and spawn parameters are defined only in [subagents.md](subagents.md).

## Lane defaults

- Shape: Sol `high`.
- Decide: Sol `high`, or `xhigh` for high-risk irreversible choices.
- Plan: Sol `medium`, or `high` for cross-cutting dependencies.
- Diagnose: Terra `high`; Sol `high/xhigh` owns difficult root-cause decisions.
- Deliver: Terra `high` for general implementation; Sol `high/xhigh` for risky implementation.
- Verify: Sol `medium/high` decides completion; child proof collection follows [subagents.md](subagents.md).
