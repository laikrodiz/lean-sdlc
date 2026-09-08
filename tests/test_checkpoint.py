from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "plugins/lean-sdlc/skills/lean-sdlc/scripts/checkpoint.py"


def run_checkpoint(
    repository: Path,
    *paths: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKPOINT), "--repo", str(repository), *paths],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class CheckpointTests(unittest.TestCase):
    def test_hash_is_stable_for_order_and_duplicate_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            nested = repository / "src" / "nested"
            nested.mkdir(parents=True)
            (repository / "src" / "a.txt").write_bytes(b"a\n")
            (nested / "b.txt").write_bytes(b"b\n")

            first = run_checkpoint(repository, "src", "src/nested/b.txt", "src/a.txt")
            second = run_checkpoint(repository, "src/a.txt", "src", "src/nested/b.txt")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertRegex(first.stdout.strip(), r"^[0-9a-f]{64}$")
            original = first.stdout

            (repository / "src" / "a.txt").write_bytes(b"changed\n")
            changed = run_checkpoint(repository, "src")
            self.assertEqual(changed.returncode, 0, changed.stderr)
            self.assertNotEqual(changed.stdout, original)

    def test_rejects_empty_root_missing_escape_and_git_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            repository.mkdir()
            (repository / ".git").mkdir()
            cases = (
                ((), "PATH"),
                ((".",), "repository root"),
                (("missing.txt",), "does not exist"),
                (("../outside",), "escapes repository"),
                ((".git",), ".git"),
            )
            for paths, expected in cases:
                with self.subTest(paths=paths):
                    result = run_checkpoint(repository, *paths)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected, result.stderr)

    def test_rejects_symbolic_links_directly_and_inside_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            source = repository / "source.txt"
            tree = repository / "tree"
            tree.mkdir(parents=True)
            source.write_text("source\n", encoding="utf-8")
            link = repository / "link.txt"
            nested_link = tree / "link.txt"
            try:
                os.symlink(source, link)
                os.symlink(source, nested_link)
            except (NotImplementedError, OSError):
                self.skipTest("symbolic links are unavailable")

            direct = run_checkpoint(repository, "link.txt")
            nested = run_checkpoint(repository, "tree")
            self.assertNotEqual(direct.returncode, 0)
            self.assertNotEqual(nested.returncode, 0)
            self.assertIn("symbolic links are not allowed", direct.stderr)
            self.assertIn("symbolic links are not allowed", nested.stderr)

    def test_policy_names_read_only_checkpoint_use_and_output_boundary(self) -> None:
        verify = (ROOT / "plugins/lean-sdlc/skills/lean-sdlc/protocols/verifier.md").read_text(
            encoding="utf-8"
        )
        command = '`python3 "<skill-root>/scripts/checkpoint.py" --repo "<repo-root>" PATH [PATH ...]`'
        self.assertIn(command, verify)
        self.assertIn("same explicit scope", verify)
        self.assertIn("outside tracked truth", verify)
        self.assertIn("Keep checkpoint values local", verify)
        self.assertIn("does not identify external state", verify)

    def test_declared_config_is_an_input_but_independent_work_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            for name in ("source.py", "config.json", "independent.md"):
                (repository / name).write_text("original\n", encoding="utf-8")
            before = run_checkpoint(repository, "source.py", "config.json")
            self.assertEqual(before.returncode, 0, before.stderr)
            (repository / "independent.md").write_text("changed\n", encoding="utf-8")
            independent = run_checkpoint(repository, "source.py", "config.json")
            self.assertEqual(independent.returncode, 0, independent.stderr)
            self.assertEqual(independent.stdout, before.stdout)
            (repository / "config.json").write_text("changed\n", encoding="utf-8")
            invalidated = run_checkpoint(repository, "source.py", "config.json")
            self.assertEqual(invalidated.returncode, 0, invalidated.stderr)
            self.assertNotEqual(invalidated.stdout, before.stdout)


if __name__ == "__main__":
    unittest.main()
