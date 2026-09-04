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
                "Use exact startup fields from the lifecycle system message.",
                "Use outdated startup fields from the lifecycle system message.",
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
                "Use exact startup fields from the lifecycle system message.",
                "Use outdated startup fields from the lifecycle system message.",
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
                "Use exact startup fields from the lifecycle system message.",
                "Use outdated startup fields from the lifecycle system message.",
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

    def test_automation_lifecycle_uses_recorded_operations_and_bounds_authority(self) -> None:
        operations = (SKILL / "references/operations.md").read_text(encoding="utf-8").lower()
        contracts = (SKILL / "references/repository-contracts.md").read_text(encoding="utf-8").lower()
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()
        asset = (SKILL / "assets/operation.md").read_text(encoding="utf-8").lower()

        for phrase in [
            "reuse recorded operations as the only automation catalog",
            "status and maintenance owner",
            "second equivalent successful mechanic",
            "direct evidence that the mechanic will recur",
            "candidates do not enter durable docs automatically",
            "architect approves the contract before scripting",
            "existing project command or target",
            "existing script",
            "native or installed tool",
            "smallest new script",
            "engineer implements an approved script and one focused runnable check",
            "maintainer records and later replays the canonical command",
            "later work reads recorded operations first",
            "solo follows the same record",
            "maintainer marks an automation as stale",
            "explicit inputs and safe defaults",
            "validate the target",
            "stable exit status",
            "run noninteractive",
            "write output atomically when practical",
            "omit secrets and machine-specific paths",
            "bound default output",
            "transient signal may retry only under recorded recovery",
            "recorded failure follows authorized recovery",
            "script defect goes to engineer",
            "changed contract or unknown cause stops and returns to architect/diagnose",
        ]:
            self.assertIn(phrase, operations)

        for phrase in [
            "first approved and recorded automation",
            "recorded operations are the only automation catalog",
            "do not add another automation file, registry, hook, state field, role, mode, dependency, or runtime framework",
        ]:
            self.assertIn(phrase, contracts)

        for phrase in [
            "before retaining new automation, follow [operations.md](operations.md)",
            "use [operations](operations.md) for delivery from the accepted source",
        ]:
            self.assertIn(phrase, subagents)

        self.assertIn("automation lifecycle", evaluations)

        for heading in [
            "## maintenance owner",
            "## canonical command",
            "## inputs and defaults",
            "## outputs and artifacts",
            "## failure and recovery",
            "## last verified",
        ]:
            self.assertIn(heading, asset)

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
        self.assertIn("responsibility and observed pressure", decide)
        self.assertIn("mermaid", contracts)
        self.assertIn("ascii pseudographics", contracts)
        self.assertIn("plausible edge cases", evaluations)

    def test_quick_fix_policy_is_inline_and_batch_review_is_bounded(self) -> None:
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8")
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8")
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8")
        ledger = (SCRIPTS / "task_ledger.py").read_text(encoding="utf-8")
        tasks_script = (SCRIPTS / "tasks.py").read_text(encoding="utf-8")

        for phrase in [
            "Quick Fix is inline Plan classification",
            "not a mode, lane, task type, or prompt",
            "Record Context `Quick Fix`",
            "exact requested outcome",
            "local reversible scope",
            "no unresolved product, design, architecture, public interface, schema, migration, dependency, security, generated-file, or external-state choice",
            "one immediate narrow proof",
            "request to use Quick Fix never bypasses eligibility",
            "one visible plan item",
            "one owned task",
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write --task TASK-ID --owner OWNER",
            "Architect may execute Quick Fix in Assisted or Solo",
            "Do not spawn Engineer, Maintainer, or Verifier per Quick Fix",
            "Shared batch may reuse or start Verifier when normal proof trigger applies",
            "Review diff and run narrow proof before close",
            "Quick-only multi-fix batch",
            "Standalone remains pending",
            "names exact",
            "`TASK-NNN — Title`",
        ]:
            self.assertIn(phrase.casefold(), plan.casefold())

        for phrase in [
            "Closing a Quick Fix records pending broad batch review",
            "`python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" quick-fixes` lists completed Quick Fixes that remain unreviewed",
            "Standard checkpoint reviews every pending Quick Fix",
            "`--review-through TASK-NNN`",
            "review prefix must contain only `Done` Quick Fix tasks through the target",
            "Invalid review references fail without ledger mutation",
            "several Quick Fixes may defer broad checks until one shared checkpoint",
            "A standalone Quick Fix may remain pending",
            "failed shared review creates a Standard correction task",
            "Deferred Quick Fix assurance is not automatic technical debt",
        ]:
            self.assertIn(phrase.casefold(), contracts.casefold())

        for phrase in [
            "Quick Fix",
            "SPECIAL_CONTEXTS",
            "QUICK_FIX_PENDING_MARKER",
        ]:
            self.assertIn(phrase.casefold(), ledger.casefold())
        for phrase in ["quick-fixes", "review-through"]:
            self.assertIn(phrase.casefold(), tasks_script.casefold())
        self.assertIn("Quick Fix classification", evaluations)
        self.assertIn("Quick Fix batch review", evaluations)
        self.assertIn("Do not spawn Engineer, Maintainer, or Verifier per Quick Fix", plan)

        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        self.assertRegex(readme, r"(?im)^.*Quick Fix(?:es)?.*$")
        for cli_detail in ["tasks.py quick-fixes", "--review-through", "[Quick Fix batch"]:
            self.assertNotIn(cli_detail.casefold(), readme.casefold())

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

        for phrase in [
            "the packaged `tasks.py` helper is the only ledger mutation path",
            "plan view",
            "python3 \"<skill-root>/scripts/lean_check.py\" \"<repo-root>\" --before-write --task task-id --owner owner",
            "one engineer checkpoint",
        ]:
            self.assertIn(phrase, dispatcher)
        for phrase in [
            "tasks.py",
            "in progress",
            "dependencies must be `done` before start",
            "update_plan",
            "rebuild only unresolved rows",
            "python3 \"<skill-root>/scripts/session_state.py\"",
        ]:
            self.assertIn(phrase, agents)
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
            "before task creation",
            "one behavior, one contract boundary, one proof cluster, and one accept-or-reject decision",
            "split on any independent answer",
            "and` in a title as a review signal, not an automatic split",
            "one ledger task represents one engineer checkpoint.",
            "one independently accepted behavior change",
            "one owning contract boundary",
            "one proof cluster",
            "one close decision",
            "may touch several files, tests, documentation, or migration steps",
            "only when all work is inseparable for that behavior",
            "require settled architecture, one coherent outcome, one independent bounded proof, and one accept-or-reject review.",
            "keep one task resumable from repository truth and its ledger row after compaction.",
            "split a task when a part can succeed, fail, defer, revert, release, or be accepted independently",
            "belongs to another behavior or contract area",
            "needs another architect decision",
            "merge pieces without independent value or proof.",
            "keep a correction in the same task",
            "only satisfies unchanged acceptance",
            "a new behavior needs a new task",
            "keep implementation tests inside the task.",
            "keep maintainer and verifier work attached unless independently deliverable.",
            "never size by elapsed time, file count, line count, or command count.",
            "keep local implementation steps and correction handoffs transient.",
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

    def test_task_sizing_preflight_and_split_rules_are_operational(self) -> None:
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8")
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8")

        self.assertIn("## Task preflight", plan)
        self.assertIn("Before task creation", plan)
        self.assertIn("Task preflight", evaluations)
        for phrase in [
            "one independently accepted behavior change under one owning contract boundary",
            "one proof cluster, and one close decision",
            "can succeed, fail, defer, revert, release, or be accepted independently",
            "belongs to another behavior or contract area",
            "needs another Architect decision",
            "Keep a correction in the same task when it only satisfies unchanged acceptance",
            "A new behavior needs a new task",
            "Never size by elapsed time, file count, line count, or command count",
            "Treat `and` in a title as a review signal, not an automatic split",
            "First size tasks for independent acceptance",
            "Keep together",
            "Split serially",
            "Split for parallel execution",
            "No mode, score, tasks.csv column, persistent group, or automation",
        ]:
            self.assertIn(phrase, plan)
        self.assertIn("Before each parallel assignment, confirm", subagents)
        self.assertIn("If separation or benefit is unclear, run serially", subagents)
        self.assertNotIn("Split on elapsed time", plan)
        self.assertNotIn("Split on file count", plan)

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
            "python3 \"<skill-root>/scripts/session_state.py\" --owner owner --mode assisted|solo",
            "python3 \"<skill-root>/scripts/session_state.py\" --owner owner --fast-children",
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
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()

        for phrase in [
            "require information, not fixed labels",
            "use natural prose for outcome, constraints, and exclusions",
            "only the plan needs visible structure",
            "concise visible plan",
            "define each durable plan item in natural prose",
            "observable completion condition and verification method",
            "the verification method is its proof",
            "a one-item plan is valid",
            "only durable task plan",
        ]:
            self.assertIn(phrase, plan)

        self.assertIn("explicit implementation authority", dispatcher + shape + deliver)
        self.assertIn("discussion and proposals remain read-only", dispatcher)
        self.assertIn("brainstorming and rephrasing remain read-only", shape)
        self.assertIn("each durable plan item maps to one task", plan)
        self.assertIn("keep local implementation steps and correction handoffs transient", plan)

        self.assertIn("engineer shows visible restatement", deliver)
        self.assertIn("use supplied task facts", child)
        self.assertIn("each durable plan item maps to one task", plan)
        self.assertIn(
            "discussion, proposal, or non-concrete proceed request",
            evaluations,
        )
        self.assertIn("task or implementation request", evaluations)
        self.assertIn("valid engineer checkpoint", evaluations)
        self.assertIn("architect direct path", evaluations)
        self.assertEqual(root_agents, template_agents)

    def test_policy_invariants_are_canonical_and_safe(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        operations = (SKILL / "references/operations.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()

        self.assertIn("## canonical lifecycle", dispatcher)
        self.assertEqual(subagents.count("## route the current work"), 1)
        route_order = [
            subagents.index("1. keep unresolved"),
            subagents.index("2. in solo"),
            subagents.index("3. apply the existing"),
            subagents.index("4. keep one understood"),
            subagents.index("5. use scout"),
            subagents.index("6. use engineer"),
            subagents.index("7. use verifier"),
        ]
        self.assertEqual(route_order, sorted(route_order))
        for role in ("engineer", "maintainer", "verifier", "scout"):
            self.assertIn(role, subagents)
        for model_term in (
            "model=gpt-5.6-luna",
            "reasoning_effort=max",
            "fork_turns=none",
            "gpt-5.6-terra",
            "reasoning_effort=xhigh",
        ):
            self.assertIn(model_term, subagents)

        for safety_term in (
            "read-only",
            "no ledger edits",
            "never let two agents mutate the same external target",
            "no scan, registry, backlog entry",
            "private chain-of-thought",
            "run the full suite once for",
        ):
            self.assertIn(safety_term, subagents + child + verify + operations)
        for naming_term in (
            "choose a lowercase role prefix and greek suffix",
            "allocate the next unused label",
            "never duplicate a reachable identity",
        ):
            self.assertIn(naming_term, subagents)
        for lifecycle_term in (
            "timeout, silence, or missed update does not mean failure",
            "completed children remain reusable",
            "give the child one atomic task or bounded inquiry",
            "stop conditions",
        ):
            self.assertIn(lifecycle_term, dispatcher + subagents)
        for boundary_term in (
            "assigned paths",
            "settled task",
            "affected-boundary risk",
            "independent proof",
            "repeat affected checks after relevant changes",
        ):
            self.assertIn(boundary_term, subagents + child + verify)
        self.assertIn("these rows are scenarios and assertions", evaluations)
        self.assertNotIn("failure indicators", evaluations)
        self.assertNotIn("role-trigger matrix", subagents)
    def test_intent_and_boundary_contracts_are_explicit(self) -> None:
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        contracts = (SKILL / "references/repository-contracts.md").read_text(encoding="utf-8").lower()
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()

        for term in (
            "shape owns the complete intent gate",
            "why -> what -> how -> proof",
            "smallest observable outcome plus constraints and non-goals",
            "stop for user confirmation",
            "brainstorming and rephrasing remain read-only",
        ):
            self.assertIn(term, shape)
        for term in (
            "derive observable acceptance from the confirmed outcome and affected value",
            "implementation mechanisms, changed files, and test commands support acceptance",
            "one proof cluster",
            "never size by elapsed time, file count, line count, or command count",
        ):
            self.assertIn(term, plan)
        for term in (
            "project purpose, value, behavior boundary, scope, stage, and version promise",
            "one root `tasks.csv` remains authoritative",
            "dependencies must exist, remain acyclic, and be `done` before start or close",
            "the ledger lock is not a source-file lock",
        ):
            self.assertIn(term, contracts)
        for term in (
            "the architect owns intent, public behavior, architecture, material assumptions, interfaces, permissions, task ownership, acceptance, conflict resolution, integration, and final signoff",
            "use at most two active work children",
            "never exceed two concurrent engineers",
            "a third child may be read-only",
            "count all descendants",
            "writable paths, generated outputs, mutable fixtures, caches, services, ports, devices, and external targets do not overlap",
            "shared read-only contracts are stable",
            "combined checkpoints use one architect-started verifier",
            "never let a child integrate sibling work",
        ):
            self.assertIn(term, subagents)
        self.assertIn("stop before the shared resource", child)
        for scenario in (
            "brain-dump discussion",
            "clear implementation authority",
            "material ambiguity",
            "behavior-based acceptance",
            "assisted parallel work",
            "bounded scout evidence",
            "dependency start block",
            "architect writer barrier",
            "collision stop",
        ):
            self.assertIn(f"| {scenario} |", evaluations)
        rows = [
            line
            for line in evaluations.splitlines()
            if line.startswith("| ") and not line.startswith("| ---") and "Scenario" not in line
        ]
        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(len(cells), 2)
            self.assertTrue(all(cells))
        scenarios = {
            row.strip("|").split("|", 1)[0].strip().casefold()
            for row in rows
        }
        for scenario in (
            "Canonical lifecycle",
            "Task preflight",
            "Assisted parallel work",
            "Proof and integration checkpoint",
        ):
            self.assertIn(scenario.casefold(), scenarios)
    def test_ledger_plan_view_projection_is_deterministic_and_read_only_for_brainstorming(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (SKILL / "assets/AGENTS.md").read_text(encoding="utf-8").lower()

        for phrase in [
            "task-nnn — title",
            "update_plan",
            "unresolved",
            "planned",
           "in_progress",
           "completed",
            "mark the closing row",
            "active close transition",
            "rebuild only unresolved non-backlog rows",
            "do not load full",
            "startup, resume, clear, or compaction",
            "python3 \"<skill-root>/scripts/tasks.py\" --repo \"<repo-root>\" open",
            "brainstorming and rephrasing remain read-only and create no task view",
            "every unresolved task in its own exact row",
            "parallel work changes status or plan prose, never task identity",
            "remains authoritative",
        ]:
            self.assertIn(phrase, dispatcher + plan)

        for phrase in [
            "brain-dump discussion",
            "creates no task or plan view",
            "ledger-to-plan projection",
        ]:
            self.assertIn(phrase, evaluations)

        self.assertEqual(root_agents, template_agents)
        self.assertIn("project unresolved", root_agents)
        self.assertIn("rebuild only unresolved rows from", root_agents)
        self.assertIn("brainstorming remains read-only and creates no task view", root_agents)

    def test_child_policy_sections_and_identity_contract(self) -> None:
        subagents_path = SKILL / "references/subagents.md"
        subagents = subagents_path.read_text(encoding="utf-8")
        child = (SKILL / "references/child.md").read_text(encoding="utf-8")

        for heading in [
            "## Authority and modes",
            "## Route the current work",
            "## Independence gate",
            "## Allocate and reuse",
            "## Model and spawn",
            "## Handoff and finish",
        ]:
            self.assertIn(heading, subagents)
        for heading in ["## Common boundary", "## Roles", "## Report and stop"]:
            self.assertIn(heading, child)
        self.assertIn("Choose a lowercase role prefix and Greek suffix", subagents)
        self.assertIn("Allocate the next unused label", subagents)
        self.assertIn("Keep the exact name with the reusable child", subagents)
        self.assertIn("No ledger edits, Git mutations, or sibling integration", child)
        self.assertIn("Focused read-only Git inspection is allowed", child)
        self.assertIn("No child spawning", child)
        self.assertIn(
            "Send an explicit parent message only for immediate action",
            child,
        )
        self.assertIn("Send one final return with outcome", child)
        self.assertIn("The thread can be reused later", child)
        self.assertNotIn("role-trigger matrix", subagents)
        self.assertNotIn("sentence template", child.casefold())

    def test_trigger_evals_and_proof_ownership_are_compact(self) -> None:
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8")
        rows = [
            line
            for line in evaluations.splitlines()
            if line.startswith("| ") and not line.startswith("| ---") and "Scenario" not in line
        ]
        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(len(cells), 2)
            self.assertTrue(all(cells))
        scenarios = {
            row.strip("|").split("|", 1)[0].strip().casefold()
            for row in rows
        }
        for scenario in (
            "Canonical lifecycle",
            "Valid Engineer checkpoint",
            "Proof reuse and invalidation",
            "Atomic-task batch checkpoint",
        ):
            self.assertIn(scenario.casefold(), scenarios)
        self.assertIn("These rows are scenarios and assertions", evaluations)
        self.assertNotIn("Failure indicators", evaluations)

        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        operations = (SKILL / "references/operations.md").read_text(encoding="utf-8").lower()
        for term in (
            "targeted proof checks changed behavior",
            "acceptance proof checks observable completion",
            "regression proof checks affected-boundary risk",
        ):
            self.assertIn(term, verify)
        self.assertIn("remain read-only", child)
        self.assertIn("do not repeat an identical targeted command", evaluations.casefold())
        self.assertIn("report a transient automation candidate", child)
        self.assertIn("run the full suite once for", verify)
        self.assertIn("maintainer records and later replays the canonical command", operations)
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        self.assertIn("after the final engineer return", deliver)
        self.assertIn("one short visible alignment signoff", deliver)
        self.assertIn("reviews scope, architecture, contract alignment", deliver)
        self.assertNotIn("verification is running against unchanged source", verify)
        self.assertNotIn("verification passed", verify)
        for name in ("deliver", "verify", "operations"):
            lane = (SKILL / "references" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("subagents.md", lane)

    def test_child_evidence_and_checkpoint_boundaries(self) -> None:
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        operations = (SKILL / "references/operations.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()

        for phrase in (
            "task id, title, owner, both exact roots, writable paths, stable reads",
            "acceptance, planned proof, and stop conditions",
            "reused children receive the change in instructions plus relevant refreshed evidence",
        ):
            self.assertIn(phrase, subagents)
        for phrase in (
            "short natural progress updates",
            "outcome, focused changes or citations, proof, and remaining risks",
        ):
            self.assertIn(phrase, child)
        verify_order = [
            verify.index(term)
            for term in (
                "identify complete verification inputs",
                "verifier runs",
                "compare returned sha-256 values locally",
                "collect independent safe failures together",
                "stop after all required proof passes",
            )
        ]
        self.assertEqual(verify_order, sorted(verify_order))
        self.assertIn("scripts/checkpoint.py", verify)
        self.assertIn("do not persist checkpoint hashes or make the architect calculate them", verify)
        self.assertIn("maintainer classifies failures only by matching a recorded operation failure signal", operations)
        self.assertIn("omit them from visible operation reports", operations)
        self.assertIn("packaged checkpoint helper before and after proof", evaluations)
        self.assertIn("compares values locally", evaluations)
        self.assertIn("stable dependencies, inputs, and resources", evaluations)
        self.assertIn("stop writers touching checkpoint inputs or resources", evaluations)
        self.assertIn("environment", evaluations)

    def test_lifecycle_and_proof_boundaries_are_behavioral(self) -> None:
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        child = (SKILL / "references/child.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8").lower()

        for term in (
            "a timeout, silence, or missed update does not mean failure",
            "reuse a reachable child for the same role and relevant context",
            "only the architect allocates children",
            "preauthorize an engineer to spawn or reuse one exact named read-only verifier",
            "never let a child integrate sibling work",
        ):
            self.assertIn(term, subagents)
        for term in (
            "complete one atomic outcome, including related tests and mechanical consistency",
            "local corrections without new approval",
            "architecture, interfaces, behavior, acceptance, permissions, and ownership remain unchanged",
            "only an exact architect-preauthorized verifier",
            "no other child spawning",
            "escalate repeated equivalent failures without new evidence",
        ):
            self.assertIn(term, child)
        for term in (
            "selected authoritative contracts",
            "focused patches",
            "exact evidence",
            "broad or cross-boundary source",
            "do not require complete broad source reads",
        ):
            self.assertIn(term, deliver + verify)
        for term in (
            "use an independent verifier",
            "run only missing or invalidated checks",
            "repeat affected checks after relevant changes",
        ):
            self.assertIn(term, verify)
        for term in (
            "after the final engineer return",
            "one short visible alignment signoff",
            "reviews scope, architecture, contract alignment",
            "stop writers touching the checkpoint inputs or resources",
        ):
            self.assertIn(term, deliver + subagents)
        self.assertNotIn("parent metadata", evaluations)

    def test_child_progress_is_event_driven_and_not_template_bound(self) -> None:
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        child = (SKILL / "references/child.md").read_text(encoding="utf-8")
        evaluations = (SKILL / "references/trigger-evals.md").read_text(encoding="utf-8")

        for phrase in [
            "short natural progress updates",
            "current action, why it matters, and the observed result or next step",
            "send an explicit parent message only for immediate action",
            "blocker",
            "scope change",
            "one final return",
            "end the active turn",
            "the thread can be reused later",
        ]:
            self.assertIn(phrase.casefold(), child.casefold())

        self.assertIn("Child visible update", evaluations)
        self.assertIn("silence alone is not failure", evaluations.casefold())
        self.assertIn("end the active turn", evaluations.casefold())
        self.assertIn("followup_task", evaluations)
        self.assertIn("routine progress stays in the child thread", subagents.casefold())
        self.assertIn("architect does not echo unchanged child facts", evaluations.casefold())
        self.assertIn("role repetition", child.casefold())

    def test_readme_stays_public_and_links_detailed_policy(self) -> None:
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        lowered = readme.lower()

        for term in ["intent", "approach", "tasks", "implement", "verify"]:
            self.assertIn(term, lowered)
        self.assertIn("child-agent policy", lowered)
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
            r"\b(?:deviation|task name)\b",
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
        self.assertIn("fork_turns=none", subagents)
        self.assertIn("Omit `agent_type`", subagents)
        self.assertIn("Standard Luna omits `service_tier`", subagents)
        self.assertIn("no `service_tier` or `agent_type`", subagents)
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

        self.assertTrue(version)
        self.assertIn(f"`v{version}`", readme)


if __name__ == "__main__":
    unittest.main()
