from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.test_task_ledger import INIT, ROOT, SKILL, initialize_repository, run, write_ledger


BASELINE = ROOT / "tests/fixtures/AGENTS-v1.24.3.txt"


class ContractUpgradeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repository = Path(self.directory.name)
        initialize_repository(self.repository)
        write_ledger(
            self.repository,
            "TASK-001,Upgrade instructions,In Progress,Project,,12345678,"
            "Preserve project rules,Compare original data,\n",
        )
        self.agents = self.repository / "AGENTS.md"
        self.baseline = BASELINE.read_text(encoding="utf-8")
        self.current = (SKILL / "assets/AGENTS.md").read_text(encoding="utf-8")

    def upgrade(self, *extra: str):
        result = run(
            str(INIT), str(self.repository), "--upgrade-contract",
            "--task", "TASK-001", "--owner", "12345678", *extra,
        )
        for line in result.stdout.splitlines():
            if line.startswith("recovery copy: "):
                path = Path(line.removeprefix("recovery copy: "))
                self.addCleanup(shutil.rmtree, path.parent)
        return result

    def test_baseline_fixture_matches_released_identity(self) -> None:
        self.assertEqual(
            hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
            "03211c7f07b3829744aceafe8893ff6c8ae83414c85e036deac5e57b74937805",
        )

    def test_upgrade_preserves_custom_text_permissions_and_project_data(self) -> None:
        prefix = "# Custom project rules\r\n\r\nUse American English.\r\n"
        suffix = "\r\n## Device calibration\r\nPreserve offset 1.25 and café labels.\r\n"
        original = prefix + self.baseline.replace("\n", "\r\n") + suffix
        self.agents.write_bytes(original.encode("utf-8"))
        os.chmod(self.agents, 0o640)
        ledger = (self.repository / "tasks.csv").read_bytes()
        project = (self.repository / "docs/PROJECT.md").read_bytes()

        result = self.upgrade()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.agents.read_bytes(), (prefix + self.current + suffix).encode())
        self.assertEqual(self.agents.stat().st_mode & 0o777, 0o640)
        self.assertEqual((self.repository / "tasks.csv").read_bytes(), ledger)
        self.assertEqual((self.repository / "docs/PROJECT.md").read_bytes(), project)
        recovery = Path(next(line.removeprefix("recovery copy: ") for line in result.stdout.splitlines() if line.startswith("recovery copy: ")))
        self.assertEqual(recovery.read_bytes(), original.encode())
        self.assertEqual(recovery.stat().st_mode & 0o777, 0o640)

        repeated = self.upgrade()
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertNotIn("recovery copy:", repeated.stdout)
        self.assertEqual(self.agents.read_bytes(), (prefix + self.current + suffix).encode())

    def test_modified_or_ambiguous_old_contract_stops_without_changes(self) -> None:
        cases = (
            self.baseline.replace("Only the owner closes", "Custom approval is required before closure"),
            self.baseline + self.baseline,
            self.baseline + "<!-- /lean-sdlc:startup -->\n",
        )
        for original in cases:
            with self.subTest(original=original[:60]):
                self.agents.write_text(original, encoding="utf-8")
                before = self.agents.read_bytes()
                result = self.upgrade()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.agents.read_bytes(), before)
                self.assertNotIn("recovery copy:", result.stdout)

    def test_upgrade_requires_owned_active_task_and_exclusive_action(self) -> None:
        self.agents.write_text(self.baseline, encoding="utf-8")
        for arguments in (
            (), ("--task", "TASK-001", "--owner", "87654321"),
            ("--task", "TASK-001", "--owner", "12345678", "--repair-startup"),
        ):
            with self.subTest(arguments=arguments):
                result = run(str(INIT), str(self.repository), "--upgrade-contract", *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.agents.read_text(), self.baseline)
        write_ledger(self.repository, "TASK-001,Upgrade,Planned,Project,,,Preserve,Check,\n")
        result = self.upgrade()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.agents.read_text(), self.baseline)

    def test_symlink_contract_stops_without_replacing_link_or_target(self) -> None:
        original = self.repository / "custom-rules.txt"
        self.agents.rename(original)
        self.agents.symlink_to(original)
        before = original.read_bytes()
        result = self.upgrade()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertTrue(self.agents.is_symlink())
        self.assertEqual(original.read_bytes(), before)

    def test_custom_only_rules_can_receive_current_contract_without_overwrite(self) -> None:
        custom = "# Project rules\n\nKeep all device calibration values."
        self.agents.write_text(custom, encoding="utf-8")
        result = self.upgrade()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.agents.read_text(), custom + "\n" + self.current)


if __name__ == "__main__":
    unittest.main()
