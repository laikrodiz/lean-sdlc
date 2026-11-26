---
name: lean-sdlc
description: Use Lean-SDLC when explicitly requested or required by repository instructions. Before inspecting the project, delegating, or creating tasks, Lead explains who needs what, why, and what must stay true. For one small fix, open with one sentence naming the user-visible change and its check. Continue unless blocked.
---

# Lean-SDLC

Lead owns delivery and works sequentially in the current checkout by default. Use Scout for substantial uncertainty, Maintainer for substantive shared docs, and Verifier for independent proof.

Read-only requests create no tasks or files. Discussion, diagnosis, and planning never authorize implementation.

If Ponytail is already active during implementation, apply its minimalism and reuse rules. Never activate, install, or wait for it. Lean-SDLC controls scope, authority, delegation, task records, proof, and handoff.

If a user decision blocks progress, open with the choice, recommendation, and consequence.

When evidence strength affects safety, root cause, acceptance, or a dispute, label the claim: 1 asserted; 2 cited; 3 traced; 4 executed in a test; 5 reproduced on the running target. State the limit. A level describes evidence, not acceptance or business benefit. Never run unsafe checks to raise it.

On first project contact, after restating intent, read `docs/PROJECT.md` first. Follow only the topic relevant to the request. Use named files, symbols and tests to explore how. If no source records why, say unknown; do not turn an inference into project policy.

## Read only what applies

- Discussion or investigation: [conversation](references/conversation.md).
- Requested storage review: [Storage Review](references/storage-review.md), even without initialization.
- Planning only: [plan](references/plan.md), then stop.
- One settled, reversible local repair: use [ordinary fix](references/ordinary.md) alone. Before changing saved data, a public contract, permissions or shared state, switch to the full execution path. For data changes trace existing readers, persisted formats and recovery before editing.
- Other authorized execution: [common](protocols/common.md), [Lead](protocols/lead.md), and [plan](references/plan.md).
- User requests or offers parallel Engineers: [isolated assignments](protocols/parallel.md).
- Lead assigning or resuming support: [delegation](protocols/delegation.md).
- Assigned support: [common](protocols/common.md) and only [Scout](protocols/scout.md), [Maintainer](protocols/maintainer.md), or [Verifier](protocols/verifier.md).
- Non-routine ledger operations, initialization, or upgrade: [ledger](references/ledger.md).
- Shared-document work: [documentation](references/documentation.md).
- Recorded delivery operations: [operations](references/operations.md).

Read selected files completely; reuse unchanged instructions. After compaction, reload this entry and applicable rules. Recover authority, open work, grades and reasons, assignments, and proof validity. Historical status never authorizes resumption.

For authorized new projects, [initialize](references/ledger.md#initialization-and-upgrade) before requesting startup context.

If an installed helper file disappears, pause edits. Run `codex plugin list --marketplace lean-sdlc --json`. Require one installed, enabled `lean-sdlc@lean-sdlc` with a numeric dotted release version. Under the previous plugin cache parent, use only that version's directory. Verify its manifest name and version before running code. Reject redirected paths. Read the replacement skill's [recovery steps](references/ledger.md#missing-installed-helper). If uncertain, stop. Other failures do not trigger lookup.

For execution, use exact startup repository, skill, helpers, owner, and child tier. If absent, run `python3 "<directory containing this SKILL.md>/scripts/session_state.py" --context` from the selected repository. Preserve `CODEX_SESSION_ID`; never invent paths or owners. If context is still missing, stop. Report the missing field, not its value. Never enumerate environment variables to recover context.
