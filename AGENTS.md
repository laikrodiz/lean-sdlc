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

## Delivery Gates

1. Unknown failure cause enters Diagnose before a fix.
2. No implementation starts without known scope, acceptance, proof, and an owned `In Progress` task.
3. Run the structural before-write check.
4. Change only the approved slice and keep affected truth in sync.
5. Verify acceptance and evidence before moving to `Done`.

## Subagent Gate

- Before Deliver or the first delegated read-only operation, read and apply `$lean-sdlc`'s canonical `references/subagents.md`, then state `Mode | Required sidecars | Eligible Workers | Reason`.
- Treat a skipped mandatory sidecar, an ineligible Worker, child-owned task disposition, implicit spawn profile, or child-created agent as a workflow failure.

## Operations

Learn project-specific build, package, deploy, flash, runtime, and smoke procedures from the first guided success. Record the repeatable procedure in `docs/OPERATIONS.md`; update it when reality changes. Never invent a target, store secrets, or retry a state-changing operation without authority and a known recovery rule.

## Engineering

- Build the smallest cohesive units that can be understood, tested, and replaced independently. Use narrow input/output/failure contracts and strengthen boundaries only under observed pressure.
- At changed behavior or module boundaries, classify plausible edge cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`; settle user-visible consequences before implementation.
- Use small Mermaid diagrams for useful visual explanations, tables for mappings, and prose for simple relationships. Never use ASCII pseudographics.

Prefer the smallest defensible solution. Avoid project-size architecture tiers, speculative abstractions, and pass-through modules. Create optional documents only when durable shared pressure justifies them.
