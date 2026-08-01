# Trigger and Routing Evaluations

Run these high-risk scenarios from a fresh task with only the installed plugin and target repository visible. The canonical runtime rules live in [subagents.md](subagents.md).

| Scenario | Required behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill. |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly. |
| Repository `AGENTS.md` requires Lean-SDLC for mutation | Trigger the skill before any write. |
| Discussion or proposal request | Remain read-only. |
| Ambiguous implementation authority | Remain read-only and request confirmation. |
| “I am thinking about X; what do you think?” | Stay read-only. |
| “Implement the agreed X proposal” | Restate intent and show the visible plan before task creation. |
| “Proceed” with no recoverable proposal | Stay read-only and request a concrete implementation instruction. |
| Task creation or implementation request | State outcome, constraints, exclusions, and concise visible plan first. |
| One-item visible plan | Accept it when outcome, completion condition, and proof are clear. |
| Any mutation | Create or claim one owned `In Progress` task, then run `lean_check.py --before-write`. |
| Unknown failure cause | Use Diagnose. |
| Known cause with an owned task and proof | Use Deliver. |
| Plausible edge cases | Classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant` before choosing behavior. |
| Engineer direct path | Use it only for one mechanical bounded change with one narrow proof command. |
| Triggered Assisted child with two independent scopes | Apply the [universal independence gate](subagents.md); allow at most two active children for Engineer/Engineer, Engineer/Scout, or Scout/Scout pairs. |
| Scout with a sidecar | Allow Scout with one Verifier or Maintainer only for future work with separate resources. |
| Shared scope, dependency, or uncertain time reduction | Schedule children serially and ask the Architect when needed. |
| Paired writers | Stop writers before integration; documentation synchronization, verification, and stateful operations remain serial. |
| Custom role request | Require direct user authority before adding the role. |
| Verifier trigger | Run acceptance proof and one planned regression command. |
| Full suite | Run it once only when the task or repository contract requires it. |
| Maintainer trigger | Replay the recorded procedure once and return bounded evidence. |
| Verifier receives Maintainer evidence | Consume it and repeat only a disputed operation. |
| Named Architect decision with distinct source sets or enough material, data, or logs to pollute lead context | Reuse or start read-only Scout with citations and conflicts. |
| Reachable role thread | Send a follow-up before replacing the role. |
| Standard child identity | Allocate the next unused canonical label; display `Role label` and use `role_label`. |
| Child visible update | Start with work or current state and use concise natural prose. |
| Handoff | State outcome, boundary, contract, proof, and stop conditions without a fixed runtime template. |
| Child replacement or pool exhaustion | Reuse one reachable thread per role; allocate the next unused label for replacement. Recycle only unreachable labels after the pool ends. |
| Primary Luna spawn | Use `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history `fork_turns`. |
| Luna priority failure | Retry Luna `max` without `service_tier`; then directly spawn Terra `xhigh` without `service_tier` or `agent_type`. |
| Child route inherits an automatic model | Fail the route; use the named profile or explicit Terra `xhigh` fallback. |
| Silent command | Retain at most two useful Luna heartbeats at two-minute intervals. |
| Proof or operation checkpoint | Identify the exact commit or working-tree fingerprint; invalidate evidence after relevant source changes. |
| Stateful operation | Use one exact target and one state change at a time; never guess, silently alter, or retry without authority and recovery. Redact secrets. |
| Task closeout | Verifier returns evidence only; the owning Architect alone decides accept, correct, reopen, fail, or close. |
| Checkpoint | Stop all active work children before integration, review scopes, synchronize shared documentation, verify acceptance sets, then run required operations serially. |
| Shared interface, schema, manifest, lock file, generated output, or exclusive target | Keep work serial. |
| Solo mode with parallel-ready work | Keep execution lead-only and preserve existing Solo gates. |
