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
- Before any other file mutation, use the installed `tasks.py start` command to create immediate work or claim a Planned task.
- Keep one intentional change per task with observable acceptance and explicit proof.
- Allowed statuses are `Planned`, `In Progress`, and `Done`.
- `Planned` is unowned. `In Progress` and `Done` retain the stable 8-digit task owner supplied by the plugin hook.
- Only the owner closes a task. A different task may close it only after a direct user request and must record the override reason.
- Use `FEAT-*` for documented behavior, `DEC-*` for a documented durable choice, `REPO` for other project work, and `BOOTSTRAP` only for initialization.
- Each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.
- Split independently accepted and independently proved work. Keep inseparable coding steps transient.

## Delivery Gates

1. Unknown failure cause enters Diagnose before a fix.
2. No implementation starts without known scope, acceptance, proof, and an owned `In Progress` task.
3. Run the structural before-write check.
4. Change only the approved slice and keep affected truth in sync.
5. Verify acceptance and evidence before moving to `Done`.

## Subagent Gate

- Before Deliver or the first delegated read-only operation, read and apply `$lean-sdlc`'s canonical `references/subagents.md`, then state `Mode | Required sidecars | Executor action | Reason`.
- Keep architecture, interfaces, task state, acceptance, integration, and closeout with the lead.
- Keep one lazily spawned thread for each child role during one lead Codex task. Reuse it across repository tasks and inquiries.
- In Assisted mode, delegate one durable task beyond the direct fast path to one reusable Executor. Keep correction handoffs concise and transient. Trigger read-only Researcher only when substantial evidence would pollute lead context. Focused keeps Researcher when its trigger applies.
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
