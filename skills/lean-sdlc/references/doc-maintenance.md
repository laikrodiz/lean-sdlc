# Documentation Maintenance Workflow

Use when the authoritative meaning is already known and approved documents need exact synchronization, movement, deletion, splitting, or index repair. Route uncertain ownership or contradictions to traceability, feature-boundary changes to refinement, and stage/version decisions to versioning.

Use Luna at `low` for exact synchronization and Terra at `high` for semantic cleanup. Use Sol only when cleanup exposes a new meaning decision, then route to its owning lane.

## Workflow

1. Identify the already-approved source of truth.
2. Update only documents whose representation is stale.
3. Synchronize feature and decision indexes with existing files.
4. Move mappings, commands, recipes, and local detail to their established owner.
5. Split files only along already-approved responsibility boundaries.
6. Create optional docs only under repeated shared pressure.
7. Delete dead text and stale placeholders.
8. Run the structural checker after changes.

Do not decide new scope, acceptance, feature boundaries, architecture, or version meaning in this lane. Escalate those discoveries to the appropriate workflow.

Success means the repository presents settled truth once, in the correct place, without stale planning debris.
