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
| Narrow mechanical implementation with exact proof | GPT-5.6 Luna | `xhigh` |
| Verifier and Operator sidecars | GPT-5.6 Luna | `xhigh` |

When Luna is unavailable, explicitly use Terra `high`. When a temporary task needs broader engineering judgment, use Terra `high` from the start. Use only models exposed by the current surface.

## Spawn contract

Before every spawn:

1. Apply explicit user model authority, then resolve the role profile against models exposed by the spawn surface.
2. Pass the model and reasoning effort explicitly. For collaboration `spawn_agent`, set `model` and `reasoning_effort`; never omit either or rely on parent, configured, or automatic defaults.
3. Set `fork_turns` to `none` or a bounded positive count so the explicit profile can apply. Never use or imply full-history inheritance for a routed child.
4. If neither the required model nor its documented fallback is exposed, keep the work with the lead or use Solo mode.

An omitted model, omitted reasoning effort, inherited lead profile, or incompatible full-history fork is a routing failure.

## Lane defaults

- Shape: Sol `high`.
- Decide: Sol `high`, or `xhigh` for high-risk irreversible choices.
- Plan: Sol `medium`, or `high` for cross-cutting dependencies.
- Diagnose: Terra `high`; Sol `high/xhigh` owns difficult root-cause decisions.
- Deliver: Terra `high`; Luna `xhigh` for exact mechanical changes; Sol for risky implementation.
- Verify: Luna `xhigh` or Terra `high` collects proof; Sol `medium/high` decides completion.

Keep stable role instructions unchanged within an active task. Put volatile task data last to support prompt-cache reuse, but never create work or preserve stale context merely for a possible cache hit.
