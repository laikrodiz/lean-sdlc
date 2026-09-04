from __future__ import annotations

import copy
import unittest
from pathlib import Path

from .evaluation_runner import (
    EvaluationError,
    evaluate,
    load_observations,
    load_scenarios,
    validate_scenarios,
)


SCENARIOS = Path(__file__).with_name("evaluation_scenarios.json")
OBSERVATIONS = Path(__file__).with_name("evaluation_observations_fixture.json")


class EvaluationRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenarios = load_scenarios(SCENARIOS)
        self.observations = load_observations(OBSERVATIONS)
        self.assertion_count = sum(
            len(scenario["assertions"]) for scenario in self.scenarios["scenarios"]
        )

    def test_repository_scenarios_pass_against_separate_observations(self) -> None:
        self.assertTrue(all("observed" not in scenario for scenario in self.scenarios["scenarios"]))
        checked, failures = evaluate(self.scenarios, self.observations)
        self.assertEqual((checked, failures), (self.assertion_count, ()))

    def test_missing_observation_fails(self) -> None:
        observations = copy.deepcopy(self.observations)
        observations["observations"].pop("proof-layers")

        checked, failures = evaluate(self.scenarios, observations)

        missing_count = next(
            len(scenario["assertions"])
            for scenario in self.scenarios["scenarios"]
            if scenario["id"] == "proof-layers"
        )
        self.assertEqual(checked, self.assertion_count - missing_count)
        self.assertIn("missing observation: proof-layers", failures)

    def test_wrong_observation_fails_its_assertion(self) -> None:
        observations = copy.deepcopy(self.observations)
        observations["observations"]["routing-unresolved-decision"]["route"] = "Engineer"

        checked, failures = evaluate(self.scenarios, observations)

        self.assertEqual(checked, self.assertion_count)
        self.assertIn(
            "routing-unresolved-decision:route equals 'Architect'; observed 'Engineer'",
            failures,
        )

    def test_extra_observation_fails(self) -> None:
        observations = copy.deepcopy(self.observations)
        observations["observations"]["unlisted-scenario"] = {"result": True}

        checked, failures = evaluate(self.scenarios, observations)

        self.assertEqual(checked, self.assertion_count)
        self.assertIn("extra observation: unlisted-scenario", failures)

    def test_invalid_shape_and_missing_category_fail_before_evaluation(self) -> None:
        document = copy.deepcopy(self.scenarios)
        document["scenarios"] = [
            scenario for scenario in document["scenarios"] if scenario["category"] != "proof"
        ]
        with self.assertRaisesRegex(EvaluationError, "missing required scenario categories: proof"):
            validate_scenarios(document)

    def test_observed_values_are_rejected_from_scenario_definitions(self) -> None:
        document = copy.deepcopy(self.scenarios)
        document["scenarios"][0]["observed"] = {"route": "Architect"}
        with self.assertRaisesRegex(EvaluationError, "observed belongs in the observation document"):
            validate_scenarios(document)

    def test_multiple_assertion_operators_are_rejected(self) -> None:
        document = copy.deepcopy(self.scenarios)
        document["scenarios"][0]["assertions"][0]["contains"] = "Architect"
        with self.assertRaisesRegex(EvaluationError, "assertion needs one operator"):
            validate_scenarios(document)


if __name__ == "__main__":
    unittest.main()
