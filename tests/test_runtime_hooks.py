from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins/lean-sdlc/skills/lean-sdlc/scripts"
SESSION_STATE = SCRIPTS / "session_state.py"
SPAWN_GUARD = SCRIPTS / "spawn_guard.py"
VERSION_ADVISORY = SCRIPTS / "version_advisory.py"


def load_version_advisory():
    spec = importlib.util.spec_from_file_location("version_advisory", VERSION_ADVISORY)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load version advisory")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERSION = load_version_advisory()


def run_script(
    script: Path,
    event: dict[str, object] | None = None,
    *,
    codex_home: Path,
    arguments: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=ROOT,
        input=None if event is None else json.dumps(event),
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "CODEX_HOME": str(codex_home), "PYTHONDONTWRITEBYTECODE": "1"},
    )


class RuntimeHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.repository = self.root / "repository"
        self.repository.mkdir()
        self.repository.joinpath("AGENTS.md").write_text(
            "Use $lean-sdlc for repository work.\n", encoding="utf-8"
        )
        self.repository.joinpath("tasks.csv").write_text("", encoding="utf-8")
        self.codex_home = self.root / "codex"
        self.session_id = "runtime-hook-session"

    def tearDown(self) -> None:
        self.directory.cleanup()

    def event(self, tool_input: dict[str, object]) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "cwd": str(self.repository),
            "hook_event_name": "PreToolUse",
            "tool_name": "Agent",
            "tool_input": tool_input,
        }

    def owner(self) -> str:
        digest = hashlib.sha256(self.session_id.encode("utf-8")).digest()
        return f"{int.from_bytes(digest[:8], 'big') % 100_000_000:08d}"

    def guard(self, tool_input: dict[str, object]) -> dict[str, object] | None:
        result = run_script(
            SPAWN_GUARD,
            self.event(tool_input),
            codex_home=self.codex_home,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return None if not result.stdout else json.loads(result.stdout)

    def set_state(self, *arguments: str) -> dict[str, object]:
        result = run_script(
            SESSION_STATE,
            codex_home=self.codex_home,
            arguments=("--owner", self.owner(), *arguments),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_bare_beta_is_rejected(self) -> None:
        denied = self.guard({"task_name": "beta"})
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_ambiguous_task_names_are_rejected(self) -> None:
        for task_name in ("_beta", "engineer__beta", "Engineer_beta", "engineer-beta"):
            with self.subTest(task_name=task_name):
                denied = self.guard({"task_name": task_name})
                self.assertEqual(
                    denied["hookSpecificOutput"]["permissionDecision"], "deny"
                )

    def test_engineer_beta_is_accepted(self) -> None:
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "engineer_beta",
                    "model": "gpt-5.6-luna",
                    "reasoning_effort": "max",
                    "fork_turns": "none",
                }
            )
        )

    def test_all_standard_roles_use_native_luna_fields(self) -> None:
        for role in ("engineer", "maintainer", "verifier", "scout"):
            with self.subTest(role=role):
                self.assertIsNone(
                    self.guard(
                        {
                            "task_name": f"{role}_beta",
                            "model": "gpt-5.6-luna",
                            "reasoning_effort": "max",
                            "fork_turns": "none",
                        }
                    )
                )

    def test_standard_priority_is_rejected(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "max",
                "fork_turns": "none",
                "service_tier": "priority",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_fast_priority_is_accepted(self) -> None:
        self.set_state("--fast-children")
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "engineer_beta",
                    "model": "gpt-5.6-luna",
                    "reasoning_effort": "max",
                    "fork_turns": "none",
                    "service_tier": "priority",
                }
            )
        )

    def test_solo_mode_denies_agent_spawns(self) -> None:
        self.set_state("--mode", "solo")
        denied = self.guard({"task_name": "engineer_beta"})
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_direct_user_custom_role_is_accepted(self) -> None:
        self.assertIsNone(self.guard({"task_name": "researcher_beta"}))

    def test_direct_user_custom_role_can_use_custom_routing(self) -> None:
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "researcher_beta",
                    "agent_type": "custom_profile",
                }
            )
        )

    def test_missing_native_model_is_rejected(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "fork_turns": "all",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_wrong_native_model_is_rejected(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-sol",
                "reasoning_effort": "max",
                "fork_turns": "none",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_wrong_native_reasoning_is_rejected(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "high",
                "fork_turns": "none",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_agent_type_is_rejected_for_standard_role(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "max",
                "fork_turns": "none",
                "agent_type": "custom",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_full_history_native_spawn_is_rejected(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "max",
                "fork_turns": "all",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_omitted_service_tier_is_allowed_for_standard_retry(self) -> None:
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "engineer_beta",
                    "model": "gpt-5.6-luna",
                    "reasoning_effort": "max",
                    "fork_turns": "none",
                }
            )
        )

    def test_fast_standard_retry_can_omit_service_tier(self) -> None:
        self.set_state("--fast-children")
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "engineer_beta",
                    "model": "gpt-5.6-luna",
                    "reasoning_effort": "max",
                    "fork_turns": "none",
                }
            )
        )

    def test_terra_fallback_is_accepted_without_profile_fields(self) -> None:
        self.assertIsNone(
            self.guard(
                {
                    "task_name": "engineer_beta",
                    "model": "gpt-5.6-terra",
                    "reasoning_effort": "xhigh",
                    "fork_turns": "none",
                }
            )
        )

    def test_terra_fallback_rejects_service_tier(self) -> None:
        denied = self.guard(
            {
                "task_name": "engineer_beta",
                "model": "gpt-5.6-terra",
                "reasoning_effort": "xhigh",
                "fork_turns": "none",
                "service_tier": "priority",
            }
        )
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_default_restoration(self) -> None:
        event = {
            "session_id": self.session_id,
            "cwd": str(self.repository),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn(self.owner(), message)
        self.assertIn("Mode: assisted", message)
        self.assertIn("Child tier: Standard", message)
        self.assertIn("reload subagents.md before Deliver", message)

    def test_workspace_root_selects_one_descendant_and_reports_both_roots(self) -> None:
        workspace = self.root / "workspace"
        repository = workspace / "nested" / "repository"
        repository.mkdir(parents=True)
        repository.joinpath("AGENTS.md").write_text(
            "Use $lean-sdlc for repository work.\n", encoding="utf-8"
        )
        repository.joinpath("tasks.csv").write_text("", encoding="utf-8")
        event = {
            "session_id": self.session_id,
            "cwd": str(workspace),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn(f"Repository root: {repository.resolve()}", message)
        self.assertIn(f"Skill root: {SCRIPTS.parent.resolve()}", message)

    def test_workspace_root_does_not_guess_between_descendants(self) -> None:
        workspace = self.root / "workspace"
        for name in ("first", "second"):
            repository = workspace / name
            repository.mkdir(parents=True)
            repository.joinpath("AGENTS.md").write_text(
                "Use $lean-sdlc for repository work.\n", encoding="utf-8"
            )
            repository.joinpath("tasks.csv").write_text("", encoding="utf-8")
        event = {
            "session_id": self.session_id,
            "cwd": str(workspace),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn("multiple repositories below this directory", message)
        self.assertIn("Focus one repository before continuing", message)
        self.assertNotIn("first", message)
        self.assertNotIn("second", message)

    def test_ancestor_repository_wins_over_ambiguous_descendants(self) -> None:
        nested = self.repository / "nested"
        nested.mkdir()
        for name in ("first", "second"):
            repository = nested / name
            repository.mkdir()
            repository.joinpath("AGENTS.md").write_text(
                "Use $lean-sdlc for repository work.\n", encoding="utf-8"
            )
            repository.joinpath("tasks.csv").write_text("", encoding="utf-8")
        event = {
            "session_id": self.session_id,
            "cwd": str(nested),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn(f"Repository root: {self.repository.resolve()}", message)
        self.assertNotIn("multiple repositories", message)

    def test_workspace_scan_ignores_deep_and_dependency_repositories(self) -> None:
        workspace = self.root / "workspace"
        for repository in (
            workspace / "one" / "two" / "three" / "four",
            workspace / "node_modules" / "dependency",
        ):
            repository.mkdir(parents=True)
            repository.joinpath("AGENTS.md").write_text(
                "Use $lean-sdlc for repository work.\n", encoding="utf-8"
            )
            repository.joinpath("tasks.csv").write_text("", encoding="utf-8")
        event = {
            "session_id": self.session_id,
            "cwd": str(workspace),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_state_persistence(self) -> None:
        self.set_state("--mode", "solo", "--fast-children")
        event = {
            "session_id": self.session_id,
            "cwd": str(self.repository),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn("Mode: solo", message)
        self.assertIn("Child tier: Fast", message)

    def test_invalid_state_falls_back_to_defaults(self) -> None:
        state_path = self.codex_home / "state/lean-sdlc" / f"{self.owner()}.json"
        state_path.parent.mkdir(parents=True)
        state_path.write_text('{"mode":"broken","fast_children":"yes"}', encoding="utf-8")
        event = {
            "session_id": self.session_id,
            "cwd": str(self.repository),
            "hook_event_name": "SessionStart",
        }
        result = run_script(SESSION_STATE, event, codex_home=self.codex_home)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["systemMessage"]
        self.assertIn("Mode: assisted", message)
        self.assertIn("Child tier: Standard", message)

    def test_version_advisory_requires_genuine_startup(self) -> None:
        def opener() -> None:
            self.fail("non-startup event must not fetch")

        for source in ("resume", "clear", "compact", None):
            event = {"hook_event_name": "SessionStart"}
            if source is not None:
                event["source"] = source
            with self.subTest(source=source), patch.dict(
                os.environ, {"CODEX_HOME": str(self.codex_home)}
            ), patch("sys.stdin", io.StringIO(json.dumps(event))), patch(
                "sys.stdout", new_callable=io.StringIO
            ) as output, patch.object(VERSION, "check_for_update", new=opener):
                self.assertEqual(VERSION.main(), 0)
                self.assertEqual(output.getvalue(), "")

    def test_version_advisory_returns_system_message(self) -> None:
        event = {"hook_event_name": "SessionStart", "source": "startup"}
        with patch("sys.stdin", io.StringIO(json.dumps(event))), patch(
            "sys.stdout", new_callable=io.StringIO
        ) as output, patch.object(
            VERSION, "check_for_update", return_value="upgrade notice"
        ):
            self.assertEqual(VERSION.main(), 0)
        self.assertEqual(json.loads(output.getvalue()), {"systemMessage": "upgrade notice"})

    def test_version_advisory_reports_highest_exact_newer_tag(self) -> None:
        manifest = self.root / "plugin.json"
        manifest.write_text(json.dumps({"version": "1.9.0"}), encoding="utf-8")

        class Response:
            status = 200

            def read(self, limit: int) -> bytes:
                self.limit = limit
                return json.dumps(
                    [
                        {"name": "v1.10.0"},
                        {"name": "v1.9.9"},
                        {"name": "1.20.0"},
                        {"name": "v1.11.0-rc.1"},
                        {"name": "release-1.20.0"},
                    ]
                ).encode("utf-8")

            def close(self) -> None:
                pass

        calls: list[tuple[object, int]] = []

        def opener(request: object, timeout: int) -> Response:
            calls.append((request, timeout))
            return Response()

        with patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)}), patch.object(
            VERSION.time, "time", return_value=1000
        ), patch.object(VERSION.urllib.request, "urlopen", side_effect=opener):
            message = VERSION.check_for_update(manifest=manifest)
        self.assertIn("Lean-SDLC v1.10.0 is available", message)
        self.assertIn("propose an upgrade", message)
        self.assertIn("repo contract compatibility", message)
        self.assertEqual(len(calls), 1)
        cache = self.codex_home / "state/lean-sdlc/version_advisory.json"
        self.assertTrue(cache.is_file())

    def test_version_advisory_rejects_bare_git_tag(self) -> None:
        manifest = self.root / "plugin.json"
        manifest.write_text(json.dumps({"version": "1.17.0"}), encoding="utf-8")

        class Response:
            status = 200

            def read(self, limit: int) -> bytes:
                return b'[{"name":"1.18.0"}]'

            def close(self) -> None:
                pass

        with patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)}):
            message = VERSION.check_for_update(
                now=1000, opener=lambda request, timeout: Response(), manifest=manifest
            )
        self.assertIsNone(message)
        cache = json.loads(
            (self.codex_home / "state/lean-sdlc/version_advisory.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIsNone(cache["latest"])

    def test_version_advisory_cache_suppresses_repeat_until_expiry(self) -> None:
        manifest = self.root / "plugin.json"
        manifest.write_text(json.dumps({"version": "1.17.0"}), encoding="utf-8")
        self.assertEqual(VERSION.CACHE_SECONDS, 24 * 60 * 60)
        responses = iter((b'[{"name":"v1.18.0"}]', b'[{"name":"v1.18.0"}]'))
        calls = 0

        class Response:
            status = 200

            def read(self, limit: int) -> bytes:
                return next(responses)

            def close(self) -> None:
                pass

        def opener(request: object, timeout: int) -> Response:
            nonlocal calls
            calls += 1
            return Response()

        with patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)}):
            first = VERSION.check_for_update(now=1000, opener=opener, manifest=manifest)
            second = VERSION.check_for_update(now=1001, opener=opener, manifest=manifest)
            third = VERSION.check_for_update(
                now=1000 + 24 * 60 * 60,
                opener=opener,
                manifest=manifest,
            )
        self.assertIsNotNone(first)
        self.assertIsNone(second)
        self.assertIsNotNone(third)
        self.assertEqual(calls, 2)

    def test_version_advisory_failures_are_silent(self) -> None:
        manifest = self.root / "plugin.json"
        manifest.write_text(json.dumps({"version": "1.17.0"}), encoding="utf-8")

        class Response:
            def __init__(self, body: bytes, status: int = 200) -> None:
                self.body = body
                self.status = status

            def read(self, limit: int) -> bytes:
                return self.body

            def close(self) -> None:
                pass

        def offline(request: object, timeout: int) -> Response:
            raise OSError("offline")

        openers = (
            offline,
            lambda request, timeout: Response(b"not json"),
            lambda request, timeout: Response(b'{"message":"rate limit"}'),
            lambda request, timeout: Response(b"[]", status=429),
            lambda request, timeout: Response(b"[{\"tag_name\":\"v1.18.0\"}]"),
        )
        with patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)}):
            for number, opener in enumerate(openers):
                with self.subTest(opener=opener):
                    self.assertIsNone(
                        VERSION.check_for_update(
                            now=1000,
                            opener=opener,
                            manifest=manifest,
                            cache=self.root / f"cache-{number}.json",
                        )
                    )

    def test_version_advisory_caches_network_failure(self) -> None:
        manifest = self.root / "plugin.json"
        manifest.write_text(json.dumps({"version": "1.17.0"}), encoding="utf-8")
        calls = 0

        def offline(request: object, timeout: int) -> None:
            nonlocal calls
            calls += 1
            raise OSError("offline")

        with patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)}):
            first = VERSION.check_for_update(now=1000, opener=offline, manifest=manifest)
            second = VERSION.check_for_update(now=1001, opener=offline, manifest=manifest)
        self.assertIsNone(first)
        self.assertIsNone(second)
        self.assertEqual(calls, 1)
        cache = json.loads(
            (self.codex_home / "state/lean-sdlc/version_advisory.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(cache, {"checked_at": 1000, "latest": None, "notified_for": None})

    def test_hook_config_limits_version_advisory_to_startup(self) -> None:
        hooks = json.loads(
            (ROOT / "plugins/lean-sdlc/hooks/hooks.json").read_text(encoding="utf-8")
        )
        entries = hooks["hooks"]["SessionStart"]
        advisory = [entry for entry in entries if "version_advisory.py" in entry["hooks"][0]["command"]]
        self.assertEqual(len(advisory), 1)
        self.assertEqual(advisory[0]["matcher"], "startup")
        self.assertIn("${PLUGIN_ROOT}", advisory[0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
