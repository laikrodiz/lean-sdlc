from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/lean-sdlc/scripts"
TASKS = SCRIPTS / "tasks.py"
CHECK = SCRIPTS / "lean_check.py"
INIT = SCRIPTS / "init_repo.py"
OWNER_HOOK = SCRIPTS / "session_owner.py"
HEADER = (
    "Task ID,Title,Status,Parent,Dependencies,Owner,"
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
    )


def write_ledger(repository: Path, body: str) -> None:
    planning = repository / "planning"
    planning.mkdir(parents=True)
    (planning / "tasks.csv").write_text(HEADER + body, encoding="utf-8")


class TaskLedgerTests(unittest.TestCase):
    def test_concurrent_creates_get_unique_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        str(TASKS),
                        "--repo",
                        str(repository),
                        "create",
                        "--title",
                        f"Task {number}",
                        "--parent",
                        "REPO",
                        "--acceptance",
                        "Row exists",
                        "--proof",
                        "Read ledger",
                    ],
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                for number in range(12)
            ]
            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(
                all(process.returncode == 0 for process in processes),
                results,
            )
            with (repository / "planning/tasks.csv").open(
                encoding="utf-8",
                newline="",
            ) as handle:
                rows = list(csv.DictReader(handle))
            ids = [row["Task ID"] for row in rows]
            self.assertEqual(len(ids), 12)
            self.assertEqual(len(set(ids)), 12)

    def test_only_owner_closes_without_direct_user_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                'TASK-001,Owned work,In Progress,REPO,,11111111,Done,Run checks,\n',
            )
            denied = run(
                str(TASKS),
                "--repo",
                str(repository),
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("belongs to owner 11111111", denied.stderr)

            allowed = run(
                str(TASKS),
                "--repo",
                str(repository),
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
                "--user-override",
                "--override-reason",
                "User requested closure in this thread",
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            ledger = (repository / "planning/tasks.csv").read_text(encoding="utf-8")
            self.assertIn("Done", ledger)
            self.assertIn("Direct user override", ledger)

    def test_claim_and_update_use_the_thread_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Planned work,Planned,REPO,,,Done,Run checks,\n",
            )
            claimed = run(
                str(TASKS),
                "--repo",
                str(repository),
                "claim",
                "TASK-001",
                "--owner",
                "12345678",
            )
            self.assertEqual(claimed.returncode, 0, claimed.stderr)

            denied = run(
                str(TASKS),
                "--repo",
                str(repository),
                "update",
                "TASK-001",
                "--owner",
                "87654321",
                "--title",
                "Wrong owner",
            )
            self.assertNotEqual(denied.returncode, 0)

            updated = run(
                str(TASKS),
                "--repo",
                str(repository),
                "update",
                "TASK-001",
                "--owner",
                "12345678",
                "--title",
                "Claimed work",
            )
            self.assertEqual(updated.returncode, 0, updated.stderr)
            ledger = (repository / "planning/tasks.csv").read_text(encoding="utf-8")
            self.assertIn("Claimed work", ledger)

    def test_owner_closes_normally(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                'TASK-001,Owned work,In Progress,REPO,,11111111,Done,Run checks,\n',
            )
            result = run(
                str(TASKS),
                "--repo",
                str(repository),
                "close",
                "TASK-001",
                "--owner",
                "11111111",
                "--evidence",
                "Checks passed",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_header_migrates_under_owned_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            planning = repository / "planning"
            planning.mkdir()
            (planning / "tasks.csv").write_text(
                "task_id,title,status,parent_ref,depends_on,owner,"
                "acceptance,proof,evidence\n"
                "TASK-001,Migrate,In Progress,REPO,,11111111,Readable,Inspect,\n",
                encoding="utf-8",
            )
            result = run(
                str(TASKS),
                "--repo",
                str(repository),
                "migrate",
                "--task",
                "TASK-001",
                "--owner",
                "11111111",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            header = (planning / "tasks.csv").read_text(encoding="utf-8").splitlines()[0]
            self.assertEqual(header, HEADER.strip())

    def test_owner_hook_is_stable_and_numeric(self) -> None:
        event = json.dumps(
            {
                "session_id": "019f71b5-b7e1-78f2-a426-1b7a95d87348",
                "hook_event_name": "SessionStart",
                "cwd": str(ROOT),
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

    def test_initializer_creates_current_ledger_and_owner_hook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            codex = repository / ".codex"
            codex.mkdir()
            (codex / "hooks.json").write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 existing.py",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            result = run(str(INIT), str(repository))
            self.assertEqual(result.returncode, 0, result.stderr)
            header = (
                repository / "planning/tasks.csv"
            ).read_text(encoding="utf-8").splitlines()[0]
            self.assertEqual(header, HEADER.strip())
            hooks = json.loads(
                (repository / ".codex/hooks.json").read_text(encoding="utf-8")
            )
            session_hooks = hooks["hooks"]["SessionStart"]
            self.assertEqual(len(session_hooks), 1)
            self.assertIn("Stop", hooks["hooks"])
            command = session_hooks[0]["hooks"][0]["command"]
            self.assertIn("lean-sdlc/scripts/session_owner.py", command)

            repeated = run(str(INIT), str(repository))
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            hooks = json.loads(
                (repository / ".codex/hooks.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(hooks["hooks"]["SessionStart"]), 1)

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
            full_check = run(str(CHECK), str(repository), "--task", "TASK-000")
            self.assertEqual(
                full_check.returncode,
                0,
                full_check.stdout + full_check.stderr,
            )


if __name__ == "__main__":
    unittest.main()
