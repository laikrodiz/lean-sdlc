"""Evaluate recorded observations against repository-owned scenarios."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FORMAT_VERSION = 1
OPERATORS = ("equals", "contains")


class EvaluationError(ValueError):
    """The scenario or observation document does not follow the format."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvaluationError(f"cannot read {path}: {error}") from error
    return document


def load_scenarios(path: Path) -> dict[str, Any]:
    return validate_scenarios(_load_json(path))


def load_observations(path: Path) -> dict[str, Any]:
    return validate_observations(_load_json(path))


def validate_scenarios(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict) or document.get("format") != FORMAT_VERSION:
        raise EvaluationError(f"expected scenario format {FORMAT_VERSION}")

    required = document.get("required_categories")
    scenarios = document.get("scenarios")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise EvaluationError("required_categories must be a list of strings")
    if not isinstance(scenarios, list) or not scenarios:
        raise EvaluationError("scenarios must be a non-empty list")

    seen: set[str] = set()
    categories: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise EvaluationError("each scenario must be an object")
        scenario_id = scenario.get("id")
        category = scenario.get("category")
        prompt = scenario.get("prompt", scenario.get("request"))
        assertions = scenario.get("assertions")
        if not isinstance(scenario_id, str) or not scenario_id:
            raise EvaluationError("each scenario needs a non-empty id")
        if scenario_id in seen:
            raise EvaluationError(f"duplicate scenario id: {scenario_id}")
        if not isinstance(category, str) or not category:
            raise EvaluationError(f"{scenario_id}: category must be a string")
        if not isinstance(prompt, str) or not prompt.strip():
            raise EvaluationError(f"{scenario_id}: prompt or request must be non-empty")
        if "prompt" in scenario and "request" in scenario:
            raise EvaluationError(f"{scenario_id}: use prompt or request, not both")
        if "observed" in scenario:
            raise EvaluationError(f"{scenario_id}: observed belongs in the observation document")
        if not isinstance(assertions, list) or not assertions:
            raise EvaluationError(f"{scenario_id}: assertions must be a non-empty list")
        seen.add(scenario_id)
        categories.add(category)
        for assertion in assertions:
            _validate_assertion(scenario_id, assertion)

    missing = set(required) - categories
    if missing:
        names = ", ".join(sorted(missing))
        raise EvaluationError(f"missing required scenario categories: {names}")
    return document


def validate_observations(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict) or document.get("format") != FORMAT_VERSION:
        raise EvaluationError(f"expected observation format {FORMAT_VERSION}")
    observations = document.get("observations")
    if not isinstance(observations, dict):
        raise EvaluationError("observations must be an object keyed by scenario id")
    for scenario_id, observed in observations.items():
        if not isinstance(scenario_id, str) or not scenario_id:
            raise EvaluationError("observation ids must be non-empty strings")
        if not isinstance(observed, dict):
            raise EvaluationError(f"{scenario_id}: observation must be an object")
    return document


def _validate_assertion(scenario_id: str, assertion: Any) -> None:
    if not isinstance(assertion, dict) or not isinstance(assertion.get("path"), str):
        raise EvaluationError(f"{scenario_id}: assertion needs a path")
    operators = [operator for operator in OPERATORS if operator in assertion]
    if len(operators) != 1:
        raise EvaluationError(f"{scenario_id}: assertion needs one operator")
    if not assertion["path"]:
        raise EvaluationError(f"{scenario_id}: assertion path cannot be empty")


def _value_at(observed: dict[str, Any], path: str) -> Any:
    value: Any = observed
    for part in path.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            raise KeyError(path)
    return value


def _holds(actual: Any, assertion: dict[str, Any]) -> bool:
    if "equals" in assertion:
        return actual == assertion["equals"]
    expected = assertion["contains"]
    return expected in actual if isinstance(actual, (str, list, dict)) else False


def evaluate(
    scenarios: dict[str, Any], observations: dict[str, Any]
) -> tuple[int, tuple[str, ...]]:
    """Return the assertion count and failures for two validated documents."""

    validate_scenarios(scenarios)
    validate_observations(observations)
    scenario_list = scenarios["scenarios"]
    expected_ids = {scenario["id"] for scenario in scenario_list}
    observed_by_id = observations["observations"]
    failures: list[str] = []
    for scenario_id in sorted(expected_ids - set(observed_by_id)):
        failures.append(f"missing observation: {scenario_id}")
    for scenario_id in sorted(set(observed_by_id) - expected_ids):
        failures.append(f"extra observation: {scenario_id}")

    checked = 0
    for scenario in scenario_list:
        scenario_id = scenario["id"]
        if scenario_id not in observed_by_id:
            continue
        observed = observed_by_id[scenario_id]
        for assertion in scenario["assertions"]:
            checked += 1
            try:
                actual = _value_at(observed, assertion["path"])
                valid = _holds(actual, assertion)
            except (KeyError, TypeError):
                actual = "<missing>"
                valid = False
            if not valid:
                operator = next(operator for operator in OPERATORS if operator in assertion)
                failures.append(
                    f"{scenario_id}:{assertion['path']} {operator} "
                    f"{assertion[operator]!r}; observed {actual!r}"
                )
    return checked, tuple(failures)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scenarios",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("evaluation_scenarios.json"),
    )
    parser.add_argument(
        "observations",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("evaluation_observations_fixture.json"),
    )
    args = parser.parse_args(argv)
    try:
        checked, failures = evaluate(load_scenarios(args.scenarios), load_observations(args.observations))
    except EvaluationError as error:
        print(f"ERROR {error}")
        return 2
    if not failures:
        print(f"PASS {checked} assertions")
        return 0
    for failure in failures:
        print(f"FAIL {failure}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
