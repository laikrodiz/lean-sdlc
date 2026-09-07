# Project

## Problem

AI can produce code faster than a team can keep intent, ownership, and proof coherent. Repository work can then solve the wrong problem, lose its owner, or claim completion without useful evidence.

## Outcome

Lean-SDLC is a small, shareable Codex workflow for turning a clear user outcome into an owned, reviewable repository change. It keeps the human purpose visible, makes the smallest useful task explicit, and closes work with acceptance evidence.

## Scope

- Shape, Decide, Plan, Diagnose, Deliver, and Verify lanes.
- One canonical lifecycle from intent through owned work, proof, and closeout.
- Architect is a workflow role independent of the selected model. The Lead owns production code, core tests, decisions, acceptance, and task mutations in Assisted lead-coding. Each work item is Routine or Critical with a short reason; risk classification is separate from execution ownership.
- Helper tests check evaluation code behavior. Document tests check required contract wording.
- `tests/evaluation_runner.py` grades saved JSON answers against scenario assertions. By default, it reads `tests/evaluation_observations_fixture.json`; it does not execute an agent or verify actions.
- `tests/live_evaluation.py` optionally runs fresh Codex sessions, collects final structured JSON answers, and validates their structure. Its output needs separate grading by `tests/evaluation_runner.py`. It does not grade decision correctness or verify tool actions, file edits, or real workflow reliability.
- One portable release gate for local and CI checks.
- One consistent task, direct-path, and proof contract.
- Visible ambiguous repository discovery and durability warnings.
- One Git-free, task-scoped checkpoint helper.
- A complete `why -> what -> how -> proof` intent gate before changes.
- Three required repository files: `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`.
- An atomic, human-readable task ledger with one task per independently accepted repository state. Dependencies must be `Done` before a task starts.
- Task planning preserves complete outcomes with cohesive tests and documentation. It splits only at independent acceptance boundaries, not arbitrary file, function, or line boundaries. Foundations are accepted before dependent work, and combined integration has an assigned check.
- During implementation, unresolved ledger task IDs and titles project into Codex's plan view. Brainstorming and rephrasing remain read-only and create no task view.
- Architect ownership of intent, architecture, interfaces, task boundaries, acceptance, integration, evidence, and closeout.
- A visible pre-handoff design brief with bounded child decisions and no exposed chain-of-thought.
- Clear contracts communicate outcome, interfaces, invariants, failure behavior, mandatory decisions versus suggestions, freedom, proof, and stop conditions.
- Four agent roles: Engineer for Delegating implementation, Maintainer for optional records, documents, known information, or established checks, Scout for substantial discovery, and Verifier for independent Critical review.
- One role-routing precedence chain, layered targeted, acceptance, and regression proof, and bounded full-suite use. One command may satisfy several proof purposes. Reuse proof and artifacts only when relevant source, dependencies, configuration, environment, toolchain, and target inputs match.
- Assisted mode is the default lead-coding workflow. Delegating preserves the previous Assisted Engineer workflow. Solo remains Lead-only with no automatic child. Maintainer use and other child handoffs are optional when overhead exceeds benefit; tiny chores need no child.
- Critical work requires independent review and evidence, including for Lead-written work. In Solo, missing evidence requires an approved reviewer or a mode change; Solo does not spawn a Verifier automatically. All modes preserve the selected model and effort.
- Versioned saved mode state starts new state in `assisted`. Only the exact unversioned legacy state `{mode, fast_children}` migrates: legacy `assisted` becomes `delegating` with active mode locked, and legacy `solo` stays `solo`. Invalid or unknown state fails visibly and never resets to defaults.
- The selected mode is the requested or restored choice. The active mode is the currently activated workflow. A default `Mode: assisted` does not mean Assisted is active. For initial authorized implementation, select and explicitly begin the mode before loading its workflow instructions. A same-mode begin reuses instructions already loaded. Discussion remains read-only and does not activate a mode. The spawn guard rejects unbegun modes.
- An explicit user request can switch modes within the same session. Finish or safely cancel active children and commands first. Select without `--begin`, load the new workflow, then activate with `--begin`. Selection clears activation and blocks child starts. Preserve session identity, owner, task IDs, acceptance, model, effort, child tier, and valid proof. The helper cannot verify termination or instruction loading; the Lead must verify those steps. A mode change does not authorize broader work, weaker proof, or a contract upgrade.
- The contract upgrader recognizes the exact released `v1.26.0` template. It replaces only the managed prefix and preserves appended custom project rules. Edited or unknown core instructions require explicit manual reconciliation. Do not overwrite custom rules or interpret application changes as migration authority. After an authorized upgrade, start a fresh session so stale injected instructions are not reused. Hooks validate covered spawn arguments only; they do not establish identity or prevent canceled child writes.
- The latest user outcome, scope, proof, and stop condition govern execution and resume. A canceled support path cannot restart from late results. A status question does not cancel work. An explicit stop ends nonessential work.
- An interrupted child turn can leave its command running. No atomic guarantee exists for command termination during interruption. Cancel and verify the command before interrupting the child.
- Delivery, verified acceptance, and marking all earlier tasks `Done` are separate outcomes. Truthful handoffs use current evidence and do not wait for obsolete paperwork.
- Delegating Engineers own complete atomic outcomes, including permitted corrections, tests, and mechanical consistency.
- A running child lifecycle state remains available despite wait expiry or silence. The Delegating Engineer visibly restates its understanding and completes routine targeted proof.
- Assisted lead-coding keeps production work with the Lead. Routine support progress stays quiet in child threads in Assisted and Delegating, including the start restatement. Explicit parent messages are only for events that require immediate Architect action. Completion produces one final return. The Architect does not repeat unchanged child facts.
- Small settled tasks use the selected workflow without compulsory child handoffs. Larger or uncertain work uses specific decision or risk checkpoints. Material blockers and conflicts escalate.
- In Delegating, one preauthorized read-only Verifier may be nested for a qualifying single task. Combined checkpoints use one Architect-started Verifier. The Architect gives one final visible alignment signoff. Verification is risk-based and not duplicated.
- Useful concurrency is constrained by native runtime capacity and independent mutable ownership, not a fixed workflow-agent or Engineer-count limit. Shared resources remain serial. Child work stays in one shared worktree without new worktrees.
- Substantial external-tool work keeps decisions with the Architect. Delegate when expected benefit exceeds handoff and verification costs; support contracts remain concise with the reason, owned boundary, acceptance, proof, and stop condition. Before an expensive or state-changing operation, confirm the exact target, prerequisites, and required permissions through read-only checks. External-tool call count and discovery are cues only. Preserve permissions and one mutable-target owner.
- The Architect reviews actual changes, evidence, and changed public interfaces against consumers, tests, and documented usage. It chooses Accept, Revise, or Redesign and returns actionable findings together. In Delegating, the Architect does not repair delegated Routine work.
- Revise keeps the same team when the contract remains settled. Redesign corrects the contract before work resumes.
- Bounded read-only evidence work stays limited to its defined question, groups independent discovery, and preserves complete authoritative reads.
- Repeated repository mechanics can yield transient automation candidates without adding new durable state. Retain a maintained deterministic command only when later reuse justifies it. Keep executable commands in code blocks, separate from explanatory prose.
- Readable checkpoint reports retain exact machine proof. Reuse evidence only when source, dependencies, configuration, environment, toolchain, and target inputs remain valid. Stop dependent actions when metadata validation fails. Stable independent boundaries may verify and draft separate documentation concurrently. Shared documentation and common regression checks batch across atomic tasks while each task keeps its own acceptance set. Final release stops relevant writers before release checks.
- Inline Quick Fix classification during Plan for trivial settled edits, with immediate narrow proof and deferred shared review.
- `docs/PROJECT.md` is the only mandatory shared project document.
- Optional document families use concrete triggers and semantic sizing.
- Each numbered family gets a small `INDEX.md` with its first document.
- The Maintainer owns shared narrative truth and indexes.
- The Architect approves document meaning and splits.
- Root `archive/` requires an explicit user request and remains inert.

## Constraints

- Keep durable planning in root `tasks.csv`. Use bundled task commands for ledger changes.
- Keep the existing tasks helper as the sole ledger writer. Keep Lead task mutations and support retrieval of concise task views and current documents. Do not add ledger schema, storage, history columns, receipt or event stores, databases, daemons, or new task-writer paths.
- Keep discussion read-only until the user gives implementation authority.
- Keep shared truth in its owning document. Keep code-local truth with its code owner.
- Use shell and Python standard library only. Keep repository state readable and recoverable.
- Preserve task ownership, dependency order, acceptance, and proof across resume and compaction.

## Deferred

- Hosted task services or issue-tracker replacement.
- Mandatory feature, decision, architecture, state-machine, interface, data, operations, security, glossary, or verification documents.
- A repository-wide documentation archive policy.
- Dashboards, telemetry, cache accounting, and project-specific operational recipes.

## Success

- Users can invoke Lean-SDLC explicitly or through repository rules.
- A new repository can start with the three required files and a root ledger.
- The plan view mirrors each unresolved ledger task ID and title during implementation. Brainstorming creates no task view.
- Tasks remain atomic, owner-aware, permission-preserving, dependency-valid, and cycle-free.
- Broad work is split only when each result remains a complete, independently acceptable outcome. Useful concurrency also needs separate mutable ownership, native capacity, and benefit beyond handoff and verification costs.
- Selected workflows preserve ownership and permission boundaries. Delegated external-tool work has one mutable-target owner and returns bounded evidence.
- Routine and Critical work use risk-aware execution ownership. Critical work has independent evidence and cannot self-certify.
- Support progress stays quiet, action-required events reach the Architect immediately, and completion produces one final return without duplicate Architect commentary.
- Substantial discovery returns bounded evidence without mutation authority and preserves authoritative reads.
- Transient automation candidates add no new durable state. A maintained deterministic command needs a later reuse case and maintenance evidence.
- Release checks use one portable gate in local and CI contexts.
- Evaluation evidence separates helper code-behavior tests from document contract-wording tests.
- Saved-fixture checks grade repository-owned JSON answers with deterministic assertions.
- Optional live collection starts fresh sessions, collects final structured JSON answers, and validates their structure. A separate runner grades those answers.
- Evaluation evidence does not measure real workflow execution reliability.
- Task, direct-path, and proof inputs follow one consistent contract.
- Ambiguous repository discovery is visible, and durability warnings identify risks before they persist.
- Task-scoped checkpoints can run without Git access.
- Eligible Quick Fixes receive narrow proof immediately and broad review in a later Standard or final batch checkpoint.
- Checkpoint reports stay readable, exact machine proof remains available, and serial closeout uses repository truth.
- Delivery, verified acceptance, and marking all earlier tasks `Done` remain separate outcomes.
- Acceptance is defined before implementation, and testable behavior has an identified acceptance check before production changes.
- Documentation commands run exactly as documented in their stated environment. A substitute interpreter or argument needs a documented, verified alternative.
- The final V5 matched benchmark was not run. No benchmark-based performance gain is claimed.
- Older benchmark results are historical context only.

## Current promise

- Stage: Evolution
- Version: 1.27.1
- Version goal: Allow explicit same-session mode changes. Assisted lead-coding is the default. Delegating preserves the former Assisted Engineer route. Solo remains lead-only. Preserve risk-based proof, permissions, ownership, atomic acceptance, ledger, and bytecode boundaries.
- Exit evidence: Acceptance uses code, documentation, helper checks, and independent proof. Release, installation, tagging, and pushing remain separately authorized. Evaluation checks do not measure real workflow execution reliability.
