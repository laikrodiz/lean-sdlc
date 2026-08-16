from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/lean-sdlc"
SKILL = PLUGIN / "skills/lean-sdlc"
SCRIPTS = SKILL / "scripts"
TASKS = SCRIPTS / "tasks.py"
CHECK = SCRIPTS / "lean_check.py"
INIT = SCRIPTS / "init_repo.py"
OWNER_HOOK = SCRIPTS / "session_state.py"
PLUGIN_HOOKS = PLUGIN / "hooks/hooks.json"
HEADER = (
    "Task ID,Title,Status,Context,Dependencies,Owner,"
    "Acceptance Criteria,Proof,Evidence\n"
)


def run(*arguments: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def task(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return run(str(TASKS), "--repo", str(repository), *arguments)


def write_ledger(repository: Path, body: str, *, legacy_path: bool = False) -> Path:
    path = (
        repository / "planning/tasks.csv"
        if legacy_path
        else repository / "tasks.csv"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def read_rows(repository: Path) -> list[dict[str, str]]:
    with (repository / "tasks.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class TaskLedgerTests(unittest.TestCase):
    def test_concurrent_plan_and_start_transactions_get_unique_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            processes: list[subprocess.Popen[str]] = []
            for number in range(12):
                command = [
                    sys.executable,
                    str(TASKS),
                    "--repo",
                    str(repository),
                    "start" if number % 2 else "plan",
                    "--title",
                    f"Task {number}",
                    "--context",
                    "Project",
                    "--acceptance",
                    "Row exists",
                    "--proof",
                    "Read ledger",
                ]
                if number % 2:
                    command.extend(["--owner", "12345678"])
                processes.append(
                    subprocess.Popen(
                        command,
                        cwd=ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    )
                )

            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(
                all(process.returncode == 0 for process in processes),
                results,
            )
            rows = read_rows(repository)
            ids = [row["Task ID"] for row in rows]
            self.assertEqual(len(ids), 12)
            self.assertEqual(len(set(ids)), 12)
            self.assertEqual(
                {row["Owner"] for row in rows if row["Status"] == "In Progress"},
                {"12345678"},
            )
            self.assertFalse(repository.joinpath(".tasks.lock").exists())

    def test_planned_work_updates_then_starts_under_one_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            planned = task(
                repository,
                "plan",
                "--title",
                "Initial title",
                "--context",
                "Project",
                "--acceptance",
                "Done",
                "--proof",
                "Run checks",
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)

            updated = task(
                repository,
                "update",
                "TASK-000",
                "--title",
                "Corrected title",
            )
            self.assertEqual(updated.returncode, 0, updated.stderr)

            started = task(
                repository,
                "start",
                "TASK-000",
                "--owner",
                "12345678",
            )
            self.assertEqual(started.returncode, 0, started.stderr)

            denied = task(
                repository,
                "update",
                "TASK-000",
                "--owner",
                "87654321",
                "--title",
                "Wrong owner",
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("belongs to owner 12345678", denied.stderr)

            allowed = task(
                repository,
                "update",
                "TASK-000",
                "--owner",
                "12345678",
                "--proof",
                "Run the final checks",
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Title"], "Corrected title")
            self.assertEqual(row["Owner"], "12345678")
            self.assertEqual(row["Status"], "In Progress")

    def test_one_owner_can_hold_two_parallel_tasks_under_before_write_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Module A,In Progress,Project,,12345678,"
                "Module A passes,Run module A checks,\n"
                "TASK-000,Module B,In Progress,Project,,12345678,"
                "Module B passes,Run module B checks,\n",
            )

            for task_id in ("TASK-001", "TASK-000"):
                checked = run(
                    str(CHECK),
                    str(repository),
                    "--before-write",
                    "--task",
                    task_id,
                    "--owner",
                    "12345678",
                )
                self.assertEqual(
                    checked.returncode,
                    0,
                    checked.stdout + checked.stderr,
                )

            first = task(
                repository,
                "update",
                "TASK-001",
                "--owner",
                "12345678",
                "--proof",
                "Run module A checks again",
            )
            second = task(
                repository,
                "update",
                "TASK-000",
                "--owner",
                "12345678",
                "--proof",
                "Run module B checks again",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(
                {row["Owner"] for row in read_rows(repository)},
                {"12345678"},
            )

    def test_only_owner_closes_without_direct_user_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Owned work,In Progress,Project,,11111111,"
                "Done,Run checks,\n",
            )
            denied = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("belongs to owner 11111111", denied.stderr)

            allowed = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
                "--user-override",
                "--override-reason",
                "User requested closure in this task",
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Status"], "Done")
            self.assertIn("Direct user override", row["Evidence"])

    def test_dependencies_must_exist_remain_acyclic_and_finish_before_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            first = task(
                repository,
                "plan",
                "--title",
                "First",
                "--context",
                "Project",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertEqual(first.returncode, 0, first.stderr)

            second = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Second",
                "--context",
                "Project",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertEqual(second.returncode, 0, second.stderr)

            linked = task(
                repository,
                "update",
                "TASK-001",
                "--owner",
                "12345678",
                "--dependencies",
                "TASK-000",
            )
            self.assertEqual(linked.returncode, 0, linked.stderr)

            blocked_close = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "12345678",
                "--evidence",
                "Done",
            )
            self.assertNotEqual(blocked_close.returncode, 0)
            self.assertIn("unfinished dependencies", blocked_close.stderr)

            cycle = task(
                repository,
                "update",
                "TASK-000",
                "--dependencies",
                "TASK-001",
            )
            self.assertNotEqual(cycle.returncode, 0)
            self.assertIn("dependency cycle", cycle.stderr)

            missing = task(
                repository,
                "plan",
                "--title",
                "Missing dependency",
                "--context",
                "Project",
                "--dependencies",
                "TASK-999",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("depends on missing task TASK-999", missing.stderr)

            self.assertEqual(len(read_rows(repository)), 2)

    def test_planned_start_rejects_unfinished_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Dependency,Planned,Project,,,"
                "Ready,Check,\n"
                "TASK-000,Child,Planned,Project,TASK-001,,Ready,Check,\n",
            )

            result = task(repository, "start", "TASK-000", "--owner", "12345678")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unfinished dependencies: TASK-001", result.stderr)
            rows = read_rows(repository)
            self.assertEqual(rows[1]["Status"], "Planned")
            self.assertEqual(rows[1]["Owner"], "")

    def test_immediate_start_rejects_unfinished_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-000,Dependency,Planned,Project,,,"
                "Ready,Check,\n",
            )

            result = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Child",
                "--context",
                "Project",
                "--dependencies",
                "TASK-000",
                "--acceptance",
                "Ready",
                "--proof",
                "Check",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unfinished dependencies: TASK-000", result.stderr)
            rows = read_rows(repository)
            self.assertEqual([row["Task ID"] for row in rows], ["TASK-000"])

    def test_immediate_start_keeps_missing_dependency_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            result = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Child",
                "--context",
                "Project",
                "--dependencies",
                "TASK-999",
                "--acceptance",
                "Ready",
                "--proof",
                "Check",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("depends on missing task TASK-999", result.stderr)
            self.assertEqual(read_rows(repository), [])

    def test_open_prints_header_and_only_planned_or_in_progress_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-003,Closed,Done,Project,,11111111,Done,Check,Evidence\n"
                "TASK-002,Planned,Planned,Project,,,Ready,Check,\n"
                "TASK-001,Active,In Progress,Project,,12345678,Ready,Check,\n",
            )
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")

            result = task(repository, "open")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout,
                HEADER
                + "TASK-002,Planned,Planned,Project,,,Ready,Check,\n"
                + "TASK-001,Active,In Progress,Project,,12345678,Ready,Check,\n",
            )
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

    def test_show_prints_selected_task_then_recursive_dependencies_in_field_order(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-004,Selected,In Progress,Project,TASK-002 TASK-001,"
                "12345678,Ready,Check,\n"
                "TASK-003,Unrelated,Done,Project,,11111111,Done,Check,Evidence\n"
                "TASK-002,First dependency,Done,Project,TASK-000,11111111,"
                "Done,Check,Evidence\n"
                "TASK-001,Second dependency,Planned,Project,TASK-000,,"
                "Ready,Check,\n"
                "TASK-000,Root dependency,Done,Project,,11111111,Done,"
                "Check,Evidence\n",
            )

            first = task(repository, "show", "TASK-004")
            second = task(repository, "show", "TASK-004")

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(first.stdout.splitlines()[0] + "\n", HEADER)
            self.assertEqual(
                [row["Task ID"] for row in csv.DictReader(first.stdout.splitlines())],
                ["TASK-004", "TASK-002", "TASK-000", "TASK-001"],
            )

    def test_show_missing_task_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-000,Existing,Planned,Project,,,Ready,Check,\n",
            )

            result = task(repository, "show", "TASK-999")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task does not exist: TASK-999", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_read_commands_leave_ledger_unchanged_and_writes_still_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")

            self.assertEqual(task(repository, "open").returncode, 0)
            self.assertEqual(task(repository, "show", "TASK-000").returncode, 1)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

            planned = task(
                repository,
                "plan",
                "--title",
                "New work",
                "--context",
                "Project",
                "--acceptance",
                "Ready",
                "--proof",
                "Check",
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            started = task(
                repository,
                "start",
                "TASK-000",
                "--owner",
                "12345678",
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            self.assertEqual(read_rows(repository)[0]["Status"], "In Progress")
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8").splitlines()[0],
                HEADER.strip(),
            )

    def test_legacy_path_and_header_upgrade_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            planning = repository / "planning"
            planning.mkdir()
            legacy = planning / "tasks.csv"
            legacy.write_text(
                "task_id,title,status,parent_ref,depends_on,owner,"
                "acceptance,proof,evidence\n"
                "TASK-001,Upgrade,In Progress,REPO,,11111111,"
                "Readable,Inspect,\n",
                encoding="utf-8",
            )
            result = task(
                repository,
                "upgrade",
                "--task",
                "TASK-001",
                "--owner",
                "11111111",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            root_ledger = repository / "tasks.csv"
            self.assertTrue(root_ledger.is_file())
            self.assertEqual(
                root_ledger.read_text(encoding="utf-8").splitlines()[0],
                HEADER.strip(),
            )
            self.assertFalse(legacy.exists())
            self.assertFalse(planning.exists())

    def test_previous_root_header_upgrade_maps_parent_to_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            old_header = (
                "Task ID,Title,Status,Parent,Dependencies,Owner,"
                "Acceptance Criteria,Proof,Evidence\n"
            )
            repository.joinpath("tasks.csv").write_text(
                old_header
                + "TASK-001,Upgrade,In Progress,REPO,,11111111,"
                "Readable,Inspect,\n",
                encoding="utf-8",
            )

            result = task(
                repository,
                "upgrade",
                "--task",
                "TASK-001",
                "--owner",
                "11111111",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            root_ledger = repository / "tasks.csv"
            self.assertEqual(
                root_ledger.read_text(encoding="utf-8").splitlines()[0],
                HEADER.strip(),
            )
            self.assertEqual(read_rows(repository)[0]["Context"], "Project")
            self.assertFalse(repository.joinpath(".tasks.lock").exists())

    def test_checker_rejects_manual_dependency_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,One,Planned,Project,TASK-002,,Done,Check,\n"
                "TASK-002,Two,Planned,Project,TASK-001,,Done,Check,\n",
            )
            checked = run(str(CHECK), str(repository), "--task", "TASK-001")
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("dependency cycle", checked.stdout)

    def test_owner_hook_is_stable_and_plugin_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            repository.joinpath("AGENTS.md").write_text(
                "Use $lean-sdlc for repository work.\n",
                encoding="utf-8",
            )
            write_ledger(repository, "")
            nested = repository / "src"
            nested.mkdir()
            event = json.dumps(
                {
                    "session_id": "019f71b5-b7e1-78f2-a426-1b7a95d87348",
                    "hook_event_name": "SessionStart",
                    "cwd": str(nested),
                    "model": "test",
                }
            )
            first = run(str(OWNER_HOOK), input_text=event)
            second = run(str(OWNER_HOOK), input_text=event)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            message = json.loads(first.stdout)["systemMessage"]
            owner = message.split(": ", 1)[1].split(".", 1)[0]
            self.assertRegex(owner, r"^\d{8}$")

        with tempfile.TemporaryDirectory() as directory:
            outside = json.dumps(
                {
                    "session_id": "019f71b5-b7e1-78f2-a426-1b7a95d87348",
                    "hook_event_name": "SessionStart",
                    "cwd": directory,
                    "model": "test",
                }
            )
            quiet = run(str(OWNER_HOOK), input_text=outside)
            self.assertEqual(quiet.returncode, 0, quiet.stderr)
            self.assertEqual(quiet.stdout, "")

        hooks = json.loads(PLUGIN_HOOKS.read_text(encoding="utf-8"))
        command = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("${PLUGIN_ROOT}", command)
        self.assertIn("session_state.py", command)
        self.assertNotIn("CODEX_HOME", command)
        pre_tool_use = hooks["hooks"]["PreToolUse"][0]
        self.assertEqual(pre_tool_use["matcher"], "Agent")
        self.assertIn("spawn_guard.py", pre_tool_use["hooks"][0]["command"])

    def test_initializer_creates_only_minimal_contract_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            first = run(str(INIT), str(repository))
            self.assertEqual(first.returncode, 0, first.stderr)

            self.assertTrue(repository.joinpath("AGENTS.md").is_file())
            self.assertTrue(repository.joinpath("docs/PROJECT.md").is_file())
            self.assertTrue(repository.joinpath("tasks.csv").is_file())
            ignores = repository.joinpath(".gitignore").read_text(encoding="utf-8")
            self.assertIn("/tasks.csv", ignores.splitlines())
            self.assertIn("/.tasks.lock", ignores.splitlines())
            self.assertFalse(repository.joinpath("README.md").exists())
            self.assertFalse(repository.joinpath(".codex/hooks.json").exists())
            self.assertFalse(repository.joinpath("docs/OPERATIONS.md").exists())
            self.assertFalse(repository.joinpath("docs/FEATURE_INDEX.csv").exists())
            self.assertFalse(repository.joinpath("docs/DECISION_INDEX.csv").exists())

            before_write = run(
                str(CHECK),
                str(repository),
                "--before-write",
                "--task",
                "TASK-000",
                "--owner",
                "bootstrap",
            )
            self.assertEqual(
                before_write.returncode,
                0,
                before_write.stdout + before_write.stderr,
            )
            full = run(str(CHECK), str(repository), "--task", "TASK-000")
            self.assertEqual(full.returncode, 0, full.stdout + full.stderr)

            closed = task(
                repository,
                "close",
                "TASK-000",
                "--owner",
                "bootstrap",
                "--evidence",
                "Minimal contract checked",
            )
            self.assertEqual(closed.returncode, 0, closed.stderr)

            repeated = run(str(INIT), str(repository))
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("0 control change(s)", repeated.stdout)
            self.assertEqual(len(read_rows(repository)), 1)

    def test_initializer_preserves_existing_project_truth(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            docs = repository / "docs"
            docs.mkdir()
            repository.joinpath("AGENTS.md").write_text("existing rules\n", encoding="utf-8")
            docs.joinpath("PROJECT.md").write_text("existing truth\n", encoding="utf-8")
            repository.joinpath(".gitignore").write_text(
                "dist/\n/tasks.csv\n",
                encoding="utf-8",
            )

            initialized = run(str(INIT), str(repository))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                "existing rules\n",
            )
            self.assertEqual(
                docs.joinpath("PROJECT.md").read_text(encoding="utf-8"),
                "existing truth\n",
            )
            ignores = repository.joinpath(".gitignore").read_text(encoding="utf-8")
            self.assertEqual(
                ignores.splitlines(),
                ["dist/", "/tasks.csv", "/.tasks.lock"],
            )


class PackageContractTests(unittest.TestCase):
    def test_package_contains_one_skill_and_no_legacy_lanes(self) -> None:
        self.assertEqual(
            {path.name for path in PLUGIN.iterdir()},
            {".codex-plugin", "hooks", "skills"},
        )
        self.assertFalse(
            any(
                path.name in {"__pycache__", ".DS_Store"} or path.suffix == ".pyc"
                for path in PLUGIN.rglob("*")
            )
        )

        skill_roots = sorted(
            path.parent.name for path in PLUGIN.glob("skills/*/SKILL.md")
        )
        self.assertEqual(skill_roots, ["lean-sdlc"])

        references = SKILL / "references"
        names = {path.name for path in references.glob("*.md")}
        self.assertTrue(
            {
                "shape.md",
                "decide.md",
                "plan.md",
                "diagnose.md",
                "deliver.md",
                "verify.md",
                "model-routing.md",
                "subagents.md",
                "operations.md",
                "repository-contracts.md",
                "trigger-evals.md",
            }.issubset(names)
        )
        self.assertNotIn("agent-coordination.md", names)
        self.assertTrue(
            names.isdisjoint(
                {
                    "brainstorm.md",
                    "refine.md",
                    "architecture.md",
                    "task-planning.md",
                    "execution.md",
                    "debugging.md",
                    "implementation.md",
                    "verification.md",
                    "traceability.md",
                    "versioning.md",
                    "doc-maintenance.md",
                    "lifecycle.md",
                }
            )
        )

    def test_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        for document in SKILL.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = (document.parent / target.split("#", 1)[0]).resolve()
                if not path.exists():
                    failures.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])

    def test_dispatcher_trigger_is_explicit_and_model_floor_has_no_assignment_to_low(
        self,
    ) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = dispatcher.split("---", 2)[1]
        self.assertIn("explicitly invokes Lean-SDLC", frontmatter)
        self.assertIn("repository AGENTS.md requires Lean-SDLC", frontmatter)
        self.assertIn("Do not invoke implicitly for read-only work", frontmatter)

        policy_files = [
            ROOT / "README.md",
            SKILL / "assets/AGENTS.md",
            SKILL / "references/model-routing.md",
            SKILL / "references/subagents.md",
        ]
        policy = "\n".join(path.read_text(encoding="utf-8") for path in policy_files)
        self.assertNotIn("GPT-5.4", policy)
        self.assertNotRegex(policy, r"\|\s*`?low`?\s*\|")

    def test_minimal_modularity_edge_cases_and_diagrams_are_explicit(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        decide = (SKILL / "references/decide.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        self.assertIn("smallest cohesive units", dispatcher)
        self.assertIn("project-size", decide)
        self.assertIn("readable orchestrator", deliver)
        self.assertIn("handle", deliver)
        self.assertIn("reject", deliver)
        self.assertIn("defer", deliver)
        self.assertIn("impossible by invariant", deliver)
        self.assertIn("change locality", verify)
        self.assertIn("mermaid", contracts)
        self.assertIn("ascii pseudographics", contracts)
        self.assertIn("plausible edge cases", evaluations)

    def test_work_boundaries_keep_tasks_atomic_and_steps_transient(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        template = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        decide = (SKILL / "references/decide.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        self.assertIn(
            "each task is one independently accepted repository state; local implementation steps stay transient.",
            dispatcher,
        )
        self.assertIn(
            "each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.",
            agents,
        )
        self.assertIn(
            "split independently accepted and independently proved work. keep inseparable coding steps transient.",
            agents,
        )
        self.assertEqual(agents, template)

        for phrase in [
            "group the current outcome in the project promise.",
            "use an optional feature document when one durable behavior spans tasks.",
            "split a feature when a part has an independent promise, test, or change.",
            "merge feature candidates when neither part has useful behavior alone.",
        ]:
            self.assertIn(phrase, shape)

        self.assertIn(
            "record one decision for one independent reversal boundary.",
            decide,
        )
        self.assertIn(
            "keep a choice local when it is cheap to reverse and clear in code, tests, or technical documentation.",
            decide,
        )

        for phrase in [
            "one ledger task represents one engineer checkpoint.",
            "require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review.",
            "keep one task resumable from repository truth and its ledger row after compaction.",
            "split a task for independent behavior, module outcome, proof, or work that needs an architect checkpoint.",
            "split a task when a part can fail, ship, revert, resume, or close independently, crosses a contract, or needs another durable decision.",
            "merge pieces without independent value or proof.",
            "keep implementation tests inside the task.",
            "keep maintainer and verifier work attached unless it is independently deliverable.",
            "keep acceptance corrections in the current task.",
            "create a new task for new behavior or a new decision.",
            "do not use time or line-count limits.",
            "shape the nearest dependency frontier fully. keep later work coarse until its dependencies become current.",
            "use [subagents.md](subagents.md) for child triggers, scheduling, handoffs, profiles, checkpoints, and reporting.",
            "keep local implementation steps and correction handoffs transient.",
            "never send several tasks or an internal backlog.",
        ]:
            self.assertIn(phrase, plan)

        for phrase in [
            "## work hierarchy",
            "- project promise: current outcome, scope, stage, and exit evidence.",
            "- feature: durable behavior that spans tasks.",
            "- task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.",
            "- local step: transient implementation or correction work that does not become a ledger row.",
            "## task sizing summary",
            "split or merge tasks by the independent boundaries in [plan.md](plan.md).",
        ]:
            self.assertIn(phrase, contracts)

        self.assertIn("assisted parallel work", evaluations)
        self.assertIn("verifier and maintainer sidecars", evaluations)

    def test_task_sizing_and_session_state_routes_use_canonical_sources(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        self.assertIn("valid engineer checkpoint", evaluations)
        self.assertIn("oversized task", evaluations)
        for token in [
            "scripts/session_state.py --owner owner --mode assisted|solo",
            "scripts/session_state.py --owner owner --fast-children",
            "--no-fast-children",
        ]:
            self.assertIn(token, dispatcher + subagents)

    def test_implementation_authority_and_visible_plan_gate_are_explicit(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()

        for phrase in [
            "require the information, not fixed labels",
            "use natural prose for the outcome, important constraints, and exclusions",
            "only the plan needs visible structure",
            "before creating a task or implementing work",
            "natural intent confirmation",
            "concise visible plan",
            "define each durable plan item in natural prose",
            "observable completion condition and verification method",
            "the verification method is its proof",
            "each durable item includes observable completion conditions and proof",
            "a one-item plan is valid",
            "only durable task plan",
        ]:
            self.assertIn(phrase, plan)

        self.assertIn("explicit implementation authority", dispatcher + shape + deliver)
        self.assertIn("discussion or proposal requests remain read-only", shape + deliver)
        self.assertIn("clear confirmation to proceed against a recoverable agreed proposal", dispatcher + shape + subagents)
        self.assertIn("if authority is ambiguous, remain read-only", dispatcher + shape + subagents)
        self.assertIn("each durable plan item maps to one task", plan)
        self.assertIn("keep local implementation steps and correction handoffs transient", plan + subagents)

        self.assertIn(
            "engineer cannot start until the visible plan exists",
            subagents,
        )
        self.assertIn(
            "the task matches one durable plan item",
            plan + subagents + deliver,
        )
        self.assertIn(
            "discussion, proposal, or non-concrete proceed request",
            evaluations,
        )
        self.assertIn("task or implementation request", evaluations)
        self.assertIn("valid engineer checkpoint", evaluations)
        self.assertIn("engineer direct path", evaluations)
        self.assertEqual(root_agents, template_agents)

    def test_subagent_policy_is_canonical_deterministic_and_explicit(
        self,
    ) -> None:
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        for term in [
            "sole authority",
            "role-trigger matrix",
            "independence gate",
            "at most two active children",
            "universal independence gate",
            "engineer/engineer",
            "engineer/scout",
            "scout/scout",
            "scout may overlap one verifier or maintainer only for future work with separate resources",
            "at most one reusable verifier",
            "at most one reusable maintainer",
            "implementation writers stop before integration",
            "documentation synchronization",
            "stateful operations",
            "no writer overlaps documentation synchronization, verification, or stateful operations",
            "named architect decision requires distinct source sets or enough material, data, or logs to pollute lead context",
            "direct user authority",
            "one mechanical bounded change",
            "shared handoff envelope",
            "outcome, boundary, contract, proof, and stop conditions",
            "without a fixed runtime template",
            "the architect owns each child name at spawn time",
            "allocates the next never-used label",
            "task_name=engineer_beta",
            "context reset reason",
            "replacement action",
            "rehydrate an allowed replacement",
            "counter-based",
            "before every spawn",
            "routing failure",
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "user-selected lead",
            "model=gpt-5.6-luna",
            "reasoning_effort=max",
            "non-full-history `fork_turns`",
            "omit `agent_type`",
            "luna max uses standard service by default",
            "normal spawns omit `service_tier`",
            "service_tier=priority",
            "material phase changes",
            "at most two useful heartbeats",
            "every child update starts with work or current state",
            "maintainer synchronizes affected shared narrative documents",
            "no child edits `tasks.csv`",
        ]:
            self.assertIn(term, subagents)
        for term in [
            "acceptance-defining proof",
            "one planned regression command",
            "full suite once under verifier only when the task or repository contract requires it",
        ]:
            self.assertIn(term, verify)
        for term in [
            "assisted parallel work",
            "custom role request",
        ]:
            self.assertIn(term, evaluations)
        self.assertIn("retry luna max", subagents)
        self.assertIn("shorthand tool names", verify)

        policy_documents = [ROOT / "README.md", ROOT / "docs/PROJECT.md", *SKILL.rglob("*.md")]
        policy = "\n".join(
            document.read_text(encoding="utf-8").lower()
            for document in policy_documents
        )
        self.assertNotIn("operator", policy)
        self.assertNotIn("service_tier=fast", policy)
        self.assertNotIn("gpt-5.6 terra `high`", policy)
        self.assertNotIn("explicitly spawn terra `high`", policy)

        for document in policy_documents:
            for line in document.read_text(encoding="utf-8").splitlines():
                self.assertNotIn(
                    "luna `xhigh`",
                    line.lower(),
                    f"{document}: {line}",
                )

    def test_intent_contract_owners_and_architect_boundary_are_explicit(self) -> None:
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        decide = (SKILL / "references/decide.md").read_text(encoding="utf-8").lower()
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8").lower()
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        for phrase in [
            "shape owns the complete intent gate",
            "why -> what -> how -> proof",
            "present problem or opportunity",
            "affected user or business value",
            "shape settles why and what",
            "decide and plan add how and proof",
            "smallest observable outcome plus constraints and non-goals",
            "technical approach and task shape after why and what are stable",
            "proof: acceptance and verification",
            "material assumption affects behavior, scope, or architecture",
            "stop for user confirmation",
            "intent is clear and implementation authority is explicit",
            "brainstorming and rephrasing remain read-only",
        ]:
            self.assertIn(phrase, shape)
        self.assertIn("derive observable acceptance from the confirmed outcome and affected value", plan)
        self.assertIn(
            "implementation mechanisms, changed files, and test commands support acceptance but do not define it alone",
            plan,
        )
        for phrase in [
            "when at least two tasks are ready",
            "checks the next ready pair",
            "resource gate passes",
            "elapsed time should decrease",
            "name the shared resource or dependency",
            "do not score the choice or add a mode",
        ]:
            self.assertIn(phrase, plan)
        self.assertIn("tie each technical choice to the confirmed intent or constraint it serves", decide)
        for phrase in [
            "project purpose, value, behavior boundary, scope, stage, and version promise",
            "durable behavior detail",
            "technical rationale and durable costly choice",
            "local corrections -> outcome-focused task truth",
            "keep durable intent in these existing owners",
            "do not add a file or task column for intent",
            "dependencies must exist, remain acyclic, and be `done` before start or close",
            "the ledger lock is not a source-file lock",
            "one root `tasks.csv` remains authoritative",
            "two ready tasks for one architect owner",
        ]:
            self.assertIn(phrase, contracts)
        for phrase in [
            "the architect always owns intent, public behavior, architecture, tasks, acceptance, integration, and closeout",
            "never sends unresolved user input to a child",
            "writes inside an active child boundary",
            "accepts unreviewed output",
            "replaces independent proof with confidence",
            "assisted mode normally delegates routine discovery, evidence, implementation, checks, documentation, and recorded operations",
            "architect may implement under these exceptions",
            "after explicit user direction that the architect itself implement",
            "after the required child and fallback are unavailable",
            "settled separable work remains engineer work",
            "each child handoff begins with a short settled purpose",
            "at most two active children",
            "resource gate passes",
            "all dependencies are `done`",
            "separate mutable code and test paths",
            "stable read paths",
            "incidental outputs or caches",
            "public interface, schema, manifest, lockfile, generator, migration, or mutable fixture",
            "independent acceptance and proof",
            "the architect is a writer and must not edit child-owned paths",
            "one architect writer group owns a worktree",
            "the `tasks.csv` lock protects only the ledger",
            "engineer/engineer requires strict isolation",
            "engineer/scout requires a stable separate read boundary",
            "scout/scout may overlap stable sources for independent questions",
            "one verifier checks the combined checkpoint",
            "scout supports bounded repo or contract mapping",
            "avoid scout for a trivial one-file lookup",
            "stop before the shared resource and report the collision and checkpoint",
            "pause affected writers",
            "invalidate read findings after a source change",
            "a child never integrates sibling work",
        ]:
            self.assertIn(phrase, subagents)
        for phrase in [
            "brain-dump discussion",
            "architect restates the understandable why and what in natural prose",
            "clear implementation authority",
            "material ambiguity",
            "behavior-based acceptance",
            "architect implementation exception",
            "safe engineer pair",
            "overlapping read-only scouts",
            "bounded scout evidence",
            "dependency start block",
            "architect writer barrier",
            "collision stop",
        ]:
            self.assertIn(phrase, evaluations)
        scenarios = [
            line
            for line in evaluations.splitlines()
            if line.startswith("| ") and not line.startswith("| ---") and "Scenario" not in line
        ]
        self.assertLess(len(scenarios), 40)

    def test_child_policy_compaction_bounds_and_identity_contract(self) -> None:
        subagents_path = SKILL / "references/subagents.md"
        subagents = subagents_path.read_text(encoding="utf-8")

        self.assertGreaterEqual(len(subagents.splitlines()), 100)
        self.assertLessEqual(len(subagents.splitlines()), 140)
        for heading in [
            "## Role-trigger matrix",
            "## Independence gate",
            "## Child lifecycle",
            "## Shared handoff envelope",
            "## Role-specific rules",
            "## Model and spawn",
            "## Checkpoint barrier",
            "## Return and stop conditions",
        ]:
            self.assertIn(heading, subagents)
        self.assertIn("The Architect owns each child name at spawn time", subagents)
        self.assertIn("task_name=engineer_beta", subagents)
        self.assertIn("Every child update starts with work or current state", subagents)
        self.assertIn(
            "Each child handoff begins with a short settled purpose, then states the outcome, boundary, contract, proof, and stop conditions",
            subagents,
        )
        self.assertIn("at most two useful heartbeats at two-minute intervals", subagents)
        self.assertNotIn("Architecture alignment:", subagents)
        self.assertNotIn("Return labels remain explicit", subagents)
        self.assertNotIn("labeled report", subagents)
        self.assertNotIn("First" + "name", subagents)

    def test_trigger_evals_and_proof_ownership_are_compact(self) -> None:
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8")
        scenarios = [
            line
            for line in evaluations.splitlines()
            if line.startswith("| ") and not line.startswith("| ---") and "Scenario" not in line
        ]
        self.assertGreaterEqual(len(scenarios), 20)
        self.assertLessEqual(len(scenarios), 40)
        self.assertNotIn("Failure indicators", evaluations)

        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        for term in [
            "Engineer owns targeted development checks",
            "After each checkpoint, the Architect reviews the diff, architecture, scope, and contract alignment in concise natural prose.",
            "Maintainer owns each recorded operation run and returns evidence once",
            "Verifier receives acceptance and the exact checkpoint",
            "independently reruns acceptance proof and one planned regression command",
            "repeat only a disputed operation",
        ]:
            self.assertIn(term, subagents)
        for name in ["deliver", "verify", "operations"]:
            lane = (SKILL / "references" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("subagents.md", lane)

        policy = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                SKILL / "SKILL.md",
                SKILL / "references/subagents.md",
                SKILL / "references/trigger-evals.md",
                ROOT / "README.md",
                ROOT / "docs/PROJECT.md",
            ]
        )
        for stale in ["Research" + "er", "research" + "er_", "First" + "name", "role_first" + "name"]:
            self.assertNotIn(stale, policy)
        self.assertIn("allocates the next never-used label", policy.lower())
        self.assertIn("scout/scout", policy.lower())

    def test_readme_stays_public_and_links_detailed_policy(self) -> None:
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        lowered = readme.lower()

        for term in ["shape", "decide", "plan", "diagnose", "deliver", "verify"]:
            self.assertIn(term, lowered)
        self.assertIn("canonical child-agent policy", lowered)
        self.assertEqual(
            lowered.count("plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md"),
            1,
        )
        for pattern in [
            r"multi-agent v2",
            r"\bgpt-\d",
            r"\b(?:service_tier|reasoning_effort)\b",
            r"\b(?:greeting|self-introduction|sentence template)\b",
            r"\b(?:heartbeat|two minutes)\b",
            r"\b(?:handoff|deviation|task name)\b",
        ]:
            self.assertIsNone(re.search(pattern, lowered), pattern)

    def test_native_luna_routing_and_hard_cut_are_packaged(self) -> None:
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        policy = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                ROOT / "AGENTS.md",
                SKILL / "SKILL.md",
                SKILL / "references/subagents.md",
            ]
        ).lower()

        self.assertFalse((SCRIPTS / "configure_codex.py").exists())
        self.assertFalse((SKILL / "assets/lean_sdlc_luna.toml").exists())
        self.assertNotIn("configure_codex", subagents)
        self.assertNotIn("lean_sdlc_luna", subagents)
        self.assertIn("model=gpt-5.6-luna", subagents)
        self.assertIn("reasoning_effort=max", subagents)
        self.assertIn("non-full-history `fork_turns`", subagents)
        self.assertIn("Omit `agent_type`", subagents)
        self.assertIn("Luna Max uses Standard service by default", subagents)
        self.assertIn("normal spawns omit `service_tier`", subagents)
        self.assertIn("gpt-5.6-terra", subagents)
        self.assertIn("reasoning_effort=xhigh", subagents)
        self.assertNotIn("configure_codex", policy)
        self.assertNotIn("lean_sdlc_luna", policy)
        for phrase in [
            "asd-ste100 issue 9",
            "active voice",
            "20 words or fewer",
            "25 words or fewer",
            "one term for one meaning",
            "conditions before actions",
            "american english spelling",
            "idioms, unnecessary synonyms, and vague pronouns",
            "preserve code, commands, paths, identifiers, protocol fields, quotations",
            "certified or full controlled-dictionary compliance",
        ]:
            self.assertIn(phrase, policy)

    def test_release_version_is_consistent(self) -> None:
        manifest = json.loads(
            PLUGIN.joinpath(".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        version = manifest["version"]
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        project = ROOT.joinpath("docs/PROJECT.md").read_text(encoding="utf-8")

        self.assertEqual(version, "1.13.0")
        self.assertIn(f"`v{version}`", readme)
        self.assertIn(f"- Version: {version}", project)
        self.assertIn(
            "- Version goal: Release the native Luna hard cut, confirmed why -> what -> how -> proof intent gate, expanded bounded evidence delegation, safe same-worktree concurrency, and dependency-before-start enforcement.",
            project,
        )


if __name__ == "__main__":
    unittest.main()
