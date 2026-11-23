from pathlib import Path
import sys
import tempfile
import unittest

from tests.test_task_ledger import SCRIPTS, run, TASKS, initialize_repository, write_ledger

sys.path.insert(0, str(SCRIPTS))
from startup_contract import contract_status, read_template_block, upgrade_text
from updates import refresh


class OrientationTests(unittest.TestCase):
    def test_old_current_custom_and_conflicting(self):
        current = read_template_block()
        old = current.replace("non-routine task transactions", "task transactions")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            path.write_text("Local rule\n" + old)
            self.assertEqual(contract_status(root), "upgrade-available")
            self.assertEqual(path.read_text(), "Local rule\n" + old)
            updated = upgrade_text(path.read_text(), current)
            self.assertEqual(updated, "Local rule\n" + current)
            self.assertEqual(upgrade_text(updated, current), updated)
            path.write_text(updated)
            self.assertEqual(contract_status(root), "current")
            path.write_text(updated.replace("non-routine", "custom"))
            self.assertEqual(contract_status(root), "review")
            path.write_text(updated)
            (root / "planning").mkdir()
            (root / "planning/tasks.csv").touch()
            self.assertEqual(contract_status(root), "review")

    def test_pinned_cached_and_offline(self):
        def forbidden():
            self.fail("unexpected lookup")
        self.assertEqual(refresh({}, forbidden, 200000), {})
        result = refresh({"follow": True}, lambda: "a refs/tags/v1.8.0\nb refs/tags/v2.0.0-rc1\nc refs/tags/v1.10.0", 200000)
        self.assertEqual(result["latest"], "1.10.0")
        self.assertEqual(refresh(result, forbidden, 200001), result)
        def offline():
            raise OSError("offline")
        self.assertEqual(refresh(result, offline, 400000)["latest"], "1.10.0")

    def test_scoped_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            initialize_repository(root)
            write_ledger(root, "TASK-001,First | item,Planned,Project,,,Works,Check,\nTASK-002,Second,Planned,Project,,,Works,Check,\nTASK-003,Omitted,Planned,Project,,,Works,Check,\n")
            def table(*ids):
                return run(str(TASKS), "--repo", str(root), "table", *ids)
            result = table("TASK-002", "TASK-001", "TASK-002")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLess(result.stdout.index("Second"), result.stdout.index("First"))
            self.assertIn(r"First \| item", result.stdout)
            self.assertNotIn("Omitted", result.stdout)
            self.assertEqual(result.stdout.count("Second"), 1)
            invalid = table("TASK-001", "TASK-999")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertNotIn("| Outcome |", invalid.stdout)
