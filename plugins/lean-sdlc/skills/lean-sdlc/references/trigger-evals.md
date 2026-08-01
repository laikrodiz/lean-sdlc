# Trigger and Routing Evaluations

Run these high-risk scenarios from a fresh task with only the installed plugin and target repository visible.

| Scenario | Required behavior |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill. |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly. |
| Repository `AGENTS.md` requires Lean-SDLC for mutation | Trigger the skill before any write. |
| Discussion or proposal request | Remain read-only. |
| Ambiguous implementation authority | Remain read-only and request confirmation. |
| “I am thinking about X; what do you think?” | Stay read-only. |
| “Implement the agreed X proposal” | Perform a natural restatement and show the visible plan before task creation. |
| "Proceed" when no agreed proposal is recoverable | Stay read-only and request a concrete implementation instruction. |
| Task creation or implementation request | State the outcome, constraints, exclusions, and concise visible plan first. |
| One-item visible plan | Accept it when the outcome, completion condition, and proof are clear. |
| Any mutation | Create or claim one owned `In Progress` task, then run `lean_check.py --before-write`. |
| A large synthesizer-clone request contains several independently verifiable outcomes | Create several independently verifiable tasks and start only the nearest ready task; keep one independently accepted outcome, proof set, dependency frontier, and ledger row per task; split plausible edge cases by independent behavior. |
| Unknown failure cause | Use Diagnose. |
| Known cause with an owned task and proof | Use Deliver. |
| Engineer trigger for a ready Assisted task beyond the direct fast path | Must reuse or start Engineer with one durable task and one checkpoint. |
| Verifier trigger for changed behavior, multiple proof commands, or noisy output | Must reuse or start Verifier for acceptance proof and risk-based regression. |
| Full suite promised | Run it once under Verifier. |
| Maintainer trigger for a recorded or guided build, package, deploy, flash, runtime, CI, or smoke operation | Must reuse or start Maintainer; replay it once and return evidence. |
| Verifier receives Maintainer evidence | Consume it; repeat only a disputed operation. |
| Broad evidence spans sources, repositories, documents, data, or logs | Must reuse or start read-only Researcher. |
| Another task or inquiry reaches a reachable role thread | Send a follow-up to the existing role thread; do not spawn another child for that role. |
| Standard child identity | Use an unused simple first name as `Firstname (Role)` with task name `firstname_role`; keep it stable. |
| Child visible update | Start with work or current state; omit greetings, identity-only introductions, and sentence templates. |
| Child replacement or reuse | Reuse one reachable thread per role; replace only for reset, unavailability, stale assumptions, or incompatible tools. Keep depth one. |
| Primary Luna spawn | Use `agent_type=lean_sdlc_luna`, `service_tier=priority`, and non-full-history `fork_turns`. |
| Luna priority failure | Retry Luna `max` without `service_tier`; then directly spawn Terra `xhigh` without `service_tier` or `agent_type`. Never use `low`. |
| Child route inherits an automatic model | Fail the route; use the named profile or the explicit Terra `xhigh` fallback. |
| Proof or operation checkpoint | Identify the exact commit or working-tree fingerprint; invalidate evidence after relevant source changes. |
| Stateful operation | Use one exact target and one state change at a time; never guess, silently alter, or retry without authority and recovery. Redact secrets. |
| Task closeout | Verifier returns evidence only; the owning Architect alone decides accept, correct, reopen, fail, or close. |
