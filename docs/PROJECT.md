# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- One workflow with no mode selector and no Engineer route.
- Natural conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until explicit implementation authority exists.
- Before the initial task set, new authorized work, or a material scope change, Lead visibly restates meaningful intent and shows all five fields. Later task claims reuse the unchanged visible approved plan. Plan-only requests remain read-only and stop after the plan. Plan-and-implement requests continue within their authority without repeated approval.
- One canonical lifecycle from intent through owned work, proof, documentation, operations, and closeout.
- Five visible plan fields: Outcome, Work, Acceptance, Checks, and Limits. Checks describe how Lead and, when assigned, Verifier establish the acceptance facts.
- Simple, Normal, and Complex task grades remain transient in the visible plan and handoffs. Grades do not add ledger columns.
- Root tasks.csv remains the only durable task plan. The ledger keeps atomic outcomes, owners, dependencies, acceptance, proof, and evidence.
- For one task, the display starts with `Starting <real ID>: <exact title>.` and then `Optimal process: <actual work/roles>.` Real task creation and ownership complete before that announcement. For one changed task, even within a multi-task workload, use a short status line. For multiple simultaneous changes, show changed rows only. Initial and final tables remain for multiple tasks, with grades shown in the plan, handoffs, and those tables. After accepting proof, Lead closes the task directly through the helper, confirms success, and shows Done. Failed transactions correct only affected rows. Real IDs, ownership, dependencies, and before-write gates remain prerequisites.
- Lead may continue independent ready work while verification runs when inputs are stable and the work has no unfinished dependency. Dependent work waits. Closure uses the verified conclusion without repeating verification. Original requirements, safety, authority, and missing proof remain binding.
- Backlog remains parked work. Direct user authority is required to add or promote it.
- Lead owns intent, architecture, scope, permissions, task boundaries, acceptance, integration, and final decisions. Lead owns every task transaction and write through `tasks.py`, and performs recorded-operation replay, including built-in checks. Lead implements code, writes code-local tests, and runs immediate focused checks. Scout performs bounded read-only evidence work when substantial uncertainty exists. Maintainer performs actual shared-document work or investigates and reports substantial reconciliation discrepancies only. Verifier performs substantial independent acceptance and regression checks when assigned. Lead applies accepted ledger corrections.
- Verification assignments state a specific acceptance question, minimum sufficient checks, and a stop condition. Unavailable proof is reported; runtime investigation is not automatic. Required proof is not silently waived; reduced acceptance requires user approval.
- Documentation review defaults to affected work and reuses valid review evidence. Broad review applies only for broad impact or missing relevant evidence.
- Support roles are conditional. Do not impose an agent quota. Before launch or reassignment, support handoffs state one sentence of purpose and whether work waits or continues. The process line in a single-task start announcement can satisfy that support-launch announcement. Do not repeat it. Event-driven waits avoid unchanged status or log polling. Routine subagent start, acknowledgment, and progress messages are omitted. Report failures, blockers, and required decisions immediately; otherwise return one useful final result without duplicate success messages. A next-task Scout, consolidated proof, and Maintainer handoff facts remain optional support patterns.
- Support roles cannot assign peers, widen scope, change decisions, or modify tracked source outside their boundary.
- Independent stable scopes may overlap only with stable inputs, separate mutable resources, no unfinished dependency, and meaningful time savings. Shared interfaces, schemas, manifests, generated output, and external targets remain serial.
- Cancellation checks the underlying process or command. Uncertain termination keeps the target blocked.
- Required repository files are AGENTS.md, docs/PROJECT.md, and root tasks.csv.
- Optional document families use concrete triggers and semantic sizing. Each numbered family gets INDEX.md with its first document.
- docs/PROJECT.md is the only mandatory shared project document. The Maintainer owns shared narrative truth and indexes. The Lead approves meaning and document splits.
- The Maintainer engages only for actual shared-document changes or substantial reconciliation investigation and reporting. There is no mandatory per-task assessment stage, no-document-change reason, or final bookkeeping.
- A first build, package, deployment, flash, runtime, or smoke procedure enters docs/OPERATIONS.md only after a guided success. No new required document family is implied.
- Existing recorded procedures replay exact commands against explicit targets and accepted source identity. Lead is the default executor. An explicitly assigned Verifier may execute one procedure once as designated independent proof; do not duplicate the gate. Lead applies accepted ledger corrections from reconciliation reports.
- Automatic routine discovery and automatic script-creation suggestions are excluded. A new reusable script requires an explicit user request.
- Upgrade preserves task IDs, owners, evidence, documents, custom instructions, valid preferences, supported earlier ledger conversions, and stopped work. Conflicting repository state stops without silent selection. No field selects a workflow.
- The ledger remains authoritative. Mirror unresolved task IDs and titles in the native plan view when available. Keep checkpoint values local and report equality or mismatch without exposing full fingerprints.
- Release validation covers package structure, version consistency, portable checks, exact remote identity, installed/source equality, selected-repository scope, structural integrity, and final ledger reconciliation.

## Constraints

- Keep discussion and planning read-only until the user gives implementation authority.
- Lead owns every task transaction and write through `tasks.py`, including every ledger mutation and built-in check. Lead replays recorded operations. All roles may read task facts. Maintainer does not perform routine ledger writes or recorded-operation replay.
- Require an owned In Progress task and a successful before-write gate before non-control repository writes.
- Keep one agent as the writer for each mutable path or external target.
- Lead owns implementation and test code and may run immediate focused checks. Verifier owns substantial independent acceptance and regression checks. Maintainer does not run tests.
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
- Lead retains decisions and records accepted task and operation results directly. Scout returns bounded evidence when substantial uncertainty exists. Maintainer records actual shared-document changes and reports substantial reconciliation discrepancies. Verifier runs substantial independent acceptance and regression proof when assigned. Lead applies accepted ledger corrections.
- Original user requirements, task acceptance, affected regression risk, and documentation parity are checked before closure.
- Documentation triggers, semantic sizing, family templates, and index navigation remain valid.
- Recorded operations replay only with valid authority, explicit targets, accepted source identity, safe recovery, and redacted output.
- Supported upgrades preserve ledger history, custom rules, valid preferences, and stopped work.
- Release exit evidence includes portable release checks, validators, exact remote commit and tag on origin main, byte-equal installed and source packages, selected-repository isolation, structural validation, and final ledger reconciliation.
- No completion claim relies only on a dispatched action, saved response, structural assertion, or unexecuted command. Closure may rely on an accepted verified conclusion without repeating the same verification.

## Current promise

- Stage: Evolution
- Version: 1.31.0
- Version goal: Deliver conditional support, Lead-owned task and recorded-operation execution, focused checks with substantial independent proof when needed, direct status recording, and clear single-task display.
- Exit evidence required: Final local release gate and validators, remote identity, installed/source equality, selected-repository upgrade validation, and final ledger reconciliation. Native behavior and performance are not claimed, and live trials are not required by the approved plan.
