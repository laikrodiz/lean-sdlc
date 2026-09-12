# Project documentation

## Required core

An initialized project needs `AGENTS.md`, `docs/PROJECT.md`, and root `tasks.csv`. Keep `/tasks.csv` and `/.tasks.lock` in `.gitignore`. Initialization creates missing files without overwriting project work. README remains project-owned.

`AGENTS.md` is a small workflow entry plus custom project rules, not a copy of the skill. `docs/PROJECT.md` is the only mandatory shared project document. It owns problem and user, intended outcome, scope, constraints, assumptions, observable success, current stage, version promise, and exit evidence. Implementation mechanisms belong in code, tests, or technical documents.

## Changed documentation

While understanding and implementing a change, Lead identifies required documentation work from changed facts and existing document owners. Assign Maintainer actual shared-document work, not an assessment for every task. No mandatory no-change report is needed when shared truth remains accurate. Within an assignment, Maintainer checks required updates, applicable optional-document triggers, and affected unchanged documents. Do not create a document merely to show activity.

Lead supplies the behavior and decision delta and approves meaning or document splits. Maintainer owns shared narrative truth and indexes. Lead owns code-local tests, comments, docstrings, annotations, and examples. Resolve conflicting facts in the authoritative source before copying them elsewhere.

Prepare independent documentation work in parallel when inputs are stable. Finalize against accepted implementation. Required safety and usage instructions must exist before the user relies on the result. A Simple task may defer a broader documentation/interaction review, not a known necessary correction.

## Optional families and triggers

Create a document only when its subject needs durable shared detail:

| Family | Owns and trigger |
| --- | --- |
| `docs/features/FEAT-*.md` | One durable user-visible behavior too detailed for PROJECT. |
| `docs/decisions/DEC-*.md` | One costly, easily forgotten, or repeatedly disputed technical choice. |
| `docs/architecture/ARCH-*.md` | One subsystem or responsibility boundary needing independent explanation. |
| `docs/state-machines/STATE-*.md` | One lifecycle with meaningful states and transitions. |
| `docs/interfaces/IFACE-*.md` | One shared or external input, output, error, or compatibility contract. |
| `docs/data/DATA-*.md` | One shared data model, ownership rule, or data lifecycle. |
| `docs/operations/OPS-*.md` | One procedure with independent target, recovery rule, or useful standalone detail. |

Use the matching template in `assets/`: `feature.md`, `decision.md`, `architecture.md`, `state-machine.md`, `interface.md`, `data.md`, or `operation.md`. Templates guide necessary content; they are not extra workflow stages.

Keep the existing `PREFIX-NNN-lowercase-slug.md` convention for numbered documents. Never reuse IDs. Create `INDEX.md` with the first numbered document, using `collection-index.md`. Its columns are ID, Title, Status, Owns, and Related. Link each current numbered document exactly once. The index provides navigation, not a duplicate specification.

## Conditional overview documents

Create `docs/ARCHITECTURE.md` when responsibilities or data flow need a system overview. Keep independently useful subsystem detail in its numbered document.

Create `docs/OPERATIONS.md` after the first successful guided build, package, deploy, flash, runtime, or smoke procedure. It owns the first simple recorded procedure and shared operation map. Existing reusable commands remain documented there or in an OPS document. Follow [operations](operations.md); do not create an automation registry.

Create `docs/SECURITY.md` when trust boundaries or controls need a shared review across documents. Create `docs/GLOSSARY.md` when repeated terms cause material ambiguity. Create `docs/VERIFICATION.md` when proof rules span several tasks or document families. Use the existing security, glossary, and verification templates. None is required for a single local note.

## Size, consistency, and preservation

One document holds one cohesive subject. Split for different outcomes, owners, contracts, change reasons, or update cadences. Merge parts without independent value or maintenance pressure. Do not impose arbitrary line limits or create numbered documents for transient task notes.

Review the assigned change and affected documents, including links, indexes, owning facts, and documented commands. Record scope, inputs, result, and remaining work in existing task proof or evidence. Reuse that review only while valid. After compaction or agent replacement, recover the evidence and review affected work. Agent replacement alone does not require a full review. Use a full consistency review when effects are broad or relevant review evidence cannot be recovered; cover the current project documentation and implementation boundary.

Preserve v1.24.3 document IDs, paths, links, content, and custom rules during upgrade. Do not rewrite project decisions to match a new template. Unknown legacy differences require a bounded review, not silent removal. Historical task contexts continue to resolve to their owning documents.

## Source archives and visuals

Normal source replacement relies on Git; do not create an archive automatically. Create root `archive/` only on explicit user request. Keep `archive/INDEX.md` and `archive/<capability>/<snapshot>/ARCHIVE.md`. Use the existing archive templates. Snapshots remain inert in imports, builds, packaging, and normal tests. Exclude secrets, dependencies, caches, and generated output.

Use a small Mermaid diagram only when it clarifies flow, state, ownership, or dependencies. Use tables for mappings and prose for simple facts. Do not use ASCII diagrams or create a separate documentation archive policy.
