from __future__ import annotations

import csv
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch


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
STARTUP_START = "<!-- lean-sdlc:startup v1 -->"
STARTUP_END = "<!-- /lean-sdlc:startup -->"


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


def initialize_repository(repository: Path) -> None:
    initialized = run(str(INIT), str(repository))
    if initialized.returncode != 0:
        raise AssertionError(initialized.stdout + initialized.stderr)


def packaged_startup_block() -> str:
    lines = (SKILL / "assets/AGENTS.md").read_text(encoding="utf-8").splitlines(
        keepends=True
    )
    start = next(index for index, line in enumerate(lines) if line.rstrip("\r\n") == STARTUP_START)
    end = next(index for index, line in enumerate(lines) if line.rstrip("\r\n") == STARTUP_END)
    return "".join(lines[start : end + 1])


def write_document_family(
    repository: Path,
    folder: str,
    prefix: str,
    *,
    name: str | None = None,
    links: list[str] | None = None,
) -> Path:
    directory = repository / "docs" / folder
    directory.mkdir(parents=True, exist_ok=True)
    filename = name or f"{prefix}-001-example.md"
    document = directory / filename
    document.write_text(f"# {prefix}-001 Example\n", encoding="utf-8")
    targets = links if links is not None else [filename]
    rows = "\n".join(
        f"| [{prefix}-001]({target}) | Example | Active | Example | None |"
        for target in targets
    )
    directory.joinpath("INDEX.md").write_text(
        "# Index\n\n"
        "| ID | Title | Status | Owns | Related |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"{rows}\n",
        encoding="utf-8",
    )
    return document


class TaskLedgerTests(unittest.TestCase):
    def test_context_mapping_accepts_valid_contexts_and_rejects_invalid_values_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            for context in ("Project", "Bootstrap", "Quick Fix", "FEAT-001", "DEC-001"):
                created = task(
                    repository,
                    "plan",
                    "--title",
                    f"Task for {context}",
                    "--context",
                    context,
                    "--acceptance",
                    "The task is accepted",
                    "--proof",
                    "Run the focused check",
                )
                self.assertEqual(created.returncode, 0, created.stderr)

            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            for context in ("Standard", "Other"):
                rejected = task(
                    repository,
                    "plan",
                    "--title",
                    "Invalid context",
                    "--context",
                    context,
                    "--acceptance",
                    "Must reject",
                    "--proof",
                    "Must not write",
                )
                self.assertNotEqual(rejected.returncode, 0)
                self.assertIn("Context", rejected.stderr)
                self.assertEqual(
                    repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                    before,
                )

            rejected_update = task(
                repository,
                "update",
                "TASK-000",
                "--context",
                "Standard",
            )
            self.assertNotEqual(rejected_update.returncode, 0)
            self.assertIn("Context", rejected_update.stderr)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

    def test_ledger_replacement_warns_after_parent_sync_failure(self) -> None:
        if os.name == "nt":
            self.skipTest("Windows does not require parent directory fsync")
        specification = importlib.util.spec_from_file_location(
            "task_ledger_for_test",
            SCRIPTS / "task_ledger.py",
        )
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.csv"
            stderr = StringIO()
            with patch.object(
                module.os,
                "fsync",
                side_effect=[None, OSError("directory sync unavailable")],
            ), redirect_stderr(stderr):
                module.write_ledger(path, [])

            self.assertTrue(path.is_file())
            self.assertIn("tasks.csv replacement succeeded", stderr.getvalue())
            self.assertIn("parent directory durability sync failed", stderr.getvalue())

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

    def test_quick_fix_close_records_pending_marker_and_lists_the_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            started = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Change a color",
                "--context",
                "Quick Fix",
                "--acceptance",
                "The color changes",
                "--proof",
                "Run the focused UI check",
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            closed = task(
                repository,
                "close",
                "TASK-000",
                "--owner",
                "12345678",
                "--evidence",
                "Focused UI check passed",
            )
            self.assertEqual(closed.returncode, 0, closed.stderr)

            row = read_rows(repository)[0]
            self.assertIn("[Quick Fix batch review pending]", row["Evidence"])
            listed = task(repository, "quick-fixes")
            self.assertEqual(listed.returncode, 0, listed.stderr)
            self.assertEqual(
                [row["Task ID"] for row in csv.DictReader(listed.stdout.splitlines())],
                ["TASK-000"],
            )

    def test_review_through_clears_only_the_reviewed_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            for title in ("First fix", "Second fix"):
                started = task(
                    repository,
                    "start",
                    "--owner",
                    "12345678",
                    "--title",
                    title,
                    "--context",
                    "Quick Fix",
                    "--acceptance",
                    "The fix works",
                    "--proof",
                    "Run the focused check",
                )
                self.assertEqual(started.returncode, 0, started.stderr)
                task_id = "TASK-000" if title == "First fix" else "TASK-001"
                closed = task(
                    repository,
                    "close",
                    task_id,
                    "--owner",
                    "12345678",
                    "--evidence",
                    "Focused check passed",
                )
                self.assertEqual(closed.returncode, 0, closed.stderr)

            reviewed_first = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Review first fix",
                "--context",
                "Project",
                "--acceptance",
                "The first fix is reviewed",
                "--proof",
                "Run the shared check",
            )
            self.assertEqual(reviewed_first.returncode, 0, reviewed_first.stderr)
            closed_first = task(
                repository,
                "close",
                "TASK-002",
                "--owner",
                "12345678",
                "--evidence",
                "Shared check passed",
                "--review-through",
                "TASK-000",
            )
            self.assertEqual(closed_first.returncode, 0, closed_first.stderr)
            listed = task(repository, "quick-fixes")
            self.assertEqual(listed.returncode, 0, listed.stderr)
            self.assertEqual(
                [row["Task ID"] for row in csv.DictReader(listed.stdout.splitlines())],
                ["TASK-001"],
            )

            reviewed_second = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Review second fix",
                "--context",
                "Project",
                "--acceptance",
                "The second fix is reviewed",
                "--proof",
                "Run the shared check",
            )
            self.assertEqual(reviewed_second.returncode, 0, reviewed_second.stderr)
            closed_second = task(
                repository,
                "close",
                "TASK-003",
                "--owner",
                "12345678",
                "--evidence",
                "Shared check passed",
                "--review-through",
                "TASK-001",
            )
            self.assertEqual(closed_second.returncode, 0, closed_second.stderr)
            self.assertEqual(
                list(csv.DictReader(task(repository, "quick-fixes").stdout.splitlines())),
                [],
            )

    def test_quick_fix_can_close_and_review_through_itself(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            started = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Self-reviewed fix",
                "--context",
                "Quick Fix",
                "--acceptance",
                "The fix works",
                "--proof",
                "Run the focused check",
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            closed = task(
                repository,
                "close",
                "TASK-000",
                "--owner",
                "12345678",
                "--evidence",
                "Focused check passed",
                "--review-through",
                "TASK-000",
            )
            self.assertEqual(closed.returncode, 0, closed.stderr)
            row = read_rows(repository)[0]
            self.assertIn("[Quick Fix batch review through TASK-000]", row["Evidence"])
            self.assertEqual(
                list(csv.DictReader(task(repository, "quick-fixes").stdout.splitlines())),
                [],
            )

    def test_invalid_quick_fix_review_does_not_mutate_the_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-000,Fix,Done,Quick Fix,,12345678,Done,Check,"
                "Focused check passed [Quick Fix batch review pending]\n"
                "TASK-001,Review,In Progress,Project,,12345678,Done,Check,\n",
            )
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            missing = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "12345678",
                "--evidence",
                "Shared check passed",
                "--review-through",
                "TASK-999",
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

            malformed = before.replace(
                "Focused check passed [Quick Fix batch review pending]",
                "Focused check passed [Quick Fix batch review through BAD]",
            )
            repository.joinpath("tasks.csv").write_text(malformed, encoding="utf-8")
            listed = task(repository, "quick-fixes")
            self.assertNotEqual(listed.returncode, 0)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                malformed,
            )

    def test_concurrent_quick_fix_closes_keep_both_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Second fix,In Progress,Quick Fix,,12345678,Done,Check,\n"
                "TASK-000,First fix,In Progress,Quick Fix,,12345678,Done,Check,\n",
            )
            processes: list[subprocess.Popen[str]] = []
            for task_id in ("TASK-001", "TASK-000"):
                processes.append(
                    subprocess.Popen(
                        [
                            sys.executable,
                            str(TASKS),
                            "--repo",
                            str(repository),
                            "close",
                            task_id,
                            "--owner",
                            "12345678",
                            "--evidence",
                            "Focused check passed",
                        ],
                        cwd=ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env={
                            **os.environ,
                            "PYTHONDONTWRITEBYTECODE": "1",
                        },
                    )
                )

            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(
                all(process.returncode == 0 for process in processes),
                results,
            )
            rows = read_rows(repository)
            self.assertEqual({row["Status"] for row in rows}, {"Done"})
            self.assertTrue(
                all(
                    "[Quick Fix batch review pending]" in row["Evidence"]
                    for row in rows
                )
            )
            self.assertFalse(repository.joinpath(".tasks.lock").exists())

    def test_review_through_rejects_an_older_planned_quick_fix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-002,Target fix,Done,Quick Fix,,12345678,Done,Check,Done\n"
                "TASK-000,Older fix,Planned,Quick Fix,,,Ready,Check,\n"
                "TASK-003,Review,In Progress,Project,,12345678,Done,Check,\n",
            )
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            result = task(
                repository,
                "close",
                "TASK-003",
                "--owner",
                "12345678",
                "--evidence",
                "Shared check passed",
                "--review-through",
                "TASK-002",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("TASK-000", result.stderr)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

    def test_review_through_rejects_an_older_active_quick_fix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-002,Target fix,Done,Quick Fix,,12345678,Done,Check,Done\n"
                "TASK-000,Older fix,In Progress,Quick Fix,,12345678,Ready,Check,\n"
                "TASK-003,Review,In Progress,Project,,12345678,Done,Check,\n",
            )
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            result = task(
                repository,
                "close",
                "TASK-003",
                "--owner",
                "12345678",
                "--evidence",
                "Shared check passed",
                "--review-through",
                "TASK-002",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("TASK-000", result.stderr)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

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

    def test_backlog_add_lists_sparse_rows_and_keeps_them_out_of_open(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            added = task(repository, "backlog-add", "--title", "Future idea")
            self.assertEqual(added.returncode, 0, added.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Status"], "Backlog")
            self.assertEqual(row["Context"], "Project")
            self.assertTrue(all(not row[field] for field in (
                "Dependencies",
                "Owner",
                "Acceptance Criteria",
                "Proof",
                "Evidence",
            )))

            listed = task(repository, "backlog")
            self.assertEqual(listed.returncode, 0, listed.stderr)
            self.assertEqual(
                listed.stdout,
                "Task ID,Title,Context\nTASK-000,Future idea,Project\n",
            )
            self.assertEqual(task(repository, "open").stdout, HEADER)

    def test_backlog_update_is_sparse_and_promotion_to_planned_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            self.assertEqual(
                task(repository, "backlog-add", "--title", "Broad idea").returncode,
                0,
            )

            updated = task(
                repository,
                "update",
                "TASK-000",
                "--title",
                "Refined idea",
                "--context",
                "FEAT-001",
            )
            self.assertEqual(updated.returncode, 0, updated.stderr)
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            rejected = task(
                repository,
                "update",
                "TASK-000",
                "--acceptance",
                "Must not be accepted in Backlog",
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

            promoted = task(
                repository,
                "promote",
                "TASK-000",
                "--to",
                "planned",
                "--title",
                "Sized task",
                "--context",
                "Project",
                "--acceptance",
                "The task is accepted",
                "--proof",
                "Run the focused check",
            )
            self.assertEqual(promoted.returncode, 0, promoted.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Status"], "Planned")
            self.assertEqual(row["Title"], "Sized task")
            self.assertEqual(row["Acceptance Criteria"], "The task is accepted")

    def test_promote_in_progress_requires_owner_and_finished_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Idea,Backlog,Project,,,,,\n"
                "TASK-000,Dependency,Done,Project,,11111111,Done,Check,Evidence\n",
            )
            before = repository.joinpath("tasks.csv").read_text(encoding="utf-8")
            missing_owner = task(
                repository,
                "promote",
                "TASK-001",
                "--to",
                "in-progress",
                "--acceptance",
                "Ready",
                "--proof",
                "Check",
            )
            self.assertNotEqual(missing_owner.returncode, 0)
            self.assertIn("--owner is required", missing_owner.stderr)
            self.assertEqual(
                repository.joinpath("tasks.csv").read_text(encoding="utf-8"),
                before,
            )

            promoted = task(
                repository,
                "promote",
                "TASK-001",
                "--to",
                "in-progress",
                "--owner",
                "12345678",
                "--dependencies",
                "TASK-000",
                "--acceptance",
                "Ready",
                "--proof",
                "Check",
            )
            self.assertEqual(promoted.returncode, 0, promoted.stderr)
            row = next(row for row in read_rows(repository) if row["Task ID"] == "TASK-001")
            self.assertEqual(row["Status"], "In Progress")
            self.assertEqual(row["Owner"], "12345678")
            self.assertEqual(row["Dependencies"], "TASK-000")

    def test_backlog_integrity_rejects_forbidden_fields_and_dependencies(self) -> None:
        cases = {
            "Bootstrap context": (
                "TASK-000,Idea,Backlog,Bootstrap,,,,,\n",
                "cannot use Bootstrap context",
            ),
            "Quick Fix context": (
                "TASK-000,Idea,Backlog,Quick Fix,,,,,\n",
                "cannot use Quick Fix context",
            ),
            "sparse fields": (
                "TASK-000,Idea,Backlog,Project,,12345678,Ready,,\n",
                "Backlog row must leave Owner empty",
            ),
            "dependency": (
                "TASK-001,Idea,Backlog,Project,,,,,\n"
                "TASK-000,Child,Planned,Project,TASK-001,,Ready,Check,\n",
                "depends on Backlog task TASK-001",
            ),
        }
        for name, (body, expected) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                repository = Path(directory)
                write_ledger(repository, body)
                result = task(repository, "backlog")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

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

    def test_checker_accepts_sparse_backlog_and_rejects_non_sparse_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            added = task(repository, "backlog-add", "--title", "Future idea")
            self.assertEqual(added.returncode, 0, added.stderr)
            checked = run(str(CHECK), str(repository))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

            repository.joinpath("tasks.csv").write_text(
                HEADER
                + "TASK-001,Future idea,Backlog,Project,,11111111,Ready,,\n"
                + "TASK-000,Initial setup,Done,Bootstrap,,bootstrap,Done,Check,Done\n",
                encoding="utf-8",
            )
            rejected = run(str(CHECK), str(repository))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("Backlog row must leave Owner empty", rejected.stdout)

    def test_checker_accepts_minimal_and_valid_optional_document_families(self) -> None:
        families = (
            ("features", "FEAT"),
            ("decisions", "DEC"),
            ("architecture", "ARCH"),
            ("state-machines", "STATE"),
            ("interfaces", "IFACE"),
            ("data", "DATA"),
            ("operations", "OPS"),
        )
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            minimal = run(str(CHECK), str(repository))
            self.assertEqual(minimal.returncode, 0, minimal.stdout + minimal.stderr)

            for folder, prefix in families:
                write_document_family(repository, folder, prefix)
            checked = run(str(CHECK), str(repository))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_before_write_does_not_require_a_finished_optional_collection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            features = repository / "docs" / "features"
            features.mkdir()
            features.joinpath("FEAT-001-example.md").write_text(
                "# Example\n", encoding="utf-8"
            )
            checked = run(
                str(CHECK),
                str(repository),
                "--before-write",
                "--task",
                "TASK-000",
                "--owner",
                "bootstrap",
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_checker_rejects_invalid_document_names_ids_and_headers(self) -> None:
        cases = {
            "malformed document name": lambda repository: write_document_family(
                repository,
                "features",
                "FEAT",
                name="FEAT-1-example.md",
            ),
            "duplicate id FEAT-001": lambda repository: (
                write_document_family(repository, "features", "FEAT"),
                repository.joinpath("docs/features/FEAT-001-other.md").write_text(
                    "# Other\n", encoding="utf-8"
                ),
            ),
            "expected header": lambda repository: (
                write_document_family(repository, "features", "FEAT"),
                repository.joinpath("docs/features/INDEX.md").write_text(
                    "# Index\n", encoding="utf-8"
                ),
            ),
        }
        for expected, setup in cases.items():
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                repository = Path(directory)
                initialize_repository(repository)
                setup(repository)
                checked = run(str(CHECK), str(repository))
                self.assertNotEqual(checked.returncode, 0)
                self.assertIn(expected, checked.stdout)

    def test_checker_rejects_broken_document_index_links(self) -> None:
        cases = {
            "missing INDEX.md": lambda repository: (
                repository.joinpath("docs/features").mkdir(parents=True),
                repository.joinpath("docs/features/FEAT-001-example.md").write_text(
                    "# Example\n", encoding="utf-8"
                ),
            ),
            "missing link to FEAT-001-example.md": lambda repository: write_document_family(
                repository, "features", "FEAT", links=[]
            ),
            "duplicate link to FEAT-001-example.md": lambda repository: write_document_family(
                repository,
                "features",
                "FEAT",
                links=["FEAT-001-example.md", "FEAT-001-example.md"],
            ),
            "linked file does not exist": lambda repository: write_document_family(
                repository,
                "features",
                "FEAT",
                links=["FEAT-999-missing.md"],
            ),
            "invalid family link": lambda repository: write_document_family(
                repository,
                "features",
                "FEAT",
                links=["../features/FEAT-001-example.md"],
            ),
        }
        for expected, setup in cases.items():
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                repository = Path(directory)
                initialize_repository(repository)
                setup(repository)
                checked = run(str(CHECK), str(repository))
                self.assertNotEqual(checked.returncode, 0)
                self.assertIn(expected, checked.stdout)

    def test_checker_accepts_one_requested_source_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            snapshot = repository / "archive" / "preset-engine" / "v1"
            snapshot.mkdir(parents=True)
            snapshot.joinpath("ARCHIVE.md").write_text(
                "# Preset Engine v1\n", encoding="utf-8"
            )
            repository.joinpath("archive/INDEX.md").write_text(
                "# Index\n\n"
                "| Capability | Snapshot | Archived | Reason | Replacement | Link |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| Preset engine | v1 | Today | Replaced | src/presets | "
                "[Open](preset-engine/v1/ARCHIVE.md) |\n",
                encoding="utf-8",
            )
            checked = run(str(CHECK), str(repository))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_checker_rejects_invalid_source_archive_structures(self) -> None:
        def create_snapshot(repository: Path, *, capability: str = "feature", snapshot: str = "v1") -> Path:
            path = repository / "archive" / capability / snapshot
            path.mkdir(parents=True)
            path.joinpath("ARCHIVE.md").write_text("# Snapshot\n", encoding="utf-8")
            return path

        cases = {
            "missing INDEX.md": lambda repository: create_snapshot(repository),
            "no source snapshots": lambda repository: repository.joinpath("archive").mkdir(),
            "missing ARCHIVE.md": lambda repository: repository.joinpath(
                "archive/feature/v1"
            ).mkdir(parents=True),
            "malformed capability name": lambda repository: create_snapshot(
                repository, capability="Feature"
            ),
            "malformed snapshot name": lambda repository: create_snapshot(
                repository, snapshot="Version 1"
            ),
            "missing link to archive/feature/v1/ARCHIVE.md": lambda repository: (
                create_snapshot(repository),
                repository.joinpath("archive/INDEX.md").write_text(
                    "# Index\n", encoding="utf-8"
                ),
            ),
            "expected header": lambda repository: (
                create_snapshot(repository),
                repository.joinpath("archive/INDEX.md").write_text(
                    "# Index\n\n[Open](feature/v1/ARCHIVE.md)\n",
                    encoding="utf-8",
                ),
            ),
            "duplicate link to archive/feature/v1/ARCHIVE.md": lambda repository: (
                create_snapshot(repository),
                repository.joinpath("archive/INDEX.md").write_text(
                    "[One](feature/v1/ARCHIVE.md)\n[Two](feature/v1/ARCHIVE.md)\n",
                    encoding="utf-8",
                ),
            ),
            "linked manifest does not exist": lambda repository: (
                create_snapshot(repository),
                repository.joinpath("archive/INDEX.md").write_text(
                    "[Missing](other/v1/ARCHIVE.md)\n", encoding="utf-8"
                ),
            ),
            "invalid snapshot link": lambda repository: (
                create_snapshot(repository),
                repository.joinpath("archive/INDEX.md").write_text(
                    "[Escape](../archive/feature/v1/ARCHIVE.md)\n",
                    encoding="utf-8",
                ),
            ),
        }
        for expected, setup in cases.items():
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                repository = Path(directory)
                initialize_repository(repository)
                setup(repository)
                archive = repository / "archive"
                if archive.is_dir() and not archive.joinpath("INDEX.md").exists() and expected != "missing INDEX.md":
                    archive.joinpath("INDEX.md").write_text("# Index\n", encoding="utf-8")
                checked = run(str(CHECK), str(repository))
                self.assertNotEqual(checked.returncode, 0)
                self.assertIn(expected, checked.stdout)

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
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                (SKILL / "assets/AGENTS.md").read_text(encoding="utf-8"),
            )
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

    def test_checker_reports_missing_and_stale_managed_startup_blocks(self) -> None:
        cases = {
            "missing managed startup block": "project-specific rules\n",
            "stale managed startup block": packaged_startup_block().replace(
                "\n", "\nStale instruction.\n",
                1,
            ),
        }
        for expected, content in cases.items():
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                repository = Path(directory)
                initialize_repository(repository)
                repository.joinpath("AGENTS.md").write_text(content, encoding="utf-8")

                checked = run(str(CHECK), str(repository))

                self.assertNotEqual(checked.returncode, 0)
                self.assertIn(expected, checked.stdout)

    def test_startup_repair_requires_owned_in_progress_authorization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            stale = packaged_startup_block().replace(
                "\n", "\nStale instruction.\n",
                1,
            )
            repository.joinpath("AGENTS.md").write_text(stale, encoding="utf-8")
            write_ledger(
                repository,
                "TASK-001,Repair startup,In Progress,Project,,12345678,"
                "Repair the startup block,Run the checker,\n",
            )
            before = repository.joinpath("AGENTS.md").read_text(encoding="utf-8")

            missing = run(str(INIT), str(repository), "--repair-startup")
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("requires --task TASK-ID and --owner OWNER", missing.stderr)
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                before,
            )

            wrong_owner = run(
                str(INIT),
                str(repository),
                "--repair-startup",
                "--task",
                "TASK-001",
                "--owner",
                "87654321",
            )
            self.assertNotEqual(wrong_owner.returncode, 0)
            self.assertIn("TASK-001 is not owned by 87654321", wrong_owner.stderr)
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                before,
            )

    def test_startup_repair_preserves_project_text_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            block = packaged_startup_block()
            prefix = "# Project-specific rules\n\n"
            suffix = "\n## Local rules\nKeep this text unchanged.\n"
            stale = block.replace(
                "\n", "\nStale instruction.\n",
                1,
            )
            repository.joinpath("AGENTS.md").write_text(
                prefix + stale + suffix,
                encoding="utf-8",
            )
            write_ledger(
                repository,
                "TASK-001,Repair startup,In Progress,Project,,12345678,"
                "Repair the startup block,Run the checker,\n",
            )

            repaired = run(
                str(INIT),
                str(repository),
                "--repair-startup",
                "--task",
                "TASK-001",
                "--owner",
                "12345678",
            )

            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            self.assertIn("repaired AGENTS.md", repaired.stdout)
            expected = prefix + block + suffix
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                expected,
            )
            checked = run(str(CHECK), str(repository))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

            before_repeat = repository.joinpath("AGENTS.md").read_text(encoding="utf-8")
            repeated = run(
                str(INIT),
                str(repository),
                "--repair-startup",
                "--task",
                "TASK-001",
                "--owner",
                "12345678",
            )

            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("0 control change(s)", repeated.stdout)
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                before_repeat,
            )

    def test_startup_repair_appends_missing_block_without_changing_project_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initialize_repository(repository)
            project_text = "# Project-owned rules\n\nKeep this text unchanged.\n"
            agents = repository.joinpath("AGENTS.md")
            agents.write_text(project_text, encoding="utf-8")
            os.chmod(agents, 0o640)
            write_ledger(
                repository,
                "TASK-001,Repair startup,In Progress,Project,,12345678,"
                "Repair the startup block,Run the checker,\n",
            )

            repaired = run(
                str(INIT),
                str(repository),
                "--repair-startup",
                "--task",
                "TASK-001",
                "--owner",
                "12345678",
            )

            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            self.assertEqual(
                agents.read_text(encoding="utf-8"),
                project_text + packaged_startup_block(),
            )
            self.assertEqual(agents.stat().st_mode & 0o777, 0o640)


class PackageContractTests(unittest.TestCase):
    def test_package_contains_one_skill_and_eleven_instruction_files(self) -> None:
        self.assertEqual({path.name for path in PLUGIN.iterdir()}, {".codex-plugin", "hooks", "skills"})
        self.assertEqual([path.parent.name for path in PLUGIN.glob("skills/*/SKILL.md")], ["lean-sdlc"])
        self.assertEqual(
            {path.name for path in (SKILL / "references").glob("*.md")},
            {"conversation.md", "plan.md", "ledger.md", "documentation.md", "operations.md"},
        )
        self.assertEqual(
            {path.name for path in (SKILL / "protocols").glob("*.md")},
            {"common.md", "lead.md", "scout.md", "maintainer.md", "verifier.md"},
        )
        self.assertFalse(any(path.name in {"__pycache__", ".DS_Store"} or path.suffix == ".pyc" for path in PLUGIN.rglob("*")))

    def test_optional_document_templates_are_complete_and_on_demand(self) -> None:
        assets = SKILL / "assets"
        expected = {
            "AGENTS.md",
            "architecture.md",
            "archive-index.md",
            "collection-index.md",
            "data.md",
            "decision.md",
            "feature.md",
            "glossary.md",
            "interface.md",
            "operation.md",
            "security.md",
            "source-archive.md",
            "state-machine.md",
            "verification.md",
        }
        self.assertEqual({path.name for path in assets.glob("*.md")}, expected)
        templates = "\n".join(
            path.read_text(encoding="utf-8")
            for path in assets.glob("*.md")
            if path.name != "AGENTS.md"
        )
        for term in [
            "FEAT-001",
            "DEC-001",
            "ARCH-001",
            "STATE-001",
            "IFACE-001",
            "DATA-001",
            "OPS-001",
            "archive/<capability>/<snapshot>/ARCHIVE.md",
        ]:
            self.assertIn(term, templates)

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

    def test_root_entry_matches_current_template_without_copied_workflow(self) -> None:
        template = (SKILL / "assets/AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual((ROOT / "AGENTS.md").read_text(encoding="utf-8"), template)
        self.assertIn("$lean-sdlc", template)
        self.assertIn("scripts/session_state.py", template)
        self.assertIn("Preserve CODEX_SESSION_ID", template)
        self.assertLess(len(template.split()), 200)
        self.assertNotIn("subagents.md", template)
        self.assertNotIn("--mode", template)

    def test_entry_and_ui_metadata_do_not_force_implementation(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = dispatcher.split("---", 2)[1]
        self.assertIn("explicitly requested", frontmatter)
        self.assertIn("required by repository instructions", frontmatter)
        for path in (SKILL / "agents/openai.yaml", PLUGIN / ".codex-plugin/plugin.json"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("discuss or plan without writes", text)
            self.assertIn("implement only authorized work", text)

    def test_readme_is_public_and_links_current_rules(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for role in ("Lead", "Scout", "Maintainer", "Verifier"):
            self.assertIn(role, text)
        self.assertNotIn("Assisted mode", text)
        self.assertNotIn("Solo mode", text)
        self.assertNotIn("subagents.md", text)
        self.assertNotRegex(text, r"\b(?:service_tier|reasoning_effort)\b")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                self.assertTrue((ROOT / target.split("#", 1)[0]).exists(), target)

    def test_release_version_is_consistent(self) -> None:
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        version = manifest["version"]
        self.assertEqual(version, "1.30.0")
        self.assertIn(f"v{version}", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(f"- Version: {version}", (ROOT / "docs/PROJECT.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
