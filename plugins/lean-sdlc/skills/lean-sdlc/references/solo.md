# Solo Mode

Solo is lead-only. The Architect performs implementation, tests, decisions, acceptance, and integration under the same task and proof gates.

Load [mode-common.md](mode-common.md) and this file. Do not load [delegating.md](delegating.md) or [assisted.md](assisted.md). Child routing rules do not apply.

## Lead process

1. Establish the current outcome, allowed changes, required proof, and stopping condition.
2. Start or claim one independently acceptable task under the shared gates. Explain the design once before implementation.
3. Read affected code and callers, then implement and correct defects within the owned boundary.
4. Assess current changes and evidence. Apply [verify.md](verify.md), then accept and close when requirements pass.

Use [shape.md](shape.md), [decide.md](decide.md), [plan.md](plan.md), [diagnose.md](diagnose.md), [deliver.md](deliver.md), [verify.md](verify.md), and [operations.md](operations.md) only when their lanes apply.

Critical work cannot self-certify. If independent evidence is required, request explicit authorization for a reviewer or a mode change in this session. Do not spawn a reviewer automatically. Do not silently change mode or lower the selected model or effort.

Use the shared lifecycle, cancellation, evidence, and truthful-delivery rules in [mode-common.md](mode-common.md).
