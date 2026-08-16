from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins/lean-sdlc/skills/lean-sdlc/scripts"
SESSION_STATE = SCRIPTS / "session_state.py"
SPAWN_GUARD = SCRIPTS / "spawn_guard.py"


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


if __name__ == "__main__":
    unittest.main()
