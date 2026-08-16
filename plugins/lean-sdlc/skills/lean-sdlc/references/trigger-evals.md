# Trigger and Routing Evaluations

Run these high-risk scenarios from a fresh task with only the installed plugin and target repository visible. The canonical runtime rules live in [subagents.md](subagents.md).

| Scenario | Required behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill. |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly. |
| Repository `AGENTS.md` requires Lean-SDLC for mutation | Trigger the skill before any write. |
| Discussion, proposal, or non-concrete proceed request | Remain read-only and ask for confirmation when authority or the proposal is ambiguous. For an agreed implementation, restate intent and show the visible plan. |
| Brain-dump discussion | Architect restates the understandable Why and What in natural prose, remains read-only, and waits for implementation authority. |
| Clear implementation authority | Confirm why, what, how, and proof in natural prose, show the visible plan, then continue without another round trip. |
| Material ambiguity | Stop for user confirmation when an assumption can affect behavior, scope, or architecture. |
| Behavior-based acceptance | Plan derives observable acceptance from the confirmed outcome and affected value, not only changed files, mechanisms, or test commands. |
| Architect implementation exception | Assisted mode normally delegates routine work; Architect implementation is limited to Solo, the existing mechanical direct path, a small architecture-bearing experiment or inseparable seam, after explicit user direction that the Architect itself implement, or after the required child and fallback are unavailable. Settled separable work remains Engineer work. |
| Session state and lifecycle restoration | Missing or invalid state restores Assisted with Standard children; keep Assisted until Solo. Restore owner, mode, and child tier after startup, resume, clear, or compaction, then reload `subagents.md` before Deliver. |
| Task or implementation request | State outcome, constraints, exclusions, and concise visible plan first. Accept one-item plans when outcome, completion condition, and proof are clear. |
| Valid Engineer checkpoint | Require one ledger task with settled architecture, one coherent outcome, independent bounded proof, and one accept-or-reject review. |
| Oversized task | Split independent behavior, module outcome, proof, or work needing an Architect checkpoint; apply merge and correction rules from [plan.md](plan.md). |
| Any mutation | Create or claim one owned `In Progress` task, then run `lean_check.py --before-write`. |
| Cause lane | Use Diagnose for an unknown failure cause. Use Deliver for a known cause with an owned task and proof. |
| Plausible edge cases | Classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior. |
| Engineer direct path | Use it only for one mechanical bounded change with one narrow proof command. |
| Assisted parallel work | Apply the [universal independence gate](subagents.md) for at most two independent children. Keep shared or uncertain scopes and paired writers serial through integration. |
| Safe Engineer pair | Check all resource-gate fields, separate mutable paths, stable reads, independent proof, and useful elapsed-time reduction. Run Engineer/Engineer only when strict isolation passes; otherwise name the shared resource or dependency and work serially. |
| Overlapping read-only Scouts | Permit Scout/Scout overlap only for independent questions over stable sources. Stop and invalidate findings after a source change. |
| Scout with a sidecar | Allow Scout with one Verifier or Maintainer only for future work with separate resources. |
| Bounded Scout evidence | Use Scout for repo or contract mapping, external research, reproduction or log reduction, change, documentation, or test impact, edge-case or test candidates, and task-size or architecture contradiction review. Avoid trivial one-file lookup; Architect decides. |
| Dependency start block | Reject both claiming Planned work and creating immediate In Progress work when any dependency is unfinished. Return `unfinished dependencies: TASK-X`. |
| Architect writer barrier | The Architect is a writer and never edits child-owned paths. Stop writers before review, shared formatter or generator, documentation, fingerprint, Verifier, or operations. |
| Collision stop | Stop before a shared resource and report the collision and checkpoint. Pause writers if bytes changed; Architect serializes or revises scope, invalidates read findings, and never lets a child integrate sibling work. |
| Custom role request | Require direct user authority before adding the role. |
| Verifier and Maintainer sidecars | Verifier runs acceptance proof and one planned regression command; the full suite runs only when required. Maintainer replays the recorded procedure, and Verifier repeats only disputed operations. |
| Named Architect decision with distinct source sets or enough material, data, or logs to pollute lead context | Reuse or start read-only Scout with citations and conflicts. |
| Reachable role thread | Send a follow-up before replacing the role. |
| Child identity and ownership | The Architect allocates the next unused label and exact `task_name` at spawn. Use one lowercase role prefix and one Greek suffix, such as `task_name=engineer_beta` for Engineer beta. Children never choose or change names. |
| Child visible update | Start with work or current state and use concise natural prose. |
| Handoff | Begin with a short settled purpose, then state outcome, boundary, contract, proof, and stop conditions without a fixed runtime template. |
| Child replacement or pool exhaustion | Reuse one reachable thread per role; allocate the next unused label for replacement. Recycle only unreachable labels after the pool ends. |
| Luna service routing | Standard roles use native `model=gpt-5.6-luna`, `reasoning_effort=max`, non-full-history `fork_turns`, and no `agent_type`; Standard omits `service_tier`. Fast children require explicit opt-in and use `service_tier=priority` only for new or normally replaced children; omission remains valid for a Standard retry. Priority failure retries Luna `max` without it, then Terra `xhigh` without `service_tier` or `agent_type`. Keep Terra and the Architect Standard unless separately overridden, and reject automatic model inheritance. |
| Proof and integration checkpoint | Identify the exact commit or working-tree fingerprint and invalidate it after source changes. Stop children, review scopes, synchronize documents, verify acceptance, and run required operations serially. |
| Stateful operation | Use one exact target and one state change at a time; never guess, silently alter, or retry without authority and recovery. Redact secrets. |
| Task closeout | Verifier returns evidence only; the owning Architect alone decides accept, correct, reopen, fail, or close. |
| Shared interface, schema, manifest, lock file, generated output, or exclusive target | Keep work serial. |
