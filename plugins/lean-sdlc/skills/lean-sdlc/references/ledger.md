# Ledger and project control

Root `tasks.csv` is the only durable task plan. Maintainer performs routine writes through the packaged `tasks.py` helper. All roles can use read-only `open`, `show TASK-ID`, `backlog`, and `quick-fixes`. Do not load full Done history for ordinary work.

## Exact context

Use startup fields for repository root, skill root, Tasks helper, Check helper, State helper, Owner, and Child tier. If absent, run `python3 "<directory containing the loaded SKILL.md>/scripts/session_state.py" --context` from the selected repository. Returned keys are `repository_root`, `skill_root`, `tasks_helper`, `check_helper`, `state_helper`, `owner`, and `tier`. Use them exactly. Preserve `CODEX_SESSION_ID`; do not invent an owner or guess between repositories.

Commands below use supplied paths. Grades do not add columns. The schema stays:

`Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence`

## Transactions

Use `python3 "<tasks-helper>" --repo "<repo-root>" COMMAND`:

- `plan`: create unowned Planned work with title, acceptance, proof, and real dependencies.
- `start`: create or claim In Progress work using `--owner` with the Lead owner.
- `update`: correct task facts; active work requires its owner.
- `close`: record accepted evidence using the Lead owner. Only direct user authority permits an ownership override with a reason.
- `backlog-add` and `promote`: add or promote ideas only under direct user authority. Promotion adds proper acceptance and proof, not a raw status flip.
- `quick-fixes`: list completed Quick Fix tasks with pending broad review. Use `close --review-through TASK-ID` only after Verifier review and Lead acceptance.

Backlog rows remain sparse. They contain only ID, title, status, and context; no dependency may target Backlog. A matching implementation request can authorize promotion without an exact ID. Backlog is not execution authority.

Dependencies must exist, be cycle-free, and be Done before start or close. The helper locks, rereads, validates, and atomically replaces the ledger. Preserve durability warnings. Owner IDs coordinate work; they are not a security boundary. A ledger lock does not protect source files.

After ownership is confirmed, run `python3 "<check-helper>" "<repo-root>" --before-write --task TASK-ID --owner OWNER` before the first non-control write. Do not continue on failure. Ordinary status transactions can run asynchronously under [plan](plan.md), but write prerequisites need confirmed results. Maintainer can batch accepted closure and dependent start into one assignment using the existing helper commands in order. A failed prerequisite stops the dependent transaction, not unrelated ready work. Report failures immediately and reconcile actual rows before completion.

## Initialization and upgrade

Control transactions are the task-before-write exception. For an explicitly authorized new project, give Maintainer the selected repository directory and the loaded skill root. Maintainer runs `python3 "<skill-root>/scripts/init_repo.py" "<repo-root>"` before Lead requests startup context. Context discovery needs the initialized core files; do not treat their absence as a missing user decision. Initialization preserves existing files and creates missing core files under the helper's `bootstrap` owner. Then obtain the real session context. Complete bootstrap proof before closing TASK-000 as owner `bootstrap`.

The compatibility baseline is v1.24.3. Retain existing earlier ledger conversions. `tasks.py ... upgrade --task TASK-ID --owner OWNER` converts the supported Parent or lowercase planning header. Conflicting root and planning ledgers stop without selecting one silently. Preserve IDs, owners, dependencies, acceptance, proof, evidence, and pending reviews.

For an authorized contract upgrade, use `init_repo.py ... --upgrade-contract --task TASK-ID --owner OWNER`. It replaces the recognized released instruction contract and preserves surrounding custom rules. Unknown modifications require review, not overwrite. `--repair-startup` repairs only a missing or stale managed block; it does not remove obsolete rules outside that block.

Use `session_state.py --owner OWNER --upgrade` to remove retired fields while preserving the child-tier preference. No field selects a workflow. Repeating a completed upgrade must not change project data.

After upgrade, read the current entry and applicable instructions, run the structural check, and continue the authorized task. An upgrade alone does not authorize unrelated work. Preserve recovery copies when changing existing contracts; never fabricate historical evidence or silently reassign unfinished work.
