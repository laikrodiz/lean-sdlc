import csv
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "plugins/lean-sdlc/skills/lean-sdlc/scripts"
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid",
           GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid",
           PYTHONDONTWRITEBYTECODE="1")


class ParallelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.run_at(self.repo, "git", "init", "-b", "main")
        (self.repo / ".gitignore").write_text("ignored\n")
        self.git(self.repo, "add", ".gitignore")
        self.git(self.repo, "commit", "-m", "base")
        self.base = self.git(self.repo, "rev-parse", "HEAD")
        self.integration = Path(self.op("begin", self.repo, "test"))

    def run_at(self, path, *args, ok=True):
        result = subprocess.run(args, cwd=path, env=dict(ENV, TMPDIR=str(self.root)),
                                text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, (args, result.stderr, result.stdout))
        return (result.stdout if ok else result.stderr).strip()

    def git(self, path, *args):
        return self.run_at(path, "git", *args)

    def op(self, *args, ok=True):
        return self.run_at(self.repo, sys.executable, SCRIPTS / "parallel.py", *args, ok=ok)

    def worker(self, name, filename):
        path = self.root / name
        self.git(self.repo, "worktree", "add", "--detach", str(path), self.base)
        (path / filename).write_text(name)
        self.git(path, "add", "--", filename)
        self.git(path, "commit", "-m", name)
        return path, self.git(path, "rev-parse", "HEAD")

    def test_combine_and_retire_only_retained_clean_work(self):
        for name in ("one", "two"):
            path, sha = self.worker(name, name)
            self.op("retire", self.integration, path, sha, ok=False)
            self.op("accept", self.integration, path, self.base, sha, "wrong", ok=False)
            self.op("accept", self.integration, path, self.base, sha, name)
            (path / "ignored").write_text("keep")
            (path / "local").write_text("keep this too")
            (path / name).write_text("edited")
            error = self.op("retire", self.integration, path, sha, ok=False)
            for entry in ("ignored: ignored", "untracked: local", f"tracked: {name}"):
                self.assertIn(entry, error)
            self.assertEqual((path / "ignored").read_text(), "keep")
            self.assertEqual((path / "local").read_text(), "keep this too")
            self.assertEqual((path / name).read_text(), "edited")
            (path / "local").unlink()
            (path / name).write_text(name)
            (path / "ignored").unlink()
            self.op("retire", self.integration, path, sha)
            self.assertFalse(path.exists())
        tip = self.git(self.integration, "rev-parse", "HEAD")
        self.op("land", self.repo, self.integration, "other", self.base, tip, ok=False)
        self.op("land", self.repo, self.integration, "main", self.base, tip)
        self.assertEqual(self.git(self.repo, "diff", "--cached", "--name-only").splitlines(), ["one", "two"])
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.base)
        self.op("retire", self.repo, self.integration, tip, ok=False)

    def test_commit_delivery_refuses_moved_or_dirty_destination(self):
        path, sha = self.worker("one", "one")
        self.op("accept", self.integration, path, self.base, sha, "one")
        tip = self.git(self.integration, "rev-parse", "HEAD")
        self.op("land", self.repo, self.integration, "main", sha, tip, "--commit", ok=False)
        (self.repo / "one").write_text("user work")
        self.op("land", self.repo, self.integration, "main", self.base, tip, "--commit", ok=False)
        self.assertEqual((self.repo / "one").read_text(), "user work")
        (self.repo / "one").unlink()
        self.op("land", self.repo, self.integration, "main", self.base, tip, "--commit")
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), tip)
        self.op("retire", self.repo, path, sha)
        self.op("retire", self.repo, self.integration, tip)
        self.assertFalse(self.integration.exists())

    def test_conflict_keeps_both_commits_and_original_checkout(self):
        first, a = self.worker("one", "shared")
        second, b = self.worker("two", "shared")
        self.op("accept", self.integration, first, self.base, a, "shared")
        error = self.op("accept", self.integration, second, self.base, b, "shared", ok=False)
        self.assertIn("'shared'", error)
        self.assertIn("rerun accept before retire", error)
        self.assertIn("shared", self.git(self.integration, "diff", "--diff-filter=U", "--name-only"))
        self.assertEqual((second / "shared").read_text(), "two")
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.base)
        self.op("retire", self.integration, second, b, ok=False)
        (self.integration / "shared").write_text("one and two")
        self.git(self.integration, "add", "shared")
        self.git(self.integration, "commit", "--no-edit")
        self.op("retire", self.integration, second, b, ok=False)
        self.op("accept", self.integration, second, self.base, b, "shared")
        self.op("retire", self.integration, second, b)
        self.assertFalse(second.exists())
        self.assertEqual((self.integration / "shared").read_text(), "one and two")

    def test_retire_preserves_hidden_edits_and_unrelated_checkouts(self):
        other = self.root / "unrelated"
        self.git(self.repo, "worktree", "add", "--detach", str(other), self.base)
        self.op("retire", self.repo, other, self.base, ok=False)
        self.assertTrue(other.exists())
        path, sha = self.worker("one", "tracked")
        self.op("accept", self.integration, path, self.base, sha, "tracked")
        for flag in ("assume-unchanged", "skip-worktree"):
            self.git(path, "update-index", "--" + flag, "tracked")
            (path / "tracked").write_text("user work")
            self.op("retire", self.integration, path, sha, ok=False)
            self.assertEqual((path / "tracked").read_text(), "user work")
            self.git(path, "update-index", "--no-" + flag, "tracked")
            (path / "tracked").write_text("one")

    def test_ready_fifty_no_claims_and_no_checkouts(self):
        ledger = self.repo / "tasks.csv"
        fields = "Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence".split(",")
        ids = [f"TASK-{n:03}" for n in range(1, 51)]
        with ledger.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(fields)
            for n, key in enumerate(ids):
                writer.writerow([key, key, "Planned", "Project", ids[0] if n == 49 else "", "", "result", "check", ""])
        before = ledger.read_bytes(), self.git(self.repo, "worktree", "list")
        for slots, count in ((0, 0), (3, 3), (50, 49)):
            rows = self.run_at(self.repo, sys.executable, SCRIPTS / "tasks.py", "--repo", self.repo,
                               "ready", "--slots", str(slots), *ids)
            self.assertEqual([row["Task ID"] for row in csv.DictReader(rows.splitlines())], ids[:count])
        self.assertEqual(before, (ledger.read_bytes(), self.git(self.repo, "worktree", "list")))
