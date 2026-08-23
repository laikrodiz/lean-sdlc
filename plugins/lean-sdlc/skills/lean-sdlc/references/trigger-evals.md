# Trigger and Routing Evaluations

These rows are scenarios and assertions. They are not a second policy source. The canonical lifecycle is in [SKILL.md](../SKILL.md), role routing is in [subagents.md](subagents.md), and proof and operation rules are in [verify.md](verify.md) and [operations.md](operations.md).

Run these scenarios from a fresh task with only the installed plugin and target repository visible.

| Scenario | Assertion |
| --- | --- |
| Explicit `$lean-sdlc` or “Lean-SDLC” | Trigger the skill. |
| Read-only work outside a Lean-SDLC repository | Do not trigger implicitly. |
| Repository `AGENTS.md` requires Lean-SDLC for mutation | Trigger before any write. |
| Discussion, proposal, or non-concrete proceed request | Remain read-only until authority and intent are clear. |
| Brain-dump discussion | Architect restates the understandable Why and What in natural prose, creates no task or plan view, and waits for authority. |
| Clear implementation authority | Confirm why, what, how, and proof, then show the visible plan. |
| Material ambiguity | Stop for user confirmation when behavior, scope, or architecture may change. |
| Behavior-based acceptance | Derive acceptance from observable outcome and affected value. |
| Canonical lifecycle | Follow the six lanes in [SKILL.md](../SKILL.md); Diagnose is conditional and Verify includes closeout. |
| Session state and lifecycle restoration | Restore owner, mode, tier, and unresolved work; silence alone is not failure. |
| Task or implementation request | Show constraints, exclusions, visible plan, owned task, and before-write proof. |
| Backlog addition | Add or promote Backlog only after a direct user request. |
| Optional project documentation | Keep `docs/PROJECT.md` mandatory; create other documents only from concrete triggers. |
| Source replacement or archive request | Use Git by default; create root `archive/` only after explicit user authority. |
| Role-routing precedence | Apply the stage-aware chain in [subagents.md](subagents.md); unresolved decisions stay with Architect and shared resources stay serial. |
| Pre-handoff design brief | Show reason, selected decision, affected ownership/interfaces/invariants, useful rejected option, child limits, acceptance, proof, and stop. Never expose chain-of-thought. |
| Valid Engineer checkpoint | Require a settled task, visible restatement, targeted proof, and one accept-or-reject review. |
| Task preflight | Before task creation, test one behavior, contract boundary, proof cluster, and close decision. |
| Task shaping and execution choice | First size tasks for independent acceptance; then use a risk-benefit check for valid splits and choose keep together, split serially, or split for parallel execution. |
| Targeted proof | Engineer runs the smallest changed-behavior check after a coherent implementation checkpoint and a permitted correction. |
| Acceptance proof | Verify the task's observable completion condition. |
| Regression proof | Check affected-boundary risk, including sibling callers or shared interfaces. |
| Oversized task | Split only at an independent behavior, contract boundary, proof cluster, or close decision. |
| Cause lane | Use Diagnose for an unknown cause and Deliver for a known cause. |
| Plausible edge cases | Classify each as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`. |
| Architect direct path | Use only for one bounded mechanical exception with one narrow proof command. |
| Quick Fix classification | Use only for an exact, local, reversible outcome with one immediate narrow proof. |
| Quick Fix batch review | Review pending Quick Fixes at a shared checkpoint. |
| Assisted parallel work | Apply the universal independence gate; immediately before parallel spawn, recheck the resource boundary: separate mutable resources, no unfinished dependency, and meaningful elapsed-time savings after coordination and verification; fall back to serial when conditions change. |
| Overlapping read-only Scouts | Allow overlap only for independent questions over stable sources. |
| Bounded Scout evidence | Route broad inquiries to Scout with citations, coverage, conflicts, and unknowns. |
| Scout platform and version dimensions | Require broad inquiries to name platform and version dimensions, map shared core and variants before broad reads, and return coverage plus unknowns. |
| Dependency start block | Reject work with unfinished dependencies. |
| Architect writer barrier | Stop writers before integration, documentation, machine verification, or stateful operations. |
| Collision stop | Stop before a shared resource and report the collision and checkpoint. |
| Custom role request | Require direct user authority before adding a role. |
| Verifier and Maintainer sidecars | Keep Verifier read-only and Maintainer within recorded operation authority. |
| Verifier repeat guard | Do not repeat an identical targeted command unless independent proof, disputed evidence, or repository policy requires it. |
| Full-suite boundary | Run the full suite only for release, broad shared contracts, migrations/build graphs, explicit repository requirements, or no trustworthy selector. |
| Child identity and ownership | Architect allocates one lowercase role prefix and Greek suffix, then keeps the exact `task_name`. |
| Child visible update and communication routing | Routine progress stays in the child thread and creates no explicit parent message. This includes the start restatement. Explicit parent messages occur only when immediate Architect action is required for a blocker, collision, scope change, proof mismatch, or decision. Completion has exactly one final return and no separate completion message; the final return must end the active turn and keep `followup_task` reuse reachable. The Architect does not echo unchanged child facts. No update includes role repetition. Preserve child-thread visibility, pre-handoff briefs, Engineer restatement, roles, modes, naming, lifecycle, and proof rules. |
| Handoff | Use natural prose and fact order; do not expose chain-of-thought or rigid scripts. |
| Reachable role thread, child replacement, or pool exhaustion | Follow up before replacement and recycle only unreachable labels after the pool ends. |
| External-tool routing and token-waste signals | Keep the Architect's decision boundary and route discovery, mutation, operations, and checks by role. |
| Proof and integration checkpoint | Pause writers; Verifier runs the packaged checkpoint helper before and after proof over the same task-owned paths, compares values locally, and omits full values from routine reports. |
| Automation lifecycle and stateful operation | Any child reports a transient candidate after directly observing a second equivalent success; Maintainer owns repeated operations, with no scan, registry, Backlog entry, or automatic script. |
| Task closeout | Verifier returns evidence; the owning Architect decides accept, correct, reopen, fail, or close. |
| Shared interface, schema, manifest, lock file, generated output, or exclusive target | Keep work serial. |
| Ledger-to-plan projection | Project unresolved task IDs and titles into exact plan rows; keep `tasks.csv` authoritative. |
