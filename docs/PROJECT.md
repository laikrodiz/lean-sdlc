# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- One workflow with no mode selector and no Engineer route.
- Natural conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until explicit implementation authority exists.
- Plan-only requests show a five-field plan and stop. Plan-and-implement requests continue within their authority.
- One canonical lifecycle from intent through owned work, proof, documentation, operations, and closeout.
- Five visible plan fields: Outcome, Work, Acceptance, Checks, and Limits.
- Simple, Normal, and Complex task grades remain transient in the visible plan and handoffs. Grades do not add ledger columns.
- Root tasks.csv remains the only durable task plan. The ledger keeps atomic outcomes, owners, dependencies, acceptance, proof, and evidence.
- Backlog remains parked work. Direct user authority is required to add or promote it.
- Lead owns intent, architecture, scope, permissions, task boundaries, acceptance, integration, and final decisions.
- Lead implements code and writes code-local tests. Scout performs bounded read-only evidence work. Maintainer performs routine ledger writes, shared-document work, and authorized recorded operations. Verifier runs all tests and independent proof.
- Support roles cannot assign peers, widen scope, change decisions, or modify tracked source outside their boundary.
- Independent stable scopes may overlap only with stable inputs, separate mutable resources, no unfinished dependency, and meaningful time savings. Shared interfaces, schemas, manifests, generated output, and external targets remain serial.
- Cancellation checks the underlying process or command. Uncertain termination keeps the target blocked.
- Required repository files are AGENTS.md, docs/PROJECT.md, and root tasks.csv.
- Optional document families use concrete triggers and semantic sizing. Each numbered family gets INDEX.md with its first document.
- docs/PROJECT.md is the only mandatory shared project document. The Maintainer owns shared narrative truth and indexes. The Lead approves meaning and document splits.
- A first build, package, deployment, flash, runtime, or smoke procedure enters docs/OPERATIONS.md only after a guided success. No new required document family is implied.
- Existing recorded procedures replay exact commands against explicit targets and accepted source identity.
- Automatic routine discovery and automatic script-creation suggestions are excluded. A new reusable script requires an explicit user request.
- Upgrade preserves task IDs, owners, evidence, documents, custom instructions, valid preferences, supported earlier ledger conversions, and stopped work. Conflicting repository state stops without silent selection. No field selects a workflow.
- The ledger remains authoritative. Mirror unresolved task IDs and titles in the native plan view when available. Keep checkpoint values local and report equality or mismatch without exposing full fingerprints.
- Release validation covers package structure, version consistency, portable checks, exact remote identity, installed/source equality, selected-repository scope, structural integrity, and final ledger reconciliation.

## Constraints

- Keep discussion and planning read-only until the user gives implementation authority.
- Use the packaged tasks.py helper for every ledger mutation. Maintainer performs routine ledger writes with the Lead owner.
- Require an owned In Progress task and a successful before-write gate before non-control repository writes.
- Keep one agent as the writer for each mutable path or external target.
- Lead owns implementation and test code. Verifier owns test execution. Maintainer does not run tests.
- Use shell and Python standard library only. Keep repository state readable and recoverable.
- Preserve existing project documents, custom rules, task IDs, ownership, evidence, valid preferences, and unrelated stopped work.
- Do not infer commit, push, publication, deployment, or reusable-script authority. Use explicit or valid standing authority for the exact target.
- Do not create new optional documents without their concrete trigger. Do not create a release operation record before guided release checks produce exact successful evidence.
- Normal source replacement relies on Git. Root archive/ requires an explicit user request and remains inert.

## Deferred

- Hosted task services or issue-tracker replacement.
- New required document families.
- Optional feature, decision, architecture, state-machine, interface, data, security, glossary, verification, and operation documents until their triggers exist.
- A repository-wide documentation archive policy.
- Dashboards, telemetry, cache accounting, and project-specific operational recipes beyond accepted recorded procedures.

## Success

- Users can invoke Lean-SDLC explicitly or through repository rules.
- Conversation, investigation, and plan-only requests do not create tasks or change repository files.
- Plan-and-implement work proceeds within explicit authority without redundant approval.
- Tasks remain atomic, owner-aware, dependency-valid, and cycle-free. Exact task state remains visible.
- Lead retains decisions. Scout returns bounded evidence. Maintainer records accepted ledger, document, and operation changes. Verifier runs the required tests and proof.
- Original user requirements, task acceptance, affected regression risk, and documentation parity are checked before closure.
- Documentation triggers, semantic sizing, family templates, and index navigation remain valid.
- Recorded operations replay only with valid authority, explicit targets, accepted source identity, safe recovery, and redacted output.
- Supported upgrades preserve ledger history, custom rules, valid preferences, and stopped work.
- Release exit evidence includes portable release checks, validators, exact remote commit and tag on origin main, byte-equal installed and source packages, selected-repository isolation, structural validation, and final ledger reconciliation.
- No completion claim relies only on a dispatched action, saved response, structural assertion, or unexecuted command.

## Current promise

- Stage: Evolution
- Version: 1.28.0
- Version goal: Deliver one task-authorized workflow with Lead-owned implementation, bounded Scout, Maintainer, and Verifier support, explicit authority separation, preserved project state, and validated release and installation behavior.
- Exit evidence required: Actual authority and interruption cases; focused ledger transactions; full Verifier test execution; changed-input and failure handling; documentation trigger and parity review; controlled operation and cancellation cases; upgrade preservation evidence; portable release checks; exact remote identity; installed/source comparison; selected-repository structural validation; and final ledger reconciliation.
