# Shape

Use Shape when problem, user, value, behavior, scope, stage, or version promise is unclear.

## Intent contract

Shape owns the complete intent gate. Before the Architect creates a task or mutates the repository, the Architect naturally confirms `why -> what -> how -> proof`. Shape settles Why and What. Decide and Plan add How and Proof before task creation or mutation:

Intent fact order: `<reason> -> <outcome> -> <boundary> -> <approach> -> <proof>`.

Angle-bracket terms are abstract fact slots. Replace them with project facts; never copy the wording or show slot labels.

- Why: the present problem or opportunity and affected user or business value.
- What: the smallest observable outcome plus constraints and non-goals.
- How: the technical approach and task shape after Why and What are stable.
- Proof: acceptance and verification that show the outcome.

Use natural prose. Do not require fixed headings. If a material assumption affects behavior, scope, or architecture, stop for user confirmation. If intent is clear and implementation authority is explicit, continue without another round trip. Brainstorming and rephrasing remain read-only.

Read `docs/PROJECT.md` and behavior documents. Identify the problem, affected user, outcome, boundaries, and acceptance. Classify boundary cases as `Handle`, `Reject`, `Defer`, or `Impossible by invariant`.

## Project and Feature boundaries

Group the current outcome in the project promise. Use an optional Feature document when one durable behavior spans tasks. Split a Feature when a part has an independent promise, test, or change. Merge Feature candidates when neither part has useful behavior alone.

Ready means the smallest outcome, boundary, acceptance, and promise are clear enough to decide or plan.

For optional documentation, use the concrete need-based triggers and semantic sizing in the repository contract. Keep `docs/PROJECT.md` as the only mandatory shared project document. If a document trigger or split changes meaning, stop for Architect approval.
