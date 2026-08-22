"""Run the portable Lean-SDLC release checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence


VERSION_PATTERN = re.compile(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)")
PLUGIN = Path("plugins/lean-sdlc")
MANIFEST = PLUGIN / ".codex-plugin/plugin.json"
PROJECT = Path("docs/PROJECT.md")
README = Path("README.md")
STRUCTURAL_CHECK = PLUGIN / "skills/lean-sdlc/scripts/lean_check.py"
EVALUATION_RUNNER = Path("tests/evaluation_runner.py")
EXPECTED_PACKAGE_ROOT = {".codex-plugin", "hooks", "skills"}
REQUIRED_PACKAGE_PATHS = (
    ".codex-plugin/plugin.json",
    "hooks/hooks.json",
    "skills/lean-sdlc/SKILL.md",
)


class ReleaseCheckError(RuntimeError):
    """A release check failed."""


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise ReleaseCheckError(f"cannot read {path}: {error}") from error


def check_package_structure(root: Path) -> None:
    plugin = root / PLUGIN
    if not plugin.is_dir():
        raise ReleaseCheckError(f"missing plugin directory: {PLUGIN}")
    names = {path.name for path in plugin.iterdir()}
    if names != EXPECTED_PACKAGE_ROOT:
        raise ReleaseCheckError(
            f"plugin root must contain {sorted(EXPECTED_PACKAGE_ROOT)}, found {sorted(names)}"
        )
    for relative in REQUIRED_PACKAGE_PATHS:
        if not (root / PLUGIN / relative).is_file():
            raise ReleaseCheckError(f"missing package path: {PLUGIN / relative}")

    skill_roots = sorted(
        path.parent.name for path in (plugin / "skills").glob("*/SKILL.md")
    )
    if skill_roots != ["lean-sdlc"]:
        raise ReleaseCheckError(f"expected one lean-sdlc skill, found {skill_roots}")
    for path in plugin.rglob("*"):
        if path.name == "__pycache__" or path.suffix == ".pyc":
            raise ReleaseCheckError(f"generated Python cache is packaged: {path}")

    try:
        manifest = json.loads(_read(root / MANIFEST))
        hooks = json.loads(_read(root / PLUGIN / "hooks/hooks.json"))
    except json.JSONDecodeError as error:
        raise ReleaseCheckError(f"package JSON is invalid: {error}") from error
    if not isinstance(manifest, dict) or manifest.get("name") != "lean-sdlc":
        raise ReleaseCheckError("plugin manifest must name lean-sdlc")
    if not isinstance(manifest.get("version"), str):
        raise ReleaseCheckError("plugin manifest must contain a version")
    if manifest.get("skills") != "./skills/":
        raise ReleaseCheckError("plugin manifest must point to ./skills/")
    if not isinstance(hooks, dict) or not isinstance(hooks.get("hooks"), dict):
        raise ReleaseCheckError("hooks manifest must contain a hooks object")


def _versions(text: str) -> list[str]:
    return VERSION_PATTERN.findall(text)


def check_version_consistency(root: Path) -> str:
    try:
        manifest = json.loads(_read(root / MANIFEST))
    except json.JSONDecodeError as error:
        raise ReleaseCheckError(f"plugin manifest is invalid: {error}") from error
    version = manifest.get("version") if isinstance(manifest, dict) else None
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise ReleaseCheckError(f"invalid plugin version: {version!r}")

    readme_versions = _versions(_read(root / README))
    project_versions = _versions(_read(root / PROJECT))
    if readme_versions != [version, version]:
        raise ReleaseCheckError(
            f"README.md must contain the release version twice, found {readme_versions}"
        )
    if project_versions != [version]:
        raise ReleaseCheckError(
            f"docs/PROJECT.md must contain the release version once, found {project_versions}"
        )
    return version


def _run_step(
    label: str,
    command: Sequence[str],
    root: Path,
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    print(f"== {label} ==")
    try:
        result = subprocess.run(
            list(command),
            cwd=root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise ReleaseCheckError(f"{label} command is not available: {command[0]}") from error
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise ReleaseCheckError(f"{label} failed with exit code {result.returncode}")
    return result


def _test_modules(root: Path) -> list[str]:
    tests = sorted((root / "tests").glob("test*.py"))
    if not tests:
        raise ReleaseCheckError("tests directory contains no test modules")
    return [".".join(path.relative_to(root).with_suffix("").parts) for path in tests]


def run_install_smoke(
    root: Path,
    environment: dict[str, str],
    *,
    codex: str = "codex",
) -> None:
    with tempfile.TemporaryDirectory(prefix="lean-sdlc-codex-home-") as codex_home:
        smoke_environment = {**environment, "CODEX_HOME": codex_home}
        _run_step(
            "isolated marketplace registration",
            [codex, "plugin", "marketplace", "add", str(root)],
            root,
            smoke_environment,
        )
        _run_step(
            "isolated plugin installation",
            [codex, "plugin", "add", "lean-sdlc@lean-sdlc"],
            root,
            smoke_environment,
        )
        listed = _run_step(
            "installed-package smoke check",
            [codex, "plugin", "list"],
            root,
            smoke_environment,
        )
        if "lean-sdlc" not in f"{listed.stdout}\n{listed.stderr}":
            raise ReleaseCheckError("installed-package smoke check did not list lean-sdlc")


def run_release_checks(root: Path, *, install_smoke: bool = False) -> str:
    root = root.resolve()
    if not root.is_dir():
        raise ReleaseCheckError(f"repository directory does not exist: {root}")
    check_package_structure(root)
    version = check_version_consistency(root)
    with tempfile.TemporaryDirectory(prefix="lean-sdlc-pycache-") as cache:
        environment = {
            **os.environ,
            "PYTHONPYCACHEPREFIX": cache,
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        python = sys.executable
        _run_step(
            "full unit suite",
            [python, "-m", "unittest", *_test_modules(root)],
            root,
            environment,
        )
        _run_step(
            "structural Lean-SDLC check",
            [python, str(root / STRUCTURAL_CHECK), str(root)],
            root,
            environment,
        )
        _run_step(
            "deterministic evaluation fixture check",
            [python, str(root / EVALUATION_RUNNER)],
            root,
            environment,
        )
        if install_smoke:
            run_install_smoke(root, environment)
    return version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--install-smoke",
        action="store_true",
        help="install the plugin in a temporary CODEX_HOME and check it with Codex",
    )
    args = parser.parse_args(argv)
    try:
        version = run_release_checks(args.repo, install_smoke=args.install_smoke)
    except ReleaseCheckError as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(f"PASS Lean-SDLC v{version} release checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
