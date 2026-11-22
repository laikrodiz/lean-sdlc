# Storage Review

Only on request, review the selected project without writes, initialization, tasks, or a saved report. Never move, delete, rebuild, or upload during review.

Start with shallow allocated sizes where available. Inspect only the largest unresolved contributors. Stop when metadata and build references settle the decision. Stay inside the project; skip external links and cloud-only files. Never probe private or unknown payloads, even to identify their type.

Use metadata and relevant build references to identify producers, required paths, local-only work, and recovery sources. Age, names, Git ignore rules, and remotes do not prove recovery. Hash only to verify a specific retained copy. Equal bytes do not make paths interchangeable; do not deduplicate differing test trees.

Report named batches: exact paths, measured size, dependencies, recovery evidence and cost, and one decision:

- **Propose removal:** No required path or unique data; recovery established.
- **Preserve first:** Mixed outputs, unique artifacts, tools, or evidence lack a verified retained copy.
- **Leave alone:** Active, necessary, private, or uncertain.

Distinguish measured size from likely reclaim; shared blocks or snapshots can reduce savings. If nothing qualifies, say so. Stop at the proposal.

Only separate approval authorizes action on named paths. Immediately recheck scope, contents, active use, and recovery evidence. Skip changed or uncertain targets. Never expand a batch with wildcards.
