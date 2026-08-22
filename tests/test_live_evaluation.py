from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from .live_evaluation import DEFAULT_SCHEMA, LiveEvaluationError, build_command, run_live
from .evaluation_runner import load_observations, load_scenarios


ROOT = Path(__file__).resolve().parent
SCENARIOS = ROOT / "evaluation_scenarios.json"


class LiveEvaluationTests(unittest.TestCase):
    def test_prompts_use_lean_sdlc_and_request_only_structured_fields(self) -> None:
        scenarios = load_scenarios(SCENARIOS)
        for scenario in scenarios["scenarios"]:
            prompt = scenario.get("prompt", scenario.get("request"))
            self.assertTrue(prompt.startswith("Use $lean-sdlc."))
            self.assertIn("Return only JSON fields:", prompt)
            situation = prompt.split("Return only JSON fields:", 1)[0]
            self.assertGreaterEqual(len(situation.split()), 8)

    def test_command_uses_ephemeral_read_only_structured_output(self) -> None:
        command = build_command(Path("/repo"), DEFAULT_SCHEMA, Path("/tmp/one.json"), "inspect")
        self.assertEqual(command[0:4], ["codex", "exec", "--ephemeral", "--json"])
        self.assertIn("--sandbox", command)
        self.assertIn("read-only", command)
        self.assertIn("--output-schema", command)
        self.assertIn(str(DEFAULT_SCHEMA.resolve()), command)
        self.assertIn("--output-last-message", command)

    def test_codex_authentication_failure_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            failure = subprocess.CalledProcessError(
                1,
                "codex",
                stderr="authentication failed",
            )
            with patch("tests.live_evaluation.subprocess.run", side_effect=failure):
                with self.assertRaisesRegex(LiveEvaluationError, "authentication failed"):
                    run_live(repository, SCENARIOS, repository / "observations.json")

    def test_each_scenario_gets_a_fresh_call_and_observation_document(self) -> None:
        calls: list[list[str]] = []

        def fake_run(command: list[str], **_: object) -> None:
            calls.append(command)
            message = Path(command[command.index("--output-last-message") + 1])
            message.write_text(json.dumps({"result": message.stem}), encoding="utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            output = repository / "observations.json"
            with patch.dict(os.environ, {}, clear=True), patch(
                "tests.live_evaluation.subprocess.run", side_effect=fake_run
            ) as run:
                run_live(repository, SCENARIOS, output, timeout=7.5)

            document = load_observations(output)
            self.assertEqual(len(calls), len(document["observations"]))
            self.assertTrue(all("--ephemeral" in command for command in calls))
            self.assertTrue(all("--output-schema" in command for command in calls))
            self.assertEqual(run.call_args.kwargs["timeout"], 7.5)


if __name__ == "__main__":
    unittest.main()
