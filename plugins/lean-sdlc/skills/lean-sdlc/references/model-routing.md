# Model Routing

Choose models by ambiguity and failure cost. Count retries, review, and integration in total cost.

## User authority

An explicit user model or reasoning request pins the lead. The workflow never replaces that lead or delegates its decision authority. A request that all work use the selected profile applies to every agent; use Solo mode when the same profile cannot be supplied to children. Never silently reduce the requested model or reasoning. Explain any unavailable-model substitution.

Model choice and orchestration mode are independent.

## Lead profiles

Never use `low` reasoning.

| Decision work | Default lead profile |
| --- | --- | --- |
| Routine routing, planning, integration, and closeout | User-selected lead; otherwise GPT-5.6 Sol `high` |
| Product, scope, architecture, subtle diagnosis, or consequential closeout | User-selected lead; otherwise GPT-5.6 Sol `high` |
| Security, concurrency, migrations, irreversible choices, or unusually subtle diagnosis | User-selected lead; otherwise GPT-5.6 Sol `xhigh` or `max` |

All child profiles, fallbacks, and spawn parameters are defined only in [subagents.md](subagents.md).

## Lane defaults

- Shape: lead.
- Decide: lead.
- Plan: lead.
- Diagnose: lead owns causal and repair decisions; bounded evidence collection may use a child.
- Deliver: lead defines and accepts each execution unit; execution follows [subagents.md](subagents.md).
- Verify: lead decides completion; child proof collection follows [subagents.md](subagents.md).
