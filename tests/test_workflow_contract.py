"""Check the legacy-to-current workflow contract boundary."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/lean-sdlc/skills/lean-sdlc"
SCRIPTS = SKILL / "scripts"
OLD = ROOT / "tests/fixtures/legacy_agents_1_26_0.md"
sys.path.insert(0, str(SCRIPTS))
from startup_contract import (  # noqa: E402
    StartupContractError,
    legacy_contract_error,
    upgrade_contract_text,
)


class WorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.env = {
            **os.environ,
            "CODEX_HOME": str(self.root / "state"),
            "CODEX_SESSION_ID": "contract-test",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        self.owner = f"{int.from_bytes(hashlib.sha256(b'contract-test').digest()[:8], 'big') % 100_000_000:08d}"
        result = self.run_cli("init_repo.py", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_cli(self, script: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / script), *arguments],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def begin(self, mode: str = "assisted") -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            "session_state.py",
            "--owner",
            self.owner,
            "--mode",
            mode,
            "--begin",
        )

    def test_known_contract_blocks_activation_without_state_write(self) -> None:
        self.repo.joinpath("AGENTS.md").write_text(OLD.read_text(), encoding="utf-8")
        for mode in ("assisted", "delegating", "solo"):
            result = self.begin(mode)
            self.assertEqual(result.returncode, 2)
            self.assertIn("legacy workflow routing", result.stderr)
        self.assertFalse(
            (self.root / "state/state/lean-sdlc" / f"{self.owner}.json").exists()
        )

    def test_known_contract_blocks_existing_write_gate(self) -> None:
        self.repo.joinpath("AGENTS.md").write_text(OLD.read_text(), encoding="utf-8")
        result = self.run_cli(
            "lean_check.py",
            str(self.repo),
            "--before-write",
            "--task",
            "TASK-000",
            "--owner",
            "bootstrap",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("legacy workflow routing", result.stdout)

    def test_upgrade_preserves_appendix_then_current_mode_can_begin(self) -> None:
        appendix = "\n## Project rules\nKeep the local privacy note.\n"
        self.repo.joinpath("AGENTS.md").write_text(
            OLD.read_text() + appendix,
            encoding="utf-8",
        )
        result = self.run_cli(
            "init_repo.py",
            str(self.repo),
            "--upgrade-contract",
            "--task",
            "TASK-000",
            "--owner",
            "bootstrap",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = self.repo.joinpath("AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(actual, SKILL.joinpath("assets/AGENTS.md").read_text() + appendix)
        self.assertIsNone(legacy_contract_error(actual))
        self.assertEqual(self.begin().returncode, 0)
        self.assertEqual(upgrade_contract_text(actual), actual)

    def test_upgrade_requires_owned_task_and_preserves_unknown_contract(self) -> None:
        original = OLD.read_text().replace("## Repository gate", "## My custom gate")
        self.repo.joinpath("AGENTS.md").write_text(original, encoding="utf-8")
        for arguments in (
            (),
            ("--task", "TASK-000", "--owner", "12345678"),
            ("--task", "TASK-000", "--owner", "bootstrap"),
        ):
            result = self.run_cli(
                "init_repo.py",
                str(self.repo),
                "--upgrade-contract",
                *arguments,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(self.repo.joinpath("AGENTS.md").read_text(), original)
        with self.assertRaises(StartupContractError):
            upgrade_contract_text(original)

    def test_current_contract_keeps_state_lock_and_has_no_old_policy_file(self) -> None:
        self.assertEqual(self.begin().returncode, 0)
        self.assertEqual(self.begin().returncode, 0)
        self.assertEqual(self.begin("delegating").returncode, 2)
        self.assertFalse(SKILL.joinpath("references/subagents.md").exists())

    def test_edited_legacy_core_cannot_activate_without_literal_trigger_phrases(self) -> None:
        text = OLD.read_text().replace("Before each child handoff", "Before each child assignment")
        text = text.replace(
            "Read `references/subagents.md` before delegation.",
            "Consult the subagent guide before allocating work.",
        )
        text = text.replace(
            "Assisted mode and Standard children are defaults.",
            "Default to Assisted with Standard children.",
        )
        self.repo.joinpath("AGENTS.md").write_text(text, encoding="utf-8")
        self.assertEqual(self.begin().returncode, 2)
        self.assertFalse(
            (self.root / "state/state/lean-sdlc" / f"{self.owner}.json").exists()
        )
        result = self.run_cli(
            "lean_check.py",
            str(self.repo),
            "--before-write",
            "--task",
            "TASK-000",
            "--owner",
            "bootstrap",
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.repo.joinpath("AGENTS.md").read_text(), text)

    def test_fresh_context_distinguishes_default_from_locked_mode(self) -> None:
        before = json.loads(self.run_cli("session_state.py", "--context").stdout)
        self.assertEqual(before["mode"], "assisted")
        self.assertIsNone(before["active_mode"])
        self.assertEqual(self.begin("solo").returncode, 0)
        after = json.loads(self.run_cli("session_state.py", "--context").stdout)
        self.assertEqual(after["active_mode"], "solo")
        self.assertEqual(after["owner"], before["owner"])
        self.assertEqual(self.begin("assisted").returncode, 2)


if __name__ == "__main__":
    unittest.main()
