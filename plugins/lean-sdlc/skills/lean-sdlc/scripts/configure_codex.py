#!/usr/bin/env python3
"""Install the Lean-SDLC Luna custom-agent profile in a Codex home."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import tomllib
from pathlib import Path


AGENT_NAME = "lean_sdlc_luna"
PROFILE_RELATIVE_PATH = Path("agents") / f"{AGENT_NAME}.toml"
V2_SETTINGS = {
    "enabled": "true",
    "tool_namespace": repr("agents"),
    "hide_spawn_agent_metadata": "false",
    "expose_spawn_agent_model_overrides": "true",
    "wait_agent_enabled": "true",
}
PROFILE_DESCRIPTION = (
    "Lean-SDLC Luna Max child agent. The lead supplies the Executor, Verifier, "
    "or Operator role in the spawn handoff."
)


class ConfigurationError(Exception):
    """Report a configuration that cannot be changed safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the Lean-SDLC Luna custom-agent profile."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Codex home to configure (default: ~/.codex)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check the profile and configuration without changing files.",
    )
    return parser.parse_args()


def load_toml(path: Path, label: str) -> dict[str, object]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigurationError(f"missing {label}: {path}") from exc
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"cannot parse {label}: {path}: {exc}") from exc


def table_bounds(text: str, table: str) -> tuple[int, int] | None:
    header = re.compile(
        rf"(?m)^\[{re.escape(table)}\][ \t]*(?:#.*)?(?:\n|$)"
    ).search(text)
    if header is None:
        return None
    next_header = re.compile(r"(?m)^\[[^\n]+\][ \t]*(?:#.*)?(?:\n|$)").search(
        text, header.end()
    )
    return header.end(), next_header.start() if next_header else len(text)


def assignment_pattern(key: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^(?P<indent>[ \t]*){re.escape(key)}[ \t]*="
        rf"(?P<value>[^\n]*)(?P<ending>\n|$)"
    )


def upsert_table_value(text: str, table: str, key: str, value: str) -> str:
    bounds = table_bounds(text, table)
    if bounds is None:
        separator = "" if not text or text.endswith("\n\n") else "\n"
        return f"{text}{separator}[{table}]\n{key} = {value}\n"

    start, end = bounds
    body = text[start:end]
    match = assignment_pattern(key).search(body)
    if match:
        existing = match.group("value")
        comment_index = existing.find("#")
        suffix = "" if comment_index < 0 else " " + existing[comment_index:].strip()
        replacement = f"{match.group('indent')}{key} = {value}{suffix}{match.group('ending')}"
        return text[:start] + body[: match.start()] + replacement + body[match.end() :] + text[end:]

    return text[:start] + f"{key} = {value}\n" + text[start:]


def remove_boolean_assignment(text: str, table: str, key: str) -> str:
    bounds = table_bounds(text, table)
    if bounds is None:
        return text

    start, end = bounds
    body = text[start:end]
    match = assignment_pattern(key).search(body)
    if match is None:
        return text

    raw_value = match.group("value").split("#", 1)[0].strip()
    if raw_value not in {"true", "false"}:
        raise ConfigurationError(
            f"[{table}].{key} must be a boolean before conversion"
        )
    return text[:start] + body[: match.start()] + body[match.end() :] + text[end:]


def configured_text(text: str) -> str:
    text = upsert_table_value(text, "features", "multi_agent", "true")
    text = remove_boolean_assignment(text, "features", "multi_agent_v2")
    for key, value in V2_SETTINGS.items():
        text = upsert_table_value(text, "features.multi_agent_v2", key, value)
    text = remove_boolean_assignment(text, "agents", AGENT_NAME)
    text = upsert_table_value(
        text,
        f"agents.{AGENT_NAME}",
        "description",
        repr(PROFILE_DESCRIPTION),
    )
    return upsert_table_value(
        text,
        f"agents.{AGENT_NAME}",
        "config_file",
        repr(PROFILE_RELATIVE_PATH.as_posix()),
    )


def profile_source() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / f"{AGENT_NAME}.toml"


def valid_configuration(config: dict[str, object]) -> bool:
    features = config.get("features")
    agents = config.get("agents")
    if not isinstance(features, dict) or features.get("multi_agent") is not True:
        return False
    multi_agent_v2 = features.get("multi_agent_v2")
    expected_v2 = {
        "enabled": True,
        "tool_namespace": "agents",
        "hide_spawn_agent_metadata": False,
        "expose_spawn_agent_model_overrides": True,
        "wait_agent_enabled": True,
    }
    if not isinstance(multi_agent_v2, dict):
        return False
    if any(multi_agent_v2.get(key) != value for key, value in expected_v2.items()):
        return False
    if not isinstance(agents, dict):
        return False
    metadata = agents.get(AGENT_NAME)
    return (
        isinstance(metadata, dict)
        and metadata.get("description") == PROFILE_DESCRIPTION
        and metadata.get("config_file") == PROFILE_RELATIVE_PATH.as_posix()
    )


def atomic_write(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def backup(path: Path) -> Path:
    destination = path.with_name(f"{path.name}.bak")
    mode = path.stat().st_mode & 0o777
    atomic_write(destination, path.read_text(encoding="utf-8"), mode)
    return destination


def check(codex_home: Path, profile_text: str) -> int:
    config_path = codex_home / "config.toml"
    profile_path = codex_home / PROFILE_RELATIVE_PATH
    config = load_toml(config_path, "config.toml")
    profile = load_toml(profile_path, "Lean-SDLC Luna profile")
    source = tomllib.loads(profile_text)

    failures = []
    if not valid_configuration(config):
        failures.append("config.toml does not expose the Lean-SDLC Luna profile")
    if profile != source:
        failures.append("Lean-SDLC Luna profile does not match the bundled profile")
    if failures:
        for failure in failures:
            print(f"check failed: {failure}", file=sys.stderr)
        return 1
    print("Lean-SDLC Luna profile is configured.")
    return 0


def configure(codex_home: Path) -> int:
    source_path = profile_source()
    source_text = source_path.read_text(encoding="utf-8")
    tomllib.loads(source_text)

    config_path = codex_home / "config.toml"
    profile_path = codex_home / PROFILE_RELATIVE_PATH
    config_text = ""
    if config_path.exists():
        load_toml(config_path, "config.toml")
        config_text = config_path.read_text(encoding="utf-8")
    new_config_text = configured_text(config_text)
    try:
        tomllib.loads(new_config_text)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigurationError(f"generated invalid config.toml: {exc}") from exc

    changed_config = config_text != new_config_text
    changed_profile = (
        not profile_path.exists()
        or profile_path.read_text(encoding="utf-8") != source_text
    )

    if changed_profile and profile_path.exists():
        print(f"backed up {backup(profile_path)}")
    if changed_config and config_path.exists():
        print(f"backed up {backup(config_path)}")

    if changed_profile:
        mode = profile_path.stat().st_mode & 0o777 if profile_path.exists() else None
        atomic_write(profile_path, source_text, mode)
        tomllib.loads(profile_path.read_text(encoding="utf-8"))
        print(f"installed {profile_path}")
    else:
        print(f"kept {profile_path}")

    if changed_config:
        mode = config_path.stat().st_mode & 0o777 if config_path.exists() else None
        atomic_write(config_path, new_config_text, mode)
        load_toml(config_path, "config.toml")
        print(f"updated {config_path}")
    else:
        print(f"kept {config_path}")
    return 0


def main() -> int:
    args = parse_args()
    try:
        source_text = profile_source().read_text(encoding="utf-8")
        tomllib.loads(source_text)
        if args.check:
            return check(args.codex_home.resolve(), source_text)
        return configure(args.codex_home.resolve())
    except (ConfigurationError, OSError, tomllib.TOMLDecodeError) as exc:
        print(f"configure_codex.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
