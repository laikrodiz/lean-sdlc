"""Negative controls for adjudicating blind behavioral runs."""
import unittest
from tests.behavior.closure import closure_only

from tests.behavior.score import CONTROLS, MODELS, grade, inventory, score_manifest, sweep


class BehaviorScoreTests(unittest.TestCase):
    def test_standalone_close_uses_commands_not_final_claim(self):
        close = 'rtk python3 "/skill/tasks.py" --repo . close TASK-001 --evidence "a; b && c"'
        self.assertIs(closure_only("/bin/zsh -lc '" + close + "'"), True)
        self.assertIs(closure_only(close + " && python3 tasks.py overview"), False)
        self.assertIs(closure_only("cd /project && " + close), False)
        self.assertIsNone(closure_only('echo "tasks.py close"'))
        self.assertIsNone(closure_only("python3 tasks.py close $(whoami)"))
        self.assertIsNone(closure_only(close + " && "))
        run = self.run_record()
        obs = {"receipt": "command-42", "pass": True}
        run["checks"] = {"standalone_close": obs}
        self.assertEqual(grade(run, run["checks"]), "not verified")
        obs["complete_call_actions"] = [close, "date"]
        self.assertEqual(grade(run, run["checks"]), "fail")
        obs["complete_call_actions"] = [close]
        self.assertEqual(grade(run, run["checks"]), "pass")
    def run_record(self, model="sol-high", session="one"):
        return dict(model=model, case="delivery", revision="fixed", session=session,
                    controls=dict.fromkeys(CONTROLS, True),
                    checks={"output": {"pass": True, "receipt": "independent-output"}})

    def test_missing_proof_and_failed_isolation_do_not_pass(self):
        run = self.run_record()
        self.assertEqual(grade(run, ["output", "privacy"]), "not verified")
        run["checks"]["output"]["receipt"] = ""
        self.assertEqual(grade(run, ["output"]), "not verified")
        run["controls"]["sibling_denied"] = False
        self.assertEqual(grade(run, ["output"]), "invalid environment")

    def test_required_model_repetitions_and_no_retry_to_erase_failure(self):
        runs = [self.run_record(model, f"{model}-{i}") for model in MODELS for i in range(2)]
        def score(misses):
            return sweep({"delivery": ["output"]}, runs, "fixed", misses, ["delivery"])
        self.assertEqual(set(score([]).values()), {"pass"})
        self.assertEqual(set(score(["delivery"]).values()), {"not verified"})
        runs[0]["checks"]["output"]["pass"] = False
        self.assertEqual(score([])["delivery", "sol-high"], "fail")
        runs.append(runs[-1])
        with self.assertRaises(ValueError):
            score([])

    def test_inventory_has_unique_cases_and_each_routed_non_engineer_family(self):
        cases = inventory()
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        self.assertEqual({c["owner"] for c in cases}, {"conversation", "entry", "plan",
                         "lead", "common", "scout", "maintainer", "verifier", "ledger",
                         "documentation", "operations", "storage-review"})
        self.assertTrue(all(all(c.values()) for c in cases))

    def test_public_manifest_cannot_omit_families_or_report_missing_runs_as_green(self):
        variants = {f"fresh-{row['id']}": row["id"] for row in inventory()}
        data = dict(variants=variants, previous_misses=[], holdouts=list(variants),
                    runs=[], revision="frozen")
        self.assertEqual(set(score_manifest(data).values()), {"not verified"})
        del variants["fresh-storage"]
        with self.assertRaises(ValueError):
            score_manifest(data)
