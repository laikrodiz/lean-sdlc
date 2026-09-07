# Support Allocation

Load this file only when assigning a child. The selected mode determines allowed roles and who can allocate them.

## Allocation and reuse

Reuse a reachable child when its role and context still fit. Start a new child only for a useful, bounded assignment.
Count all active descendants against native capacity. Keep each mutable path, generated output, fixture, and external target under one writer.
Parallel work needs stable shared inputs and a benefit beyond coordination and verification costs. Otherwise, run serially.
Do not create branches or worktrees for parallelism. Never interpret wait expiry or silence alone as failure.

Use a lowercase role prefix and Greek suffix, such as `maintainer_beta`. Keep the existing name when reusing an agent.
Choose an unused suffix from:

`alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi, omega`.

Recycle a role-label combination only after its previous agent is unreachable. Assisted permits Maintainer, Scout, and Verifier only.

## Profiles

For a user-requested tier change, the Lead updates the session before allocating support.
Use `python3 "<skill-root>/scripts/session_state.py" --owner OWNER --fast-children` for Fast or `--no-fast-children` for Standard.
Use the exact state-helper path and current owner. A tier change does not authorize a mode change or broader work.

- Standard: `model=gpt-5.6-luna`, `reasoning_effort=max`, `fork_turns=none` or positive bounded history. Omit `agent_type` and `service_tier`.
- Fast requires user opt-in. Set `service_tier=priority` only when the native tool supports that field.
- If priority fails, retry Luna Max once without `service_tier`. Report unsupported settings; do not invent tool arguments.
- If Luna is unavailable, announce the fallback to `model=gpt-5.6-terra`, `reasoning_effort=xhigh`, bounded history, and no `service_tier` or `agent_type`.

Do not combine model overrides with full-history forks. Preserve the Lead's selected model and effort.

## Assignment and return

Supply the task ID, owner, both roots, request revision, bounded outcome, allowed paths or question, required evidence, and stopping condition.
Include permissions, known facts, and the before-write result when writes are assigned. Point the child to [child.md](child.md) and its assigned role instructions.
In Assisted, use a concise support assignment, not the full Delegating implementation brief.
Keep routine progress in the child conversation. Send the Lead only action-required findings and one final result with evidence references.

Use native messages for changed facts and cancellation. Reuse relevant source references; refresh them when their inputs change.
An accepted message is not completed work. If a child is lost, preserve its assignment as unfinished in existing task facts.
Restore only relevant pending work after interruption. Do not add a message service, worker pool, scheduler, or knowledge database.

The hook validates covered spawn arguments only. Role names do not enforce caller identity, writable paths, or canceled child actions.
The Lead must apply the selected mode, ownership, and cancellation rules to all native calls, including reused agents.

## Command cancellation

Native agent interruption stops the agent turn but can leave its command running.
Cancel the assignment through a native message. Stop and verify its running command before interrupting the child.
Ask the command owner to cancel its existing command session and return termination evidence, not the canceled assignment's normal result.
If the user says not to wait, do not wait for ordinary work. Obtain cancellation evidence or stop the verified command directly.
This order keeps command ownership and cancellation information available. It also avoids leaving an orphan command after interruption.
Prefer its existing command-session cancellation operation. If that operation is unavailable, verify the exact process identity against the assigned command and target before terminating it.
Use a known session identifier or the operating system's process inspection. Never terminate processes by a broad name or unrelated match.
Verify that the command stopped before reporting cancellation complete. If its identity or termination authority is unclear, report command cancellation as unconfirmed.
After command cancellation, use the native agent interrupt operation. Do not wait for the obsolete assignment to finish normally.
Stopping the canceled command is required cancellation work. Do not start unrelated cleanup, tests, or task closure.
