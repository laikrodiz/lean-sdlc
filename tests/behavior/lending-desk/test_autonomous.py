import csv
from pathlib import Path
import tempfile
import unittest
import zipfile

import autonomous as a


class TrialTests(unittest.TestCase):
    def record(self, **changes):
        return dict(dict(run_id="first", candidate="a"*64, variant="baseline",
                         revision=1, trace="pass", product=True, ledger=True), **changes)

    def test_two_independent_runs(self):
        one = self.record()
        two = self.record(run_id="second", variant="confirmation")
        self.assertEqual(a.advance([one])["action"], "run fresh confirmation")
        self.assertEqual(a.advance([one, two])["action"], "confirmed")
        for bad in ([two], [one, dict(two, run_id="first")], [one, dict(two, candidate="b"*64)]):
            with self.assertRaises(ValueError):
                a.advance(bad)

    def test_bound_revisions_and_require_changed_instructions(self):
        failed = self.record(trace="fail")
        second = dict(failed, run_id="2", revision=2, candidate="b"*64)
        third = dict(second, run_id="3", revision=3, candidate="c"*64)
        self.assertEqual(a.advance([failed, second, third])["action"], "stop: revision limit")
        with self.assertRaises(ValueError):
            a.advance([failed, dict(second, candidate=failed["candidate"])])

    def test_no_evidence_no_pass(self):
        self.assertEqual(a.trace_status({}), "unverified")
        with self.assertRaises(ValueError):
            a.trace_status({"no_operator_or_followup": {"status": "pass"}})
        self.assertEqual(a.advance([self.record(trace="unverified")])["action"],
                         "stop: incomplete workflow evidence")

    def test_open_bootstrap_blocks_ledger_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            with (p / "tasks.csv").open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([["Task ID","Owner","Status","Evidence"],
                                  ["TASK-000","bootstrap","In Progress",""],
                                  ["TASK-001","01234567","Done","one"],
                                  ["TASK-002","01234567","Done","two"]])
            self.assertFalse(a.ledger_status(p))

    def test_blind_bundles(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / n for n in ("first.zip", "next.zip")]
            self.assertEqual(a.pack(paths[0], "baseline"), a.pack(paths[1], "confirmation"))
            with zipfile.ZipFile(paths[0]) as x, zipfile.ZipFile(paths[1]) as y:
                self.assertEqual(x.namelist(), y.namelist())
                self.assertNotEqual(x.read("Friday cupboard/counter.csv"), y.read("Friday cupboard/counter.csv"))
                self.assertFalse(any("tests/behavior" in n or n.endswith("tasks.csv") for n in x.namelist()))
                self.assertIn("START.txt", x.namelist())
            with self.assertRaises(FileExistsError):
                a.pack(paths[0], "baseline")
