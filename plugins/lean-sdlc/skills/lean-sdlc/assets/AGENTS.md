# Lean-SDLC Repository Rules

Invoke `$lean-sdlc` before planning, diagnosing, changing, verifying, or closing repository work. Read-only explanation and inspection may use the direct fast path.

## Read Order

1. `docs/PROJECT.md`
2. relevant optional feature or decision document
3. `docs/OPERATIONS.md` for build, package, deploy, flash, runtime, or smoke work
4. `tasks.csv`
5. affected code, tests, and technical documentation

Resolve contradictions before closeout.

## Task Gate

- Task commands are control transactions and need no prior task.
- Never edit `tasks.csv` directly.
- Discussion or proposal requests remain read-only. Brainstorming requests use the same read-only path.
- Explicit implementation wording, or clear confirmation to proceed against a recoverable agreed proposal, permits Plan and Deliver. If authority is ambiguous, remain read-only.
- Before task creation and implementation, apply `$lean-sdlc`'s canonical `references/plan.md` contract. It requires natural intent confirmation and a concise visible plan with measurable completion conditions and proof. A one-item plan is valid.
- Keep `tasks.csv` as the only durable task plan. Each durable plan item maps to one task, exactly once. Keep implementation steps transient.
- Use stable child identities: Executor David / `executor_david`, Maintainer Emily / `maintainer_emily`, Verifier Michael / `verifier_michael`, and Researcher Sarah / `researcher_sarah`. Replacements keep the role prefix and use another unused common American first name.
- Each child writes a short plain-language commentary inside its own agent task at work start, implementation or evidence completion with proof starting, blocked state, and final result. Keep lead reports compact and heartbeat limits unchanged.
- Before any other file mutation, use the installed `tasks.py start` command to create immediate work or claim a Planned task.
- Keep one intentional change per task with observable acceptance and explicit proof.
- Allowed statuses are `Planned`, `In Progress`, and `Done`.
- `Planned` is unowned. `In Progress` and `Done` retain the stable 8-digit task owner supplied by the plugin hook.
- Only the owner closes a task. A different task may close it only after a direct user request and must record the override reason.
- Use `FEAT-*` for documented behavior, `DEC-*` for a documented durable choice, `Project` for other project work, and `Bootstrap` only for initialization.
- Use `Context` to identify durable project truth. Dependencies keep task sequencing.
- Each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.
- Split independently accepted and independently proved work. Keep inseparable coding steps transient.

## Delivery Gates

1. Unknown failure cause enters Diagnose before a fix.
2. No implementation starts without explicit user authority, the natural intent and visible-plan gates, known scope, measurable acceptance, explicit proof, and an owned `In Progress` task that matches one durable plan item.
3. Run the structural before-write check.
4. Change only the approved slice and keep affected truth in sync.
5. Verify acceptance and evidence before moving to `Done`.

## Subagent Gate

- Before Deliver or the first delegated read-only operation, read and apply `$lean-sdlc`'s canonical `references/subagents.md`. Tell the user the mode, child action, active task or inquiry, and reason in one or two short sentences.
- Before every child handoff, tell the user the role, task or inquiry, intended result, and proof.
- Include the stable human identity and task name in every child handoff.
- Before every Executor handoff, show a concise architecture brief with `Task`, `Product or architecture decision`, `Boundaries and invariants`, `Non-goals`, and `Proof`.
- Do not start Executor until the visible plan exists and its task matches one durable plan item.
- After each Executor checkpoint, inspect the diff and contract alignment. Then sign off with `Architecture alignment`, `Deviation`, and `Next`.
- Require child reports for work started, implementation or evidence complete with proof starting, blocked, and final result. A silent command may receive at most two heartbeats per command, one every two minutes.
- Use normal prose for user-facing orchestration and labeled multiline fields for internal child handoffs.
- Keep architecture, interfaces, task state, acceptance, integration, and closeout with the lead.
- Keep one lazily spawned thread for each child role during one lead Codex task. Reuse it across repository tasks and inquiries.
- The standard child roles are Executor, Maintainer, Verifier, and Researcher. Use one reusable thread per role and keep depth one.
- Assisted mode uses every triggered role, including Executor. Delegate one durable task beyond the direct fast path to one reusable Executor. Keep correction handoffs concise and transient. Trigger read-only Researcher only when substantial evidence would pollute lead context. Trigger Maintainer only for guided or recorded operations.
- Treat a skipped mandatory handoff, oversized assignment, child-owned decision, incorrect spawn route, or child-created agent as a workflow failure.

## Operations

Learn project-specific build, package, deploy, flash, runtime, and smoke procedures from the first guided success. Record the repeatable procedure in `docs/OPERATIONS.md`; update it when reality changes. Never invent a target, store secrets, or retry a state-changing operation without authority and a known recovery rule.

## Engineering

- Build the smallest cohesive units that can be understood, tested, and replaced independently. Use narrow input/output/failure contracts and strengthen boundaries only under observed pressure.
- At changed behavior or module boundaries, classify plausible edge cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`; settle user-visible consequences before implementation.
- Use small Mermaid diagrams for useful visual explanations, tables for mappings, and prose for simple relationships. Never use ASCII pseudographics.

Prefer the smallest defensible solution. Avoid project-size architecture tiers, speculative abstractions, and pass-through modules. Create optional documents only when durable shared pressure justifies them.

## Technical English

Apply the applicable ASD-STE100 Issue 9 rules to generated English technical prose.

- Use short, direct sentences. Use active voice.
- State one instruction or topic in each sentence.
- Keep procedural sentences to 20 words or fewer.
- Keep descriptive sentences to 25 words or fewer.
- Use one term for one meaning.
- State conditions before actions.
- Explain a necessary abbreviation at its first use.
- Use American English spelling unless project rules require another spelling.
- Avoid idioms, unnecessary synonyms, and vague pronouns.
- Preserve code, commands, paths, identifiers, protocol fields, quotations, and required domain terms.

Preserve technical meaning and safety. Do not claim certified or full controlled-dictionary compliance without an ASD-STE100 checker.
