"""Run the portable Lean-SDLC release checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Sequence


VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+")
README_INSTALL_SECTION = re.compile(
    r"(?ms)^##\s+Install\b[^\n]*\n(?P<body>.*?)(?=^##\s|\Z)"
)
README_CLONE_COMMAND = re.compile(
    r"(?m)^\s*(?:\$\s*)?git\s+clone\b(?P<args>[^\n]*)$"
)
README_CLONE_BRANCH = re.compile(r"(?:^|\s)--branch(?:=|\s+)(?P<tag>\S+)")
README_VERSION_TAG = re.compile(r"(?<![\w.])v\d+\.\d+\.\d+(?![\w.])")
PROJECT_VERSION = re.compile(r"(?m)^\s*-\s*Version:\s*(?P<version>\S+)\s*$")
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
EMPTY_LEDGER = "Task ID,Title,Status,Context,Dependencies,Owner,Acceptance Criteria,Proof,Evidence\n"


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


def check_version_consistency(root: Path) -> str:
    try:
        manifest = json.loads(_read(root / MANIFEST))
    except json.JSONDecodeError as error:
        raise ReleaseCheckError(f"plugin manifest is invalid: {error}") from error
    version = manifest.get("version") if isinstance(manifest, dict) else None
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise ReleaseCheckError(f"invalid plugin version: {version!r}")

    expected_tag = f"v{version}"
    readme = _read(root / README)
    install_match = README_INSTALL_SECTION.search(readme)
    if install_match is None:
        raise ReleaseCheckError("README.md must contain an Install section")
    install_body = install_match.group("body")
    clone_commands = list(README_CLONE_COMMAND.finditer(install_body))
    clone_tags = [
        tag
        for clone in clone_commands
        for tag in README_CLONE_BRANCH.findall(clone.group("args"))
    ]
    release_tags = README_VERSION_TAG.findall(README_CLONE_COMMAND.sub("", install_body))
    if (
        not release_tags
        or any(tag != expected_tag for tag in release_tags)
        or len(clone_commands) != 1
        or clone_tags != [expected_tag]
    ):
        raise ReleaseCheckError(
            "README.md Install section must contain the release tag and one clone branch "
            f"{expected_tag!r}, found release tags {release_tags!r} and clone tags {clone_tags!r}"
        )
    project = _read(root / PROJECT)
    project_versions = [
        match.group("version") for match in PROJECT_VERSION.finditer(project)
    ]
    if project_versions != [version]:
        raise ReleaseCheckError(
            f"docs/PROJECT.md must contain one matching Version field {version!r}, "
            f"found {project_versions!r}"
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


@contextmanager
def _temporary_empty_ledger(root: Path) -> Iterator[None]:
    path = root / "tasks.csv"
    created = False
    try:
        try:
            with path.open("x", encoding="utf-8", newline="") as handle:
                created = True
                handle.write(EMPTY_LEDGER)
        except FileExistsError:
            yield
            return
        yield
    finally:
        if created:
            path.unlink(missing_ok=True)


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
        failures: list[str] = []

        def run_independent(label: str, command: Sequence[str]) -> None:
            try:
                _run_step(label, command, root, environment)
            except ReleaseCheckError as error:
                message = str(error)
                if not message.startswith(label):
                    message = f"{label}: {message}"
                failures.append(message)

        run_independent("full unit suite", [python, "-m", "unittest", *_test_modules(root)])
        with _temporary_empty_ledger(root):
            run_independent(
                "structural Lean-SDLC check",
                [python, str(root / STRUCTURAL_CHECK), str(root)],
            )
        run_independent(
            "deterministic evaluation fixture check",
            [python, str(root / EVALUATION_RUNNER)],
        )
        if failures:
            details = "\n".join(f"- {failure}" for failure in failures)
            raise ReleaseCheckError(
                f"{len(failures)} independent release checks failed:\n{details}"
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
