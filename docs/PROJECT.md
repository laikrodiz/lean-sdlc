# Project

## Purpose

Lean-SDLC helps people use Codex to make repository changes without losing the reason for the work, the owner, or proof of the result. It turns an authorized request into work that the user can review and accept.

## Scope

Lean-SDLC has one workflow. Discussion, investigation, and plan-only requests do not change files or create tasks. Authorized implementation uses one task at a time by default. The Lead owns the result and makes the final decisions. Support is conditional and sequential. See the [plan rules](../plugins/lean-sdlc/skills/lean-sdlc/references/plan.md) and [role rules](../plugins/lean-sdlc/skills/lean-sdlc/protocols/common.md).

The user chooses the Lead model and tier. Scout, Maintainer, and Verifier use `gpt-6.2-sol` with Medium reasoning. Priority service for support requires user opt-in and host support. If Sol is unavailable, the Lead reports the blocker and does not switch models.

The user can opt in to Parallel Engineers for the current request only. Engineers use the Lead model and reasoning effort in separate checkouts. The Lead limits concurrency to useful independent work within the requested count and available resources. Queued tasks start only when a slot and their accepted inputs are available. See the [parallel rules](../plugins/lean-sdlc/skills/lean-sdlc/protocols/parallel.md).

Hosted task services, dashboards, telemetry, and automatic discovery or proposal of reusable procedures are outside scope. A new reusable script requires a user request.

## Constraints

- Keep tools portable. Use the shell and the Python standard library.
- Keep `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`. The task ledger records ownership, dependencies, and accepted results. Before changing project files, confirm task ownership and the required check. Assign one writer per file or external target. See the [ledger rules](../plugins/lean-sdlc/skills/lean-sdlc/references/ledger.md) for the initialization exception and transaction rules.
- Preserve project documents, custom rules, task history, owners, evidence, preferences, and stopped work during upgrades. Report conflicts before making changes. Keep additional documents only when their subject needs durable detail. See the [documentation rules](../plugins/lean-sdlc/skills/lean-sdlc/references/documentation.md).
- Require authority for the exact delivery action and target. Recorded procedures require explicit targets, accepted source identity, safe recovery, and redacted output. See the [operations rules](../plugins/lean-sdlc/skills/lean-sdlc/references/operations.md).
- The Lead alone integrates parallel changes. If a push is authorized, push the accepted destination once and never publish Engineer branches. Remove only recorded temporary checkouts after their processes stop and their results are retained. Preserve dirty, canceled, disputed, or unverified work.

## Success

- Read-only requests leave the repository unchanged. Authorized work stays within the user's limits.
- Each task has one outcome, an owner when work starts, clear completion criteria, and checks that match the outcome. Dependencies are valid, and the reported state matches the ledger.
- Accepted evidence covers the request, including essential safety proof and affected documentation. The Lead reuses valid evidence and examines gaps or exceptions. If required proof is missing, the task stays open. Report unmeasured effects as unproven.
- Checks of individual parallel tasks do not replace checks of the combined result. The Lead checks the combined result before delivery.
- Supported upgrades preserve project history and rules. Canceled work does not release its target until the underlying process stops.

## Current stage and version

- Stage: Evolution.
- Version: 1.40.0.
- Version goal: Reduce instruction overhead and match planning, implementation checks, and evidence claims to the actual request.
- Exit evidence: Require fresh [candidate checks](OPERATIONS.md), version checks, exact remote commit and tag on `origin/main`, and byte-for-byte installed/source equality. Confirm selected-repository isolation, upgrade and structural checks, a live support-profile check, and final ledger reconciliation.
