"""Collect live final JSON answers in fresh sessions; do not verify agent actions."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

try:
    from .evaluation_runner import EvaluationError, load_scenarios, validate_observations
except ImportError:
    from evaluation_runner import EvaluationError, load_scenarios, validate_observations


DEFAULT_TIMEOUT = 120.0
DEFAULT_SCHEMA = Path(__file__).with_name("evaluation_observation_schema.json")


class LiveEvaluationError(RuntimeError):
    """The optional live evaluation cannot start or complete."""


def build_command(
    repo: Path,
    schema: Path,
    output: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "--ephemeral",
        "--json",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "--ignore-user-config",
        "--cd",
        str(repo.resolve()),
        "--output-schema",
        str(schema.resolve()),
        "--output-last-message",
        str(output.resolve()),
        prompt,
    ]


def _run_command(command: list[str], timeout: float) -> None:
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as error:
        raise LiveEvaluationError("codex executable is not available") from error
    except subprocess.TimeoutExpired as error:
        raise LiveEvaluationError(f"live evaluation timed out after {timeout:g}s") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "no error output").strip()
        raise LiveEvaluationError(f"codex live evaluation failed: {detail}") from error


def _read_observation(path: Path, scenario_id: str) -> dict[str, object]:
    try:
        observed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LiveEvaluationError(f"{scenario_id}: invalid structured observation: {error}") from error
    if not isinstance(observed, dict):
        raise LiveEvaluationError(f"{scenario_id}: structured observation must be an object")
    return observed


def run_live(
    repo: Path,
    scenarios_path: Path,
    output: Path,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    schema: Path = DEFAULT_SCHEMA,
) -> None:
    if timeout <= 0:
        raise LiveEvaluationError("live evaluation timeout must be positive")
    if not repo.is_dir():
        raise LiveEvaluationError(f"repository does not exist: {repo}")
    if not schema.is_file():
        raise LiveEvaluationError(f"output schema does not exist: {schema}")
    try:
        scenarios = load_scenarios(scenarios_path)
    except EvaluationError as error:
        raise LiveEvaluationError(str(error)) from error

    observations: dict[str, dict[str, object]] = {}
    with tempfile.TemporaryDirectory(prefix="lean-sdlc-evaluation-") as temporary:
        temporary_path = Path(temporary)
        for scenario in scenarios["scenarios"]:
            scenario_id = scenario["id"]
            prompt = scenario.get("prompt", scenario.get("request"))
            message = temporary_path / f"{scenario_id}.json"
            _run_command(build_command(repo, schema, message, prompt), timeout)
            observations[scenario_id] = _read_observation(message, scenario_id)

    document = {"format": 1, "observations": observations}
    try:
        validate_observations(document)
        output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    except (EvaluationError, OSError) as error:
        raise LiveEvaluationError(f"cannot write observations: {error}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("scenarios", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args(argv)
    try:
        run_live(args.repo, args.scenarios, args.output, timeout=args.timeout, schema=args.schema)
    except LiveEvaluationError as error:
        print(f"ERROR {error}")
        return 1
    print(f"WROTE {args.output} (live final JSON answers only; actions not verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
