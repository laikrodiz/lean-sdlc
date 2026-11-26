# Delegating support

Specify purpose, target, owner, inputs, acceptance question, proof, stop condition, allowed paths, exclusions, constraints and authority. Supply exact startup repository, skill and helper paths. Read selected instructions and decisive contracts completely. Reuse unchanged context.

Before spawning support, give a known agent in this thread a bounded follow-up if role, model profile, workspace and context fit. On native Codex, use `followup_task` to start its next turn. If identity is uncertain or a name collides, check the existing agent once before choosing another name. Start fresh if reuse is unavailable, the host requires a new thread, or independence requires fresh context.

On T3, continue a discussion with `t3_thread_send` to the same child thread. Leave `freshContext` unset. A new task ID does not require a new thread. For a new delegated review or re-check, use `delegate_task`, not `t3_thread_send`.

Before launch or material reassignment, name the support role and purpose in one short sentence. Combine this with a task update when useful. Keep assignment details separate. Report failed launches.

## Child profile

For Scout, Maintainer, and Verifier, use the current-generation model one capability tier below the Lead from the same model provider, at Medium reasoning. Keep the Lead's connection; a gateway is not a model family. Use the active catalog and known tier relationships. Never infer rank from list order, price, or similar names. Reuse the choice until the Lead or available profiles change.

If that exact lower-tier profile is unavailable or uncertain, select the Lead's exact model at Medium. If that model lacks Medium, keep the Lead's effort. Honor explicit user overrides for the fields specified. If the host cannot select or reliably inherit the resulting profile, report the blocker; never silently switch. A launch request is not proof of the executed model.

Use the host's model and effort controls. For native Codex, select non-full-history `fork_turns` and omit `agent_type`. Use unique role-prefixed Greek names: native `scout_beta`, T3 title `Scout Beta`. Priority requires user opt-in and host support. On priority failure retry the same profile without priority.
