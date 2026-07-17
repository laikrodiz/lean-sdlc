---
name: lean-architecture
description: Shape a Lean-SDLC project into a small, defensible technical form by choosing stack, boundaries, key flows, and durable decisions without slipping into low-value implementation detail. Use when scope and features are stable enough to need architecture notes, decision records, or optional technical docs.
---

# Lean Architecture

## Purpose

Use this skill after active features are stable enough to deserve technical shaping.

Follow the repository's `AGENTS.md`. Open [../lean-sdlc-core/SKILL.md](../lean-sdlc-core/SKILL.md) only when recovering context or resolving a shared contract.

## Workflow

1. Re-read brief, scope, and active feature files.
2. Ask what technical choices are truly irreversible or costly.
3. Choose the simplest stack that fits operator skill, deployment reality, testability, diagnostics, and maintenance cost.
4. Define modules and boundaries only to the level needed for safe implementation.
5. Record major decisions with context and consequences.
6. Push mappings, route tables, commands, protocol fields, and other dense technical bindings into `INTERFACES.md` or `docs/maps/*.md` when they need shared documentation.
7. Establish the first shared proof and diagnostics baseline when cross-cutting policy now exists.
8. Keep feature behavior separate from decision records and keep decision records separate from implementation recipes.

## Delegation Checkpoints

Apply the shared [delegation policy](../lean-sdlc-core/references/delegation.md). Explorers may collect bounded option evidence when the cost gate passes. Keep stack, boundary, and tradeoff decisions with the Sol decision profile; start at `low` and escalate only for material ambiguity or risk.

## Stack Selection Rules

Choose language and framework from these pressures:

1. deployment environment,
2. operator or team fit,
3. testability,
4. diagnostics support,
5. dependency maturity,
6. maintenance cost,
7. speed to a reliable first version.

Do not choose stack by fashion.

## Boundaries

1. Keep architecture high-level.
2. Do not turn `ARCHITECTURE.md` into low-level implementation notes.
3. Do not create layers that exist only to look clean.
4. Prefer hard cuts over compatibility wrappers unless explicitly justified.
5. Do not store hardware mappings, route tables, or runtime command lists in decisions when a lower doc will do.

## Outcome

Success means the project has a small technical shape, durable decisions are written down, and implementation can proceed without hand-waving or architecture cosplay.
