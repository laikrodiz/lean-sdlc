---
name: lean-sdlc
description: Use Lean-SDLC when explicitly requested or required by repository instructions. Support conversation and planning without writes; implement authorized work through owned tasks, focused support roles, and evidence-based completion.
---

# Lean-SDLC

Lead owns delivery and implements sequentially in the current checkout by default. Use Scout for substantial uncertainty, Maintainer for substantive shared docs, and Verifier for independent proof.

Conversation, diagnosis, and planning do not authorize implementation. Read-only requests create no tasks or files.

## Read only what applies

- Discussion or investigation: [conversation](references/conversation.md).
- Requested storage review: [Storage Review](references/storage-review.md), even without initialization.
- Planning only: [plan](references/plan.md), then stop.
- Authorized execution: [common](protocols/common.md), [Lead](protocols/lead.md), and [plan](references/plan.md).
- User requests or offers parallel Engineers: [isolated assignments](protocols/parallel.md).
- Assigned support: [common](protocols/common.md) and only [Scout](protocols/scout.md), [Maintainer](protocols/maintainer.md), or [Verifier](protocols/verifier.md).
- Ledger operations, initialization, or upgrade: [ledger](references/ledger.md).
- Shared-document work: [documentation](references/documentation.md).
- Recorded delivery operations: [operations](references/operations.md).

Read selected files completely; reuse unchanged instructions. After compaction, reload this entry and applicable protocols; recover authority and unresolved work.

For authorized new projects, [initialize](references/ledger.md#initialization-and-upgrade) before requesting startup context.

For execution, use exact startup repository, skill, helpers, owner, and child tier. If absent, run `python3 "<directory containing this SKILL.md>/scripts/session_state.py" --context` from the selected repository. Preserve `CODEX_SESSION_ID`; never invent paths or owners.
