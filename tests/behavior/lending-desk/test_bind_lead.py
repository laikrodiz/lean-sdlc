"""Run with unittest discovery in this directory; no live session or provider needed."""
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest

from bind_lead import bind


class HandoffTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.db = self.root / "sessions.db"
        self.helper = (Path(__file__).resolve().parents[3] /
                       "plugins/lean-sdlc/skills/lean-sdlc/scripts/session_state.py")
        (self.root / "AGENTS.md").write_text("Use $lean-sdlc.")
        (self.root / "tasks.csv").touch()
        self.conn = sqlite3.connect(self.db)
        self.addCleanup(self.conn.close)
        self.conn.execute("CREATE TABLE threads(id,originator,model,reasoning_effort,cwd,archived,agent_role)")
        self.row = ("synthetic-child", "T3 Code", "gpt-6.2-sol", "high", str(self.root), 0, None)
        self.add_row(self.row)
        digest = hashlib.sha256(b"synthetic-child").digest()
        self.owner = f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"

    def add_row(self, row):
        self.conn.execute("INSERT INTO threads VALUES (?,?,?,?,?,?,?)", row)
        self.conn.commit()

    def check(self, **kwargs):
        return bind(self.db, self.root, self.helper,
                    **({"lead_owner": self.owner, "lead_helper": self.helper} | kwargs))

    def test_correct_child(self):
        self.assertIn(f"Owner: {self.owner}.", self.check())

    def test_wrong_owner(self):
        with self.assertRaisesRegex(ValueError, "owner"):
            self.check(lead_owner="00000000")

    def test_wrong_helper(self):
        with self.assertRaisesRegex(ValueError, "helper"):
            self.check(lead_helper=self.root / "AGENTS.md")

    def test_ambiguous_checkout(self):
        self.add_row(("second", *self.row[1:]))
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.check()

    def test_missing_session(self):
        self.conn.execute("UPDATE threads SET archived = 1")
        self.conn.commit()
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.check()
