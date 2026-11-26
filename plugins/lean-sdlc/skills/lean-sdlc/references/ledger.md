# Ledger and project control

Root `tasks.csv` is the only durable task plan. Lead performs all task writes directly through packaged `tasks.py`. Never delegate routine transactions or require a reconciliation agent. Use `overview` for current work, backlog titles, and pending reviews; `show TASK-ID` for missing details. Reuse returned facts. Refresh affected state after ambiguous results, possible concurrent changes, interruption, or lost context.

## Exact context

Use the entry’s exact startup values: `repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, and `tier`.

Record the settled grade with `--grade Simple|Normal|Complex` on plan, new start, or promotion. Correct it through update if scope changes. Older ledgers remain readable. The next write adds the Grade column and leaves unknown historical grades blank.

## Transactions

Use `python3 "<tasks-helper>" --repo "<repo-root>" COMMAND`:

- `plan`: create unowned Planned work with title, acceptance, proof, and real dependencies.
- `start --check`: create or claim In Progress work using `--owner` with the Lead owner; pass the full before-write check before saving.
- `update`: correct task facts; active work requires its owner.
- `close`: record accepted evidence using the Lead owner. Only direct user authority permits an ownership override with a reason.
- `backlog-add` and `promote`: add or promote ideas only under direct user authority. Promotion adds proper acceptance and proof, not a raw status flip.
- `quick-fixes`: list completed Quick Fix tasks with pending broad review. Use `close --review-through TASK-ID` only after Verifier review and Lead acceptance.

Backlog rows remain sparse. They contain only ID, title, status, and context; no dependency may target Backlog. A matching implementation request can authorize promotion without an exact ID. Backlog is not execution authority.

Dependencies must exist, be cycle-free, and be Done before start or close. The helper locks, rereads, validates, and atomically replaces the ledger. Preserve durability warnings. Owner IDs coordinate work; they are not a security boundary. A ledger lock does not protect source files.

For one ready authorized task, use `start --check` directly before the first non-control write. Its returned row confirms ownership and the gate; skip redundant `plan` and `show`. Failed validation leaves the ledger unchanged. For already-active work or control-only promotion, run `python3 "<check-helper>" "<repo-root>" --before-write --task TASK-ID --owner OWNER`. Stop on failure. Confirm closure before dependent work. Reconcile records against accepted results. The helper validates records, not whether the original request was fulfilled. Lead corrects omissions; Maintainer may investigate substantial discrepancies without writing records.

## Initialization and upgrade

Control transactions are the task-before-write exception. For an explicitly authorized new project, Lead runs `python3 "<skill-root>/scripts/init_repo.py" "<repo-root>"` in the selected repository before requesting startup context. Context discovery needs the initialized core files; do not treat their absence as a missing user decision. Initialization preserves existing files and creates missing core files under the helper's `bootstrap` owner. Then obtain the real session context. Complete bootstrap proof before closing TASK-000 as owner `bootstrap`.

The compatibility baseline is v1.24.3. Retain existing earlier ledger conversions. `tasks.py ... upgrade --task TASK-ID --owner OWNER` converts the supported Parent or lowercase planning header. Conflicting root and planning ledgers stop without selecting one silently. Preserve IDs, owners, dependencies, acceptance, proof, evidence, and pending reviews.

For an authorized contract upgrade, use `init_repo.py ... --upgrade-contract --task TASK-ID --owner OWNER`. It replaces the recognized released instruction contract and preserves surrounding custom rules. Unknown modifications require review, not overwrite. `--repair-startup` repairs only a missing or stale managed block; it does not remove obsolete rules outside that block.

Use `session_state.py --owner OWNER --upgrade` to remove retired fields while preserving the child-tier preference. No field selects a workflow. Repeating a completed upgrade must not change project data.

After a plugin upgrade, discard cached helper paths. From the selected repository, refresh startup context using the new installation's `session_state.py --context` before any helper call. After upgrade, read the current entry and applicable instructions, run the structural check, and continue the authorized task. An upgrade alone does not authorize unrelated work. Preserve recovery copies when changing existing contracts; never fabricate historical evidence or silently reassign unfinished work.

### Missing installed helper

After verifying the replacement installation, run from the original repository. Pass the successful listing unchanged on standard input:

```sh
catalog=$(codex plugin list --marketplace lean-sdlc --json) &&
  printf '%s\n' "$catalog" | python3 -B "<verified-skill-root>/scripts/session_state.py" --recover-context "<previous-repository-root>" "<previous-owner>"
```

Keep the same session. On failure, stop without edits. On success, reload the entry and applicable rules, honor contract checks, and inspect the affected task. Retry a missing start once only if still authorized and not already applied. For an owned active task, run the before-write gate. Never replay a close, create, or delivery with uncertain effects.

### Existing projects and release notices

Startup compares the project's managed block with the loaded template offline. On review or conflicting ledgers, stop affected writes. Never use repair to bypass review. Keep historical documents and local rules. During an authorized documentation upgrade, add topic pointers to PROJECT from existing sources; do not reconstruct missing reasons. Preview any proposed move or deletion separately.

Default: pinned. At the user's explicit request, run `scripts/updates.py follow-stable` once on the workstation using Python; `pin` turns it off. In follow-stable mode, on authorized execution run `updates.py refresh`. It checks official stable tags at most once per day. Offline, use the cached result. If the reported version exceeds the installed version, notify; do not install packages or trust hooks. Read-only work never refreshes or migrates.

Follow-stable is standing permission to upgrade an exact recognized managed block on the next authorized edit, only from the reviewed, installed stable plugin. Do not migrate from an experimental checkout, an untrusted install, or a project that declares a version pin. Claim a separate control task with `start` (no product edits). Recheck the exact known block before the existing upgrade command above; never use the control exception for product writes. Inspect preserved custom rules and check the project before product edits. Unknown edits and legacy ledger conflicts need a user decision.
