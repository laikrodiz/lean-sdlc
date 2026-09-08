---
name: lean-sdlc
description: Use Lean-SDLC when explicitly requested or required by repository instructions. Support conversation and planning without writes; implement authorized work through owned tasks, focused support roles, and evidence-based completion.
---

# Lean-SDLC

Use one workflow. Lead implements; Scout researches; Maintainer manages tasks, shared documentation, and authorized recorded operations; Verifier runs tests.

Interpret the request before loading execution details. Conversation, brainstorming, diagnosis, and planning do not imply implementation authority. Read-only requests create no tasks or project files.

## Read only what applies

- Conversation, brainstorming, shaping, or read-only investigation: [conversation](references/conversation.md).
- Planning: [plan](references/plan.md). A plan-only request stops after the plan.
- Authorized execution: [common](protocols/common.md), [Lead](protocols/lead.md), and [plan](references/plan.md).
- Assigned support: [common](protocols/common.md) and only [Scout](protocols/scout.md), [Maintainer](protocols/maintainer.md), or [Verifier](protocols/verifier.md).
- Ledger operations, initialization, or upgrade: [ledger](references/ledger.md).
- Shared-document work: [documentation](references/documentation.md).
- Recorded delivery operations: [operations](references/operations.md).

Read selected files completely. Do not follow every link. Reuse unchanged instructions already loaded. After compaction, reload this entry and the applicable role or request instructions, then recover current authority and unresolved work.

For an authorized new project, follow [ledger initialization](references/ledger.md#initialization-and-upgrade) before requesting startup context.

For execution, use exact repository, skill, helper, owner, and child-tier fields from startup context. If missing, run `python3 "<directory containing this SKILL.md>/scripts/session_state.py" --context` from the selected repository. Preserve `CODEX_SESSION_ID`; never invent paths or owners. Conversation needs no helper discovery.

[Plan](references/plan.md) owns the visible plan and task gates. [Common](protocols/common.md) owns assignments and role boundaries. Optional documents do not create additional workflow stages.
