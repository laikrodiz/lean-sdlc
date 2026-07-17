# Architecture Workflow

Use only after behavior and scope are stable. Architecture owns technical choices, boundaries, and durable consequences; return to refinement when the real uncertainty concerns behavior or value.

Use Sol at `high`. Raise to `xhigh` for security boundaries, concurrency, data migrations, or expensive irreversible choices. Terra may gather bounded option evidence.

## Workflow

1. Read the brief, scope, and active features.
2. Identify choices that are irreversible, costly, or likely to be re-litigated.
3. Choose the simplest stack fitting deployment, operator skill, testability, diagnostics, maturity, and maintenance cost.
4. Define only the modules and boundaries needed for safe implementation.
5. Record major decisions with context and consequences.
6. Put shared mappings, commands, and protocol fields in interfaces or mapping docs.
7. Establish shared proof and diagnostics policy only when it crosses several features.
8. Keep architecture separate from feature behavior and low-level recipes.

Prefer hard cuts over compatibility wrappers unless compatibility is an explicit requirement. Avoid speculative layers and fashionable stack choices without repository pressure.

Success means implementation can proceed from a small defensible technical shape without hidden architectural decisions.
