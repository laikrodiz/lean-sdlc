from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/release_check.py"
WORKFLOW = ROOT / ".github/workflows/release-check.yml"


def load_release_check():
    spec = importlib.util.spec_from_file_location("release_check", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load release check")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RELEASE = load_release_check()


class ReleaseCheckTests(unittest.TestCase):
    def test_package_structure_and_versions_pass(self) -> None:
        RELEASE.check_package_structure(ROOT)
        self.assertEqual(RELEASE.check_version_consistency(ROOT), "1.24.2")

    def test_portable_default_runs_required_steps_with_external_cache(self) -> None:
        calls: list[tuple[str, list[str], dict[str, str]]] = []

        def fake_step(
            label: str,
            command: list[str],
            root: Path,
            environment: dict[str, str],
        ) -> subprocess.CompletedProcess[str]:
            calls.append((label, command, environment))
            return subprocess.CompletedProcess(command, 0, "", "")

        with patch.object(RELEASE, "_run_step", side_effect=fake_step):
            version = RELEASE.run_release_checks(ROOT)

        self.assertEqual(version, "1.24.2")
        self.assertEqual(
            [label for label, _, _ in calls],
            [
                "full unit suite",
                "structural Lean-SDLC check",
                "deterministic evaluation fixture check",
            ],
        )
        self.assertEqual(calls[0][1][1:3], ["-m", "unittest"])
        self.assertIn("tests.test_task_ledger", calls[0][1])
        self.assertIn("lean_check.py", calls[1][1][1])
        self.assertIn("evaluation_runner.py", calls[2][1][1])
        cache = Path(calls[0][2]["PYTHONPYCACHEPREFIX"])
        self.assertFalse(cache.is_relative_to(ROOT))
        self.assertEqual(calls[0][2]["PYTHONDONTWRITEBYTECODE"], "1")

    def test_structural_check_gets_missing_ledger_only_temporarily(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "tasks.csv"
            calls: list[str] = []

            def fake_step(
                label: str,
                command: list[str],
                step_root: Path,
                environment: dict[str, str],
            ) -> subprocess.CompletedProcess[str]:
                calls.append(label)
                if label == "full unit suite" or label == "deterministic evaluation fixture check":
                    self.assertFalse(ledger.exists())
                if label == "structural Lean-SDLC check":
                    self.assertEqual(ledger.read_text(encoding="utf-8"), RELEASE.EMPTY_LEDGER)
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch.object(RELEASE, "check_package_structure"), patch.object(
                RELEASE, "check_version_consistency", return_value="test"
            ), patch.object(RELEASE, "_test_modules", return_value=["tests.test_release_check"]), patch.object(
                RELEASE, "_run_step", side_effect=fake_step
            ):
                self.assertEqual(RELEASE.run_release_checks(root), "test")

            self.assertEqual(calls[1], "structural Lean-SDLC check")
            self.assertFalse(ledger.exists())

    def test_existing_ledger_is_preserved_during_structural_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "tasks.csv"
            original = b"private ledger\n"
            ledger.write_bytes(original)

            def fake_step(
                label: str,
                command: list[str],
                step_root: Path,
                environment: dict[str, str],
            ) -> subprocess.CompletedProcess[str]:
                if label == "structural Lean-SDLC check":
                    self.assertEqual(ledger.read_bytes(), original)
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch.object(RELEASE, "check_package_structure"), patch.object(
                RELEASE, "check_version_consistency", return_value="test"
            ), patch.object(RELEASE, "_test_modules", return_value=["tests.test_release_check"]), patch.object(
                RELEASE, "_run_step", side_effect=fake_step
            ):
                RELEASE.run_release_checks(root)

            self.assertEqual(ledger.read_bytes(), original)

    def test_missing_ledger_is_removed_when_structural_check_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "tasks.csv"

            def fail_structural_check(
                label: str,
                command: list[str],
                step_root: Path,
                environment: dict[str, str],
            ) -> subprocess.CompletedProcess[str]:
                if label == "structural Lean-SDLC check":
                    self.assertTrue(ledger.is_file())
                    raise RELEASE.ReleaseCheckError("structural failure")
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch.object(RELEASE, "check_package_structure"), patch.object(
                RELEASE, "check_version_consistency", return_value="test"
            ), patch.object(RELEASE, "_test_modules", return_value=["tests.test_release_check"]), patch.object(
                RELEASE, "_run_step", side_effect=fail_structural_check
            ):
                with self.assertRaisesRegex(RELEASE.ReleaseCheckError, "structural failure"):
                    RELEASE.run_release_checks(root)

            self.assertFalse(ledger.exists())

    def test_install_smoke_uses_temporary_codex_home_and_checks_listing(self) -> None:
        calls: list[tuple[str, list[str], dict[str, str]]] = []

        def fake_step(
            label: str,
            command: list[str],
            root: Path,
            environment: dict[str, str],
        ) -> subprocess.CompletedProcess[str]:
            calls.append((label, command, environment))
            output = "lean-sdlc" if label == "installed-package smoke check" else ""
            return subprocess.CompletedProcess(command, 0, output, "")

        with patch.object(RELEASE, "_run_step", side_effect=fake_step):
            RELEASE.run_install_smoke(ROOT, {"PYTHONPYCACHEPREFIX": "/tmp/cache"})

        self.assertEqual(
            [label for label, _, _ in calls],
            [
                "isolated marketplace registration",
                "isolated plugin installation",
                "installed-package smoke check",
            ],
        )
        self.assertEqual(
            calls[0][1],
            ["codex", "plugin", "marketplace", "add", str(ROOT.resolve())],
        )
        self.assertEqual(calls[1][1], ["codex", "plugin", "add", "lean-sdlc@lean-sdlc"])
        self.assertEqual(calls[2][1], ["codex", "plugin", "list"])
        homes = {environment["CODEX_HOME"] for _, _, environment in calls}
        self.assertEqual(len(homes), 1)
        home = Path(next(iter(homes)))
        self.assertNotEqual(home, Path("~/.codex").expanduser())
        self.assertFalse(home.is_relative_to(ROOT))

    def test_workflow_calls_only_the_portable_default(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("actions/checkout@v4", workflow)
        self.assertIn("actions/setup-python@v5", workflow)
        self.assertIn(
            "python3 scripts/release_check.py",
            workflow,
        )
        self.assertNotIn("--install-smoke", workflow)
        self.assertNotIn("OPENAI_API_KEY", workflow)


if __name__ == "__main__":
    unittest.main()
