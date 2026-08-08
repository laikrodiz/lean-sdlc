# Trigger and Routing Evaluations

Run these high-risk scenarios from a fresh task with only the installed plugin and target repository visible. The canonical runtime rules live in [subagents.md](subagents.md).

| Scenario | Required behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill. |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly. |
| Repository `AGENTS.md` requires Lean-SDLC for mutation | Trigger the skill before any write. |
| Discussion, proposal, or non-concrete proceed request | Remain read-only and ask for confirmation when authority or the proposal is ambiguous. For an agreed implementation, restate intent and show the visible plan. |
| Session state and lifecycle restoration | Missing or invalid state restores Assisted with Standard children; keep Assisted until Solo. Restore owner, mode, and child tier after startup, resume, clear, or compaction, then reload `subagents.md` before Deliver. |
| Task or implementation request | State outcome, constraints, exclusions, and concise visible plan first. Accept one-item plans when outcome, completion condition, and proof are clear. |
| Valid Engineer checkpoint | Require one ledger task with settled architecture, one coherent outcome, independent bounded proof, and one accept-or-reject review. |
| Oversized task | Split independent behavior, module outcome, proof, or work needing an Architect checkpoint; apply merge and correction rules from [plan.md](plan.md). |
| Any mutation | Create or claim one owned `In Progress` task, then run `lean_check.py --before-write`. |
| Cause lane | Use Diagnose for an unknown failure cause. Use Deliver for a known cause with an owned task and proof. |
| Plausible edge cases | Classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior. |
| Engineer direct path | Use it only for one mechanical bounded change with one narrow proof command. |
| Assisted parallel work | Apply the [universal independence gate](subagents.md) for at most two independent children. Keep shared or uncertain scopes and paired writers serial through integration. |
| Scout with a sidecar | Allow Scout with one Verifier or Maintainer only for future work with separate resources. |
| Custom role request | Require direct user authority before adding the role. |
| Verifier and Maintainer sidecars | Verifier runs acceptance proof and one planned regression command; the full suite runs only when required. Maintainer replays the recorded procedure, and Verifier repeats only disputed operations. |
| Named Architect decision with distinct source sets or enough material, data, or logs to pollute lead context | Reuse or start read-only Scout with citations and conflicts. |
| Reachable role thread | Send a follow-up before replacing the role. |
| Child identity and ownership | The Architect allocates the next unused label and exact `task_name` at spawn. Use one lowercase role prefix and one Greek suffix, such as `task_name=engineer_beta` for Engineer beta. Children never choose or change names. |
| Child visible update | Start with work or current state and use concise natural prose. |
| Handoff | State outcome, boundary, contract, proof, and stop conditions without a fixed runtime template. |
| Child replacement or pool exhaustion | Reuse one reachable thread per role; allocate the next unused label for replacement. Recycle only unreachable labels after the pool ends. |
| Luna service routing | Normal Luna uses `agent_type=lean_sdlc_luna`, omits `service_tier`, and sets non-full-history `fork_turns`. Fast children require explicit opt-in and use `service_tier=priority` only for new or normally replaced children; reachable threads remain. Standard retry omits `service_tier`; priority failure retries Luna `max` without it, then Terra `xhigh` without `service_tier` or `agent_type`. Keep Terra and the Architect Standard unless separately overridden, and reject automatic model inheritance. |
| Proof and integration checkpoint | Identify the exact commit or working-tree fingerprint and invalidate it after source changes. Stop children, review scopes, synchronize documents, verify acceptance, and run required operations serially. |
| Stateful operation | Use one exact target and one state change at a time; never guess, silently alter, or retry without authority and recovery. Redact secrets. |
| Task closeout | Verifier returns evidence only; the owning Architect alone decides accept, correct, reopen, fail, or close. |
| Shared interface, schema, manifest, lock file, generated output, or exclusive target | Keep work serial. |
