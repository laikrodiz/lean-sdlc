---
name: lean-versioning
description: Manage Lean-SDLC stage and version framing so the project keeps a current business context and does not stay trapped in stale labels such as perpetual MVP. Use when a version is closing, the stage no longer fits reality, or the next delivery slice needs a new business promise and exit criteria.
---

# Lean Versioning

## Purpose

Use this skill whenever the project framing itself needs to move, not just the task list.

Follow the repository's `AGENTS.md` and read [the lifecycle reference](../lean-sdlc-core/references/lifecycle.md). Open the core only when recovering context or resolving a shared contract.

## Workflow

1. Read current stage, version goal, and exit criteria in `SCOPE.md`.
2. Check whether the current framing still matches reality.
3. If the version is complete, define the next version promise and what is deferred.
4. If the stage is wrong, propose the correct stage and why.
5. Create `docs/versions/V-*.md` only when version history now deserves its own files.

Use the Sol decision profile from the shared [delegation policy](../lean-sdlc-core/references/delegation.md) for version and stage decisions.

## Pressure Tests

1. Is the current version already effectively closed?
2. Has the user context or operator need changed materially?
3. Is the project still acting like discovery when it is already in delivery or operation?
4. Is the team hiding oversized scope behind one vague version label?
5. Is version language being used to hide broad capability buckets instead of clean feature slices?

## Outcome

Success means the project has an honest current framing, clear exit criteria, and a small next promise instead of stale product mythology.
