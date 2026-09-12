# Project

## Problem

AI produces code faster than teams keep intent, ownership, and proof coherent. Repository work can solve the wrong problem, lose its owner, or claim completion without evidence.

## Outcome

For a stated beneficiary in a defined situation, Lean-SDLC turns desired progress into an owned, reviewable repository change. It keeps purpose visible, makes the smallest useful task explicit, and closes with acceptance evidence.

## Scope

- One workflow with no mode selector or Engineer route.
- Natural conversation, brainstorming, shaping, investigation, and diagnosis remain read-only until explicit implementation authority exists.
- Before initial tasks, authorized work, or material scope change, Lead visibly restates intent and shows all five fields. Later claims reuse the approved plan. Plan-only requests remain read-only after the plan. Plan-and-implement requests continue under authority without repeated approval. Reuse settled context, decisions, and suitable architecture. Ask only material missing questions. Compare alternatives only when consequential.
- One canonical lifecycle runs from intent through owned work, proof, documentation, operations, and closeout.
- Five visible fields: Outcome states beneficiary, situation, desired progress, and established reason without invented business benefits. Work states independently accepted changes, grades, sequencing, approach, and rationale; its How covers architecture and implementation. Acceptance states observable behavior and constraints. Checks state needed evidence, its limits, and who checks it. Limits state exclusions, unresolved choices, and operation authority.
- Simple, Normal, and Complex task grades remain transient in the visible plan and handoffs. Grades do not add ledger columns.
- Root tasks.csv remains the only durable task plan. The ledger keeps atomic outcomes, owners, dependencies, acceptance, proof, and evidence.
- The [plan protocol](../plugins/lean-sdlc/skills/lean-sdlc/references/plan.md) governs display: real IDs, exact titles, and process lines start one-task work after creation and ownership; changed rows show middle updates; initial and final tables cover multi-task work. Lead closes accepted tasks through `tasks.py`, then confirms success before showing Done. Failed transactions affect affected rows; ownership, dependencies, and before-write gates remain prerequisites.
- Lead may continue stable, independent ready work during verification; dependent work waits. Closure uses accepted verification without repeating it. Requirements, safety, authority, and proof remain binding.
- Backlog remains parked work. Direct user authority is required to add or promote it.
- Lead owns intent, architecture, scope, permissions, task boundaries, acceptance, integration, final decisions, task transactions, writes, operation replay, implementation, code-local tests, focused checks, and accepted ledger corrections. Scout, Maintainer, and Verifier are conditional and bounded: Scout gathers read-only evidence for substantial uncertainty; Maintainer changes shared documents or reports substantial reconciliation discrepancies; Verifier performs assigned independent acceptance and regression checks. See the [role protocols](../plugins/lean-sdlc/skills/lean-sdlc/protocols/common.md).
- Verification assignments state an acceptance question, minimum checks, and stop condition. Proof separates demonstrated behavior and constraints from expected effects. Required measured impact without proof blocks closure; otherwise report effects as unproven and do not invent business benefits for technical work. Report unavailable proof; runtime investigation is not automatic. Do not silently waive required proof; reduced acceptance needs user approval.
- Documentation review covers affected work, reuses valid evidence, and broadens only for broad impact or missing relevant evidence. See the [documentation reference](../plugins/lean-sdlc/skills/lean-sdlc/references/documentation.md).
- Support is conditional; no quota. Before launch or reassignment, handoffs state purpose and wait or continue; the one-task process line can satisfy this. Event-driven waits avoid unchanged polling. Omit routine starts and acknowledgments. Progress reports show meaningful results, decisions with reasons, or blockers, not command logs. Report failures, collisions, unsafe conditions, changed assumptions, and required decisions immediately; otherwise return one useful final result. Optional patterns include next-task Scout, consolidated proof, and Maintainer handoff facts. See the [common protocol](../plugins/lean-sdlc/skills/lean-sdlc/protocols/common.md).
- Support roles cannot assign peers, widen scope, change decisions, or modify tracked source outside their boundary.
- Independent stable scopes may overlap only with stable inputs, separate mutable resources, no unfinished dependency, and meaningful time savings. Shared interfaces, schemas, manifests, generated output, and external targets remain serial.
- Cancellation checks the underlying process or command. Uncertain termination keeps the target blocked.
- Required repository files are AGENTS.md, docs/PROJECT.md, and root tasks.csv.
- Optional document families require concrete triggers and semantic sizing; each numbered family gets INDEX.md with its first document. docs/PROJECT.md is the only mandatory shared document. Maintainer owns narrative truth and indexes; Lead approves meaning and splits. Maintainer works only on shared documents or substantial reconciliation. No mandatory assessment, no-change reason, or final bookkeeping. See the [documentation reference](../plugins/lean-sdlc/skills/lean-sdlc/references/documentation.md).
- After the first guided build, package, deployment, flash, runtime, or smoke success, record the procedure in docs/OPERATIONS.md; no new family is implied. Existing procedures replay exact commands against explicit targets and accepted source identity. Lead executes by default; an assigned Verifier may execute once as independent proof. Do not duplicate the gate; Lead applies accepted reconciliation corrections. See the [operations reference](../plugins/lean-sdlc/skills/lean-sdlc/references/operations.md).
- Automatic routine discovery and automatic script-creation suggestions are excluded. A new reusable script requires an explicit user request.
- Upgrade preserves task IDs, owners, evidence, documents, custom instructions, valid preferences, supported earlier ledger conversions, and stopped work. Conflicting repository state stops without silent selection. No field selects a workflow.
- The ledger remains authoritative. Mirror unresolved task IDs and titles in the native plan view when available. Keep checkpoint values local and report equality or mismatch without exposing full fingerprints.
- Release validation covers package structure, version consistency, portable checks, exact remote identity, installed/source equality, selected-repository scope, structural integrity, and final ledger reconciliation.

## Constraints

- Keep discussion and planning read-only until the user gives implementation authority.
- Before non-control writes, require an owned In Progress task, a successful before-write gate, and one writer per mutable path or external target. Lead owns task transactions and ledger mutations through `tasks.py`. Lead runs recorded operations and their built-in checks directly; all roles may read task facts. Maintainer does not perform routine ledger writes or replay.
- Lead owns implementation and test code and may run focused checks. Verifier owns substantial independent acceptance and regression checks. Maintainer does not run tests.
- Use shell and Python standard library only. Keep repository state readable and recoverable.
- Preserve existing project documents, custom rules, task IDs, ownership, evidence, valid preferences, and unrelated stopped work.
- Do not infer commit, push, publication, deployment, or reusable-script authority. Use explicit or valid standing authority for the exact target.
- Do not create optional documents without their concrete triggers or a release operation record before guided checks produce exact successful evidence.
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
- Plan-and-implement work proceeds within explicit authority without redundant approval. Visible plans connect the established beneficiary, situation, reason, desired progress, approach, acceptance, checks, and limits; later work reuses settled context and decisions.
- Tasks remain atomic, owner-aware, dependency-valid, and cycle-free. Exact task state remains visible.
- Lead retains decisions and records accepted task and operation results. Scout returns bounded evidence; Maintainer records shared-document changes and substantial reconciliation discrepancies; Verifier supplies assigned independent proof; Lead applies accepted ledger corrections.
- Original user requirements, task acceptance, affected regression risk, documentation parity, and evidence limits are checked before closure. Results distinguish demonstrated behavior from unproven effects. Missing required impact proof blocks closure; optional impact remains unproven without a benefit claim.
- Documentation triggers, semantic sizing, family templates, and index navigation remain valid.
- Recorded operations replay only with valid authority, explicit targets, accepted source identity, safe recovery, and redacted output.
- Supported upgrades preserve ledger history, custom rules, valid preferences, and stopped work.
- Release exit evidence includes portable release checks, validators, exact remote commit and tag on origin main, byte-equal installed and source packages, selected-repository isolation, structural validation, and final ledger reconciliation.
- No completion claim relies only on a dispatched action, saved response, structural assertion, or unexecuted command. Closure may rely on an accepted verified conclusion without repeating the same verification.

## Current promise

- Stage: Evolution
- Version: 1.32.0
- Version goal: Deliver reason-to-result intent plans, settled-context reuse, direct Lead implementation, conditional support, proportional proof with evidence limits, and clear status.
- Exit evidence required: Final local release gate and validators, remote identity, installed/source equality, selected-repository upgrade validation, and final ledger reconciliation. Native behavior and performance are not claimed, and live trials are not required by the approved plan.
