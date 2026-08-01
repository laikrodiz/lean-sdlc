from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/lean-sdlc"
SKILL = PLUGIN / "skills/lean-sdlc"
SCRIPTS = SKILL / "scripts"
TASKS = SCRIPTS / "tasks.py"
CHECK = SCRIPTS / "lean_check.py"
INIT = SCRIPTS / "init_repo.py"
OWNER_HOOK = SCRIPTS / "session_owner.py"
CONFIGURE_CODEX = SCRIPTS / "configure_codex.py"
LUNA_PROFILE = SKILL / "assets/lean_sdlc_luna.toml"
PLUGIN_HOOKS = PLUGIN / "hooks/hooks.json"
HEADER = (
    "Task ID,Title,Status,Context,Dependencies,Owner,"
    "Acceptance Criteria,Proof,Evidence\n"
)


def run(*arguments: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def task(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return run(str(TASKS), "--repo", str(repository), *arguments)


def configure_codex(
    codex_home: Path, *arguments: str
) -> subprocess.CompletedProcess[str]:
    return run(str(CONFIGURE_CODEX), "--codex-home", str(codex_home), *arguments)


def write_ledger(repository: Path, body: str, *, legacy_path: bool = False) -> Path:
    path = (
        repository / "planning/tasks.csv"
        if legacy_path
        else repository / "tasks.csv"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def read_rows(repository: Path) -> list[dict[str, str]]:
    with (repository / "tasks.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class TaskLedgerTests(unittest.TestCase):
    def test_concurrent_plan_and_start_transactions_get_unique_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")
            processes: list[subprocess.Popen[str]] = []
            for number in range(12):
                command = [
                    sys.executable,
                    str(TASKS),
                    "--repo",
                    str(repository),
                    "start" if number % 2 else "plan",
                    "--title",
                    f"Task {number}",
                    "--context",
                    "Project",
                    "--acceptance",
                    "Row exists",
                    "--proof",
                    "Read ledger",
                ]
                if number % 2:
                    command.extend(["--owner", "12345678"])
                processes.append(
                    subprocess.Popen(
                        command,
                        cwd=ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    )
                )

            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(
                all(process.returncode == 0 for process in processes),
                results,
            )
            rows = read_rows(repository)
            ids = [row["Task ID"] for row in rows]
            self.assertEqual(len(ids), 12)
            self.assertEqual(len(set(ids)), 12)
            self.assertEqual(
                {row["Owner"] for row in rows if row["Status"] == "In Progress"},
                {"12345678"},
            )
            self.assertFalse(repository.joinpath(".tasks.lock").exists())

    def test_planned_work_updates_then_starts_under_one_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            planned = task(
                repository,
                "plan",
                "--title",
                "Initial title",
                "--context",
                "Project",
                "--acceptance",
                "Done",
                "--proof",
                "Run checks",
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)

            updated = task(
                repository,
                "update",
                "TASK-000",
                "--title",
                "Corrected title",
            )
            self.assertEqual(updated.returncode, 0, updated.stderr)

            started = task(
                repository,
                "start",
                "TASK-000",
                "--owner",
                "12345678",
            )
            self.assertEqual(started.returncode, 0, started.stderr)

            denied = task(
                repository,
                "update",
                "TASK-000",
                "--owner",
                "87654321",
                "--title",
                "Wrong owner",
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("belongs to owner 12345678", denied.stderr)

            allowed = task(
                repository,
                "update",
                "TASK-000",
                "--owner",
                "12345678",
                "--proof",
                "Run the final checks",
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Title"], "Corrected title")
            self.assertEqual(row["Owner"], "12345678")
            self.assertEqual(row["Status"], "In Progress")

    def test_only_owner_closes_without_direct_user_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,Owned work,In Progress,Project,,11111111,"
                "Done,Run checks,\n",
            )
            denied = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("belongs to owner 11111111", denied.stderr)

            allowed = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "22222222",
                "--evidence",
                "Checks passed",
                "--user-override",
                "--override-reason",
                "User requested closure in this task",
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            row = read_rows(repository)[0]
            self.assertEqual(row["Status"], "Done")
            self.assertIn("Direct user override", row["Evidence"])

    def test_dependencies_must_exist_remain_acyclic_and_finish_before_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(repository, "")

            first = task(
                repository,
                "plan",
                "--title",
                "First",
                "--context",
                "Project",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertEqual(first.returncode, 0, first.stderr)

            second = task(
                repository,
                "start",
                "--owner",
                "12345678",
                "--title",
                "Second",
                "--context",
                "Project",
                "--dependencies",
                "TASK-000",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertEqual(second.returncode, 0, second.stderr)

            blocked_close = task(
                repository,
                "close",
                "TASK-001",
                "--owner",
                "12345678",
                "--evidence",
                "Done",
            )
            self.assertNotEqual(blocked_close.returncode, 0)
            self.assertIn("unfinished dependencies", blocked_close.stderr)

            cycle = task(
                repository,
                "update",
                "TASK-000",
                "--dependencies",
                "TASK-001",
            )
            self.assertNotEqual(cycle.returncode, 0)
            self.assertIn("dependency cycle", cycle.stderr)

            missing = task(
                repository,
                "plan",
                "--title",
                "Missing dependency",
                "--context",
                "Project",
                "--dependencies",
                "TASK-999",
                "--acceptance",
                "Done",
                "--proof",
                "Check",
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("depends on missing task TASK-999", missing.stderr)

            self.assertEqual(len(read_rows(repository)), 2)

    def test_legacy_path_and_header_upgrade_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            planning = repository / "planning"
            planning.mkdir()
            legacy = planning / "tasks.csv"
            legacy.write_text(
                "task_id,title,status,parent_ref,depends_on,owner,"
                "acceptance,proof,evidence\n"
                "TASK-001,Upgrade,In Progress,REPO,,11111111,"
                "Readable,Inspect,\n",
                encoding="utf-8",
            )
            result = task(
                repository,
                "upgrade",
                "--task",
                "TASK-001",
                "--owner",
                "11111111",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            root_ledger = repository / "tasks.csv"
            self.assertTrue(root_ledger.is_file())
            self.assertEqual(
                root_ledger.read_text(encoding="utf-8").splitlines()[0],
                HEADER.strip(),
            )
            self.assertFalse(legacy.exists())
            self.assertFalse(planning.exists())

    def test_previous_root_header_upgrade_maps_parent_to_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            old_header = (
                "Task ID,Title,Status,Parent,Dependencies,Owner,"
                "Acceptance Criteria,Proof,Evidence\n"
            )
            repository.joinpath("tasks.csv").write_text(
                old_header
                + "TASK-001,Upgrade,In Progress,REPO,,11111111,"
                "Readable,Inspect,\n",
                encoding="utf-8",
            )

            result = task(
                repository,
                "upgrade",
                "--task",
                "TASK-001",
                "--owner",
                "11111111",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            root_ledger = repository / "tasks.csv"
            self.assertEqual(
                root_ledger.read_text(encoding="utf-8").splitlines()[0],
                HEADER.strip(),
            )
            self.assertEqual(read_rows(repository)[0]["Context"], "Project")
            self.assertFalse(repository.joinpath(".tasks.lock").exists())

    def test_checker_rejects_manual_dependency_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            write_ledger(
                repository,
                "TASK-001,One,Planned,Project,TASK-002,,Done,Check,\n"
                "TASK-002,Two,Planned,Project,TASK-001,,Done,Check,\n",
            )
            checked = run(str(CHECK), str(repository), "--task", "TASK-001")
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("dependency cycle", checked.stdout)

    def test_owner_hook_is_stable_and_plugin_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            repository.joinpath("AGENTS.md").write_text(
                "Use $lean-sdlc for repository work.\n",
                encoding="utf-8",
            )
            write_ledger(repository, "")
            nested = repository / "src"
            nested.mkdir()
            event = json.dumps(
                {
                    "session_id": "019f71b5-b7e1-78f2-a426-1b7a95d87348",
                    "hook_event_name": "SessionStart",
                    "cwd": str(nested),
                    "model": "test",
                }
            )
            first = run(str(OWNER_HOOK), input_text=event)
            second = run(str(OWNER_HOOK), input_text=event)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            message = json.loads(first.stdout)["systemMessage"]
            owner = message.split(": ", 1)[1].split(".", 1)[0]
            self.assertRegex(owner, r"^\d{8}$")

        with tempfile.TemporaryDirectory() as directory:
            outside = json.dumps(
                {
                    "session_id": "019f71b5-b7e1-78f2-a426-1b7a95d87348",
                    "hook_event_name": "SessionStart",
                    "cwd": directory,
                    "model": "test",
                }
            )
            quiet = run(str(OWNER_HOOK), input_text=outside)
            self.assertEqual(quiet.returncode, 0, quiet.stderr)
            self.assertEqual(quiet.stdout, "")

        hooks = json.loads(PLUGIN_HOOKS.read_text(encoding="utf-8"))
        command = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("${PLUGIN_ROOT}", command)
        self.assertNotIn("CODEX_HOME", command)

    def test_initializer_creates_only_minimal_contract_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            first = run(str(INIT), str(repository))
            self.assertEqual(first.returncode, 0, first.stderr)

            self.assertTrue(repository.joinpath("AGENTS.md").is_file())
            self.assertTrue(repository.joinpath("docs/PROJECT.md").is_file())
            self.assertTrue(repository.joinpath("tasks.csv").is_file())
            ignores = repository.joinpath(".gitignore").read_text(encoding="utf-8")
            self.assertIn("/tasks.csv", ignores.splitlines())
            self.assertIn("/.tasks.lock", ignores.splitlines())
            self.assertFalse(repository.joinpath("README.md").exists())
            self.assertFalse(repository.joinpath(".codex/hooks.json").exists())
            self.assertFalse(repository.joinpath("docs/OPERATIONS.md").exists())
            self.assertFalse(repository.joinpath("docs/FEATURE_INDEX.csv").exists())
            self.assertFalse(repository.joinpath("docs/DECISION_INDEX.csv").exists())

            before_write = run(
                str(CHECK),
                str(repository),
                "--before-write",
                "--task",
                "TASK-000",
                "--owner",
                "bootstrap",
            )
            self.assertEqual(
                before_write.returncode,
                0,
                before_write.stdout + before_write.stderr,
            )
            full = run(str(CHECK), str(repository), "--task", "TASK-000")
            self.assertEqual(full.returncode, 0, full.stdout + full.stderr)

            closed = task(
                repository,
                "close",
                "TASK-000",
                "--owner",
                "bootstrap",
                "--evidence",
                "Minimal contract checked",
            )
            self.assertEqual(closed.returncode, 0, closed.stderr)

            repeated = run(str(INIT), str(repository))
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("0 control change(s)", repeated.stdout)
            self.assertEqual(len(read_rows(repository)), 1)

    def test_initializer_preserves_existing_project_truth(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            docs = repository / "docs"
            docs.mkdir()
            repository.joinpath("AGENTS.md").write_text("existing rules\n", encoding="utf-8")
            docs.joinpath("PROJECT.md").write_text("existing truth\n", encoding="utf-8")
            repository.joinpath(".gitignore").write_text(
                "dist/\n/tasks.csv\n",
                encoding="utf-8",
            )

            initialized = run(str(INIT), str(repository))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            self.assertEqual(
                repository.joinpath("AGENTS.md").read_text(encoding="utf-8"),
                "existing rules\n",
            )
            self.assertEqual(
                docs.joinpath("PROJECT.md").read_text(encoding="utf-8"),
                "existing truth\n",
            )
            ignores = repository.joinpath(".gitignore").read_text(encoding="utf-8")
            self.assertEqual(
                ignores.splitlines(),
                ["dist/", "/tasks.csv", "/.tasks.lock"],
            )


class PackageContractTests(unittest.TestCase):
    def test_package_contains_one_skill_and_no_legacy_lanes(self) -> None:
        self.assertEqual(
            {path.name for path in PLUGIN.iterdir()},
            {".codex-plugin", "hooks", "skills"},
        )
        self.assertFalse(
            any(
                path.name in {"__pycache__", ".DS_Store"} or path.suffix == ".pyc"
                for path in PLUGIN.rglob("*")
            )
        )

        skill_roots = sorted(
            path.parent.name for path in PLUGIN.glob("skills/*/SKILL.md")
        )
        self.assertEqual(skill_roots, ["lean-sdlc"])

        references = SKILL / "references"
        names = {path.name for path in references.glob("*.md")}
        self.assertTrue(
            {
                "shape.md",
                "decide.md",
                "plan.md",
                "diagnose.md",
                "deliver.md",
                "verify.md",
                "model-routing.md",
                "subagents.md",
                "operations.md",
                "repository-contracts.md",
                "trigger-evals.md",
            }.issubset(names)
        )
        self.assertNotIn("agent-coordination.md", names)
        self.assertTrue(
            names.isdisjoint(
                {
                    "brainstorm.md",
                    "refine.md",
                    "architecture.md",
                    "task-planning.md",
                    "execution.md",
                    "debugging.md",
                    "implementation.md",
                    "verification.md",
                    "traceability.md",
                    "versioning.md",
                    "doc-maintenance.md",
                    "lifecycle.md",
                }
            )
        )

    def test_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        for document in SKILL.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = (document.parent / target.split("#", 1)[0]).resolve()
                if not path.exists():
                    failures.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])

    def test_dispatcher_trigger_is_explicit_and_model_floor_has_no_assignment_to_low(
        self,
    ) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = dispatcher.split("---", 2)[1]
        self.assertIn("explicitly invokes Lean-SDLC", frontmatter)
        self.assertIn("repository AGENTS.md requires Lean-SDLC", frontmatter)
        self.assertIn("Do not invoke implicitly for read-only work", frontmatter)

        policy_files = [
            ROOT / "README.md",
            SKILL / "assets/AGENTS.md",
            SKILL / "references/model-routing.md",
            SKILL / "references/subagents.md",
        ]
        policy = "\n".join(path.read_text(encoding="utf-8") for path in policy_files)
        self.assertNotIn("GPT-5.4", policy)
        self.assertNotRegex(policy, r"\|\s*`?low`?\s*\|")

    def test_minimal_modularity_edge_cases_and_diagrams_are_explicit(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        decide = (SKILL / "references/decide.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        self.assertIn("smallest cohesive units", dispatcher)
        self.assertIn("project-size", decide)
        self.assertIn("readable orchestrator", deliver)
        self.assertIn("handle", deliver)
        self.assertIn("reject", deliver)
        self.assertIn("defer", deliver)
        self.assertIn("impossible by invariant", deliver)
        self.assertIn("change locality", verify)
        self.assertIn("mermaid", contracts)
        self.assertIn("ascii pseudographics", contracts)
        self.assertIn("plausible edge cases", evaluations)

    def test_work_boundaries_keep_tasks_atomic_and_steps_transient(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        template = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        decide = (SKILL / "references/decide.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        contracts = (
            SKILL / "references/repository-contracts.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()

        self.assertIn(
            "each task is one independently accepted repository state; local implementation steps stay transient.",
            dispatcher,
        )
        self.assertIn(
            "each task is one independently accepted repository state and remains resumable from repository truth and its ledger row after compaction.",
            agents,
        )
        self.assertIn(
            "split independently accepted and independently proved work. keep inseparable coding steps transient.",
            agents,
        )
        self.assertEqual(agents, template)

        for phrase in [
            "group the current outcome in the project promise.",
            "use an optional feature document when one durable behavior spans tasks.",
            "split a feature when a part has an independent promise, test, or change.",
            "merge feature candidates when neither part has useful behavior alone.",
        ]:
            self.assertIn(phrase, shape)

        self.assertIn(
            "record one decision for one independent reversal boundary.",
            decide,
        )
        self.assertIn(
            "keep a choice local when it is cheap to reverse and clear in code, tests, or technical documentation.",
            decide,
        )

        for phrase in [
            "one durable task represents one independently accepted repository state.",
            "the task owns one observable outcome, one coherent change boundary, one acceptance set, one proof set, and one close decision.",
            "the task must resume from repository truth and its ledger row after compaction.",
            "split a task when a part can fail, ship, revert, resume, or close independently.",
            "split a task when a part needs different proof.",
            "split a task when a part crosses a contract.",
            "split a task when a part needs another durable decision.",
            "merge rows when they only describe inseparable coding mechanics.",
            "avoid fixed limits based on time, lines, or file count.",
            "shape the nearest dependency frontier fully. keep later work coarse until its dependencies become current.",
            "engineer receives one durable task.",
            "local implementation steps and correction handoffs remain transient.",
            "never send several tasks or an internal backlog.",
        ]:
            self.assertIn(phrase, plan)

        for phrase in [
            "## work hierarchy",
            "- project promise: current outcome, scope, stage, and exit evidence.",
            "- feature: durable behavior that spans tasks.",
            "- task: one independently accepted repository state with one change boundary, acceptance set, proof set, and close decision.",
            "- local step: transient implementation or correction work that does not become a ledger row.",
            "## task sizing summary",
            "split or merge tasks by the independent boundaries in [plan.md](plan.md).",
        ]:
            self.assertIn(phrase, contracts)

        self.assertIn(
            "a large synthesizer-clone request contains several independently verifiable outcomes",
            evaluations,
        )
        self.assertIn(
            "create several independently verifiable tasks and start only the nearest ready task",
            evaluations,
        )

    def test_implementation_authority_and_visible_plan_gate_are_explicit(self) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        shape = (SKILL / "references/shape.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()

        for phrase in [
            "require the information, not fixed labels",
            "use natural prose for the outcome, important constraints, and exclusions",
            "only the plan needs visible structure",
            "before creating a task or implementing work",
            "natural intent confirmation",
            "concise visible plan",
            "define each durable plan item in natural prose",
            "observable completion condition and verification method",
            "the verification method is its proof",
            "each durable item includes observable completion conditions and proof",
            "a one-item plan is valid",
            "only durable task plan",
        ]:
            self.assertIn(phrase, plan)

        self.assertIn("explicit implementation authority", dispatcher + shape + deliver)
        self.assertIn("discussion or proposal requests remain read-only", shape + deliver)
        self.assertIn("clear confirmation to proceed against a recoverable agreed proposal", dispatcher + shape + subagents)
        self.assertIn("if authority is ambiguous, remain read-only", dispatcher + shape + subagents)
        self.assertIn("each durable plan item maps to one task", subagents)
        self.assertIn("implementation steps and correction handoffs remain transient", plan + subagents)

        self.assertIn(
            "engineer cannot start until the visible plan exists",
            subagents,
        )
        self.assertIn(
            "the task matches one durable plan item",
            plan + subagents + deliver,
        )
        self.assertIn("discussion or proposal request", evaluations)
        self.assertIn("ambiguous implementation authority", evaluations)
        self.assertIn("i am thinking about x; what do you think?", evaluations)
        self.assertIn("implement the agreed x proposal", evaluations)
        self.assertIn(
            "perform a natural restatement and show the visible plan before task creation",
            evaluations,
        )
        self.assertIn('"proceed" when no agreed proposal is recoverable', evaluations)
        self.assertIn("one-item visible plan", evaluations)
        self.assertIn("engineer trigger", evaluations)
        self.assertEqual(root_agents, template_agents)

    def test_subagent_policy_is_canonical_deterministic_and_explicit(
        self,
    ) -> None:
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8")
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8")

        for term in [
            "sole authority",
            "mandatory sidecar triggers",
            "engineer trigger and loop",
            "lead authority",
            "principal engineer",
            "product or architecture decision",
            "boundaries and invariants",
            "non-goals",
            "architecture alignment",
            "decision reopened",
            "delegation is mandatory",
            "one writing engineer active per architect",
            "task_name=role_firstname",
            "simple human first name",
            "role firstname",
            "context reset reason",
            "replacement action",
            "arbitrary counter",
            "disjoint paths",
            "before every spawn",
            "fork_turns",
            "routing failure",
            "gpt-5.6 luna `max`",
            "gpt-5.6 terra `xhigh`",
            "user-selected lead",
            "agent_type=lean_sdlc_luna",
            "service_tier=priority",
            "approved concise lowercase snake_case responsibility name",
            "material phase changes",
            "two heartbeats per command",
        ]:
            self.assertIn(term, subagents + dispatcher)
        for term in [
            "lead alone decide task disposition",
            "must reuse or start verifier",
            "must reuse or start maintainer",
            "must reuse or start engineer",
            "must reuse or start read-only researcher",
            "follow-up to the existing role thread",
            "do not spawn another child for that role",
            "directly spawn terra `xhigh`",
            "inherits an automatic model",
        ]:
            self.assertIn(term, verify + evaluations)
        self.assertIn("retry luna max", subagents)
        self.assertIn("shorthand tool names", verify)
        self.assertEqual(root_agents, template_agents)

        policy_documents = [ROOT / "README.md", ROOT / "docs/PROJECT.md", *SKILL.rglob("*.md")]
        policy = "\n".join(
            document.read_text(encoding="utf-8").lower()
            for document in policy_documents
        )
        self.assertNotIn("operator", policy)
        self.assertNotIn("service_tier=fast", policy)
        self.assertNotIn("gpt-5.6 terra `high`", policy)
        self.assertNotIn("explicitly spawn terra `high`", policy)

        for document in policy_documents:
            for line in document.read_text(encoding="utf-8").splitlines():
                self.assertNotIn(
                    "luna `xhigh`",
                    line.lower(),
                    f"{document}: {line}",
                )

    def test_child_identities_replacements_and_commentary_are_human_monitorable(
        self,
    ) -> None:
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
        developer = profile["developer_instructions"].lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8").lower()
        project = ROOT.joinpath("docs/PROJECT.md").read_text(encoding="utf-8").lower()

        for term in [
            "simple human first name",
            "role firstname",
            "role_firstname",
            "identity stable",
            "thread remains reusable",
            "reachable child per role",
            "another unused",
            "role prefix",
            "reset reason",
            "task identifier",
            "material phases",
            "planned proof",
            "current work or state",
            "greetings",
            "sentence templates",
            "heartbeat limits",
        ]:
            self.assertIn(term, subagents)

        for term in [
            "standard child identity",
            "replacement is required",
            "first visible update",
            "later material phase",
            "i am thinking about x",
            "implement the agreed x proposal",
            "proceed",
        ]:
            self.assertIn(term, evaluations)

        for document in [dispatcher, developer]:
            for term in ["simple human first name", "task name", "natural prose"]:
                self.assertIn(term, document)
        self.assertIn("inside your own agent task", developer)
        self.assertIn("short plain-language commentary", subagents)
        self.assertEqual(root_agents, template_agents)
        self.assertIn("canonical child-agent policy", readme)
        self.assertIn("existing engineer role thread", subagents)
        self.assertIn("existing researcher role thread", subagents)
        self.assertIn("task identifiers", evaluations)
        policy_documents = [
            subagents,
            deliver,
            plan,
            verify,
            readme,
            project,
            root_agents,
            template_agents,
            developer,
        ]
        for document in policy_documents:
            self.assertNotIn("common " + "american first name", document)
            self.assertNotRegex(document, r"(?i)\b(?:hello|hi)\s*,")
            self.assertNotRegex(document, r"(?i)\bi\s+am\s+<role/name>")
            self.assertNotRegex(document, r"(?i)\bstarting task-\d+\b")
            for role, first_name in zip(
                ["engineer", "maintainer", "verifier", "researcher"],
                ["d" + "avid", "e" + "mily", "m" + "ichael", "s" + "arah"],
            ):
                self.assertNotIn(f"{role} {first_name}", document)
                self.assertNotIn(f"{role}_{first_name}", document)
        for role in ["engineer", "maintainer", "verifier", "researcher"]:
            self.assertIn(f"role: {role} firstname", subagents)
            self.assertIn(f"task name: {role}_firstname", subagents)

    def test_visible_communication_contract_is_natural_and_returns_stay_lossless(
        self,
    ) -> None:
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        plan = (SKILL / "references/plan.md").read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
        developer = profile["developer_instructions"].lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8").lower()
        project = ROOT.joinpath("docs/PROJECT.md").read_text(encoding="utf-8").lower()

        policy = "\n".join(
            [subagents, evaluations, dispatcher, developer, plan, deliver, readme, project]
        )
        for term in [
            "task",
            "inquiry",
            "intended result",
            "boundaries",
            "acceptance",
            "proof",
            "checkpoint",
            "deviation",
            "natural prose",
            "sentence template",
            "lossless",
        ]:
            self.assertIn(term, policy)

        for field in [
            "role:",
            "task:",
            "task name:",
            "outcome:",
            "architecture:",
            "acceptance:",
            "proof:",
            "stop conditions:",
            "result:",
            "files changed:",
            "targeted checks:",
            "task checkpoint:",
            "deviation or decision needed:",
            "cited findings:",
            "conflicts:",
            "unknowns:",
            "decision impact:",
            "sources:",
            "status:",
            "evidence or artifacts:",
            "issue or risk:",
            "next:",
        ]:
            self.assertIn(field, subagents)

        self.assertIn("concise natural update", dispatcher)
        self.assertIn("natural prose", plan + deliver + developer + root_agents)
        self.assertIn("canonical child-agent policy", readme)
        self.assertEqual(readme.count("plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md"), 1)
        self.assertEqual(root_agents, template_agents)

        self.assertNotIn(
            "tell the user the mode, child action, active task or inquiry, and reason in one or two short sentences",
            dispatcher,
        )
        for document in [
            subagents,
            evaluations,
            dispatcher,
            developer,
            root_agents,
            template_agents,
            readme,
            project,
        ]:
            self.assertNotRegex(document, r"(?i)\b(?:hello|hi)\s*,")
            self.assertNotRegex(document, r"(?i)\bi\s+am\s+<role/name>")
            self.assertNotRegex(document, r"(?i)\bstarting task-\d+\b")

        self.assertIn("assisted and solo are the only orchestration modes", subagents)
        self.assertIn("assisted and solo are the only orchestration modes", dispatcher)
        self.assertIn("assisted and solo are the only orchestration modes", readme)
        self.assertIn("assisted and solo are the only orchestration modes", project)
        self.assertIn("targeted", subagents)
        for document in [
            subagents,
            dispatcher,
            developer,
            root_agents,
            template_agents,
            readme,
            project,
        ]:
            self.assertNotIn(
                "child commentary does not repeat its own name or role when the task title or lead assignment identifies it",
                document,
            )
            self.assertNotIn(
                "child identity is allowed only after replacement or genuine ambiguity",
                document,
            )
        current_policy = "\n".join(
            [subagents, dispatcher, plan, deliver, developer, root_agents, template_agents, readme, project]
        )
        for disallowed_mode in ["focused mode", "parallel mode", "review mode"]:
            self.assertNotIn(disallowed_mode, current_policy)

    def test_readme_stays_public_and_links_detailed_policy(self) -> None:
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        lowered = readme.lower()

        for term in ["shape", "decide", "plan", "diagnose", "deliver", "verify"]:
            self.assertIn(term, lowered)
        self.assertIn("canonical child-agent policy", lowered)
        self.assertEqual(
            lowered.count("plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md"),
            1,
        )
        for pattern in [
            r"multi-agent v2",
            r"\bgpt-\d",
            r"\b(?:luna|terra|xhigh|service_tier|priority|reasoning_effort)\b",
            r"\b(?:greeting|self-introduction|sentence template)\b",
            r"\b(?:heartbeat|two minutes)\b",
            r"\b(?:handoff|checkpoint|deviation|task name)\b",
        ]:
            self.assertIsNone(re.search(pattern, lowered), pattern)

    def test_children_address_primary_agent_as_architect(self) -> None:
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        dispatcher = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
        developer = profile["developer_instructions"].lower()
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()
        template_agents = (
            SKILL / "assets/AGENTS.md"
        ).read_text(encoding="utf-8").lower()
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8").lower()
        project = ROOT.joinpath("docs/PROJECT.md").read_text(encoding="utf-8").lower()

        for document in [dispatcher, subagents]:
            for term in [
                "primary agent",
                "architect",
                "visible commentary",
                "handoffs",
                "returns",
                "decision requests",
                "speaks as i",
            ]:
                self.assertIn(term, document)
        for term in ["child refers to the primary agent", "architect-supplied outcome", "architect supplies question"]:
            self.assertIn(term, evaluations)
        self.assertIn(
            "plugins/lean-sdlc/skills/lean-sdlc/references/subagents.md",
            readme,
        )

        self.assertIn("architect speaks as i", developer)
        self.assertNotIn("lead", developer)
        self.assertNotIn("from the lead", subagents)
        self.assertNotIn("lead decision", subagents)
        self.assertNotIn("lead-owned task", subagents)
        self.assertIn("from the architect", subagents)
        self.assertIn("decision to the architect", evaluations)

    def test_role_contracts_separate_execution_research_proof_and_operations(
        self,
    ) -> None:
        subagents = (
            SKILL / "references/subagents.md"
        ).read_text(encoding="utf-8").lower()
        deliver = (SKILL / "references/deliver.md").read_text(encoding="utf-8").lower()
        verify = (SKILL / "references/verify.md").read_text(encoding="utf-8").lower()
        operations = (
            SKILL / "references/operations.md"
        ).read_text(encoding="utf-8").lower()
        evaluations = (
            SKILL / "references/trigger-evals.md"
        ).read_text(encoding="utf-8").lower()
        profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
        root_agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8").lower()

        for term in [
            "durable task",
            "decision envelope",
            "local implementation mechanics",
            "task checkpoint",
            "architect reviews",
            "correction",
            "researcher",
            "read-only",
            "architect evaluates",
            "verifier",
            "acceptance-defining proof",
            "risk-based regression",
            "maintainer evidence",
            "exact procedure",
            "question and source boundary",
            "preferred answer",
        ]:
            self.assertIn(term, subagents)
        for term in ["one durable task", "one outcome", "checkpoint", "correction delta"]:
            self.assertIn(term, deliver)
        for term in [
            "acceptance-defining proof",
            "risk-based regression",
            "engineer-only targeted checks",
            "full suite",
            "maintainer evidence",
            "solo mode",
        ]:
            self.assertIn(term, verify)
        for term in ["state-changing operation", "maintainer trigger", "required architect action"]:
            self.assertIn(term, operations)
        for field in ["role: researcher", "inquiry:", "decision informed:"]:
            self.assertIn(field, subagents)
        for term in [
            "evidence collection",
            "known source",
            "researcher receives",
            "researcher returns",
            "read-only",
            "repository writes",
            "solo mode",
            "snake_case responsibility",
            "additional role name",
            "correction",
            "returned checkpoint",
        ]:
            self.assertIn(term, evaluations)
        for term in ["architecture", "interfaces", "task state", "acceptance", "integration", "closeout", "architect"]:
            self.assertIn(term, root_agents)
        self.assertIn("reuse the existing engineer role thread", subagents)
        self.assertIn("researcher is read-only", subagents)
        self.assertEqual(profile["model"], "gpt-5.6-luna")
        self.assertEqual(profile["model_reasoning_effort"], "max")
        self.assertIn("Researcher", profile["description"])
        self.assertIn("Use that role: Engineer, Maintainer, Verifier, or Researcher.", profile["developer_instructions"])

    def test_luna_profile_and_technical_english_rules_are_packaged(self) -> None:
        profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
        configure = CONFIGURE_CODEX.read_text(encoding="utf-8")
        subagents = (SKILL / "references/subagents.md").read_text(encoding="utf-8")
        policy = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                ROOT / "AGENTS.md",
                SKILL / "SKILL.md",
                SKILL / "references/subagents.md",
            ]
        ).lower()

        self.assertEqual(profile["name"], "lean_sdlc_luna")
        self.assertEqual(profile["model"], "gpt-5.6-luna")
        self.assertEqual(profile["model_reasoning_effort"], "max")
        self.assertIn("Engineer, Maintainer, Verifier, or Researcher", profile["description"])
        self.assertIn("agent_type=lean_sdlc_luna", subagents)
        self.assertIn("gpt-5.6-terra", subagents)
        self.assertIn("reasoning_effort=xhigh", subagents)
        self.assertNotIn("model_catalog_json", configure)
        for phrase in [
            "asd-ste100 issue 9",
            "active voice",
            "20 words or fewer",
            "25 words or fewer",
            "one term for one meaning",
            "conditions before actions",
            "american english spelling",
            "idioms, unnecessary synonyms, and vague pronouns",
            "preserve code, commands, paths, identifiers, protocol fields, quotations",
            "certified or full controlled-dictionary compliance",
        ]:
            self.assertIn(phrase, policy)

    def test_release_version_is_consistent(self) -> None:
        manifest = json.loads(
            PLUGIN.joinpath(".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        version = manifest["version"]
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        project = ROOT.joinpath("docs/PROJECT.md").read_text(encoding="utf-8")

        self.assertEqual(version, "1.8.2")
        self.assertIn(f"`v{version}`", readme)
        self.assertIn(f"- Version: {version}", project)
        self.assertIn(
            "- Version goal: Release intentional planning and human-monitorable children",
            project,
        )


class CodexConfigurationTests(unittest.TestCase):
    def assert_v2_configuration(self, config: dict[str, object]) -> None:
        features = config["features"]
        self.assertIsInstance(features, dict)
        self.assertTrue(features["multi_agent"])
        multi_agent_v2 = features["multi_agent_v2"]
        self.assertIsInstance(multi_agent_v2, dict)
        expected = {
            "enabled": True,
            "tool_namespace": "agents",
            "hide_spawn_agent_metadata": False,
            "expose_spawn_agent_model_overrides": True,
            "wait_agent_enabled": True,
        }
        for key, value in expected.items():
            self.assertEqual(multi_agent_v2[key], value)

    def test_configuration_creation_enables_luna_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory) / "codex"
            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)

            config = tomllib.loads(
                codex_home.joinpath("config.toml").read_text(encoding="utf-8")
            )
            self.assert_v2_configuration(config)
            self.assertEqual(
                config["agents"]["lean_sdlc_luna"]["config_file"],
                "agents/lean_sdlc_luna.toml",
            )
            source_profile = tomllib.loads(LUNA_PROFILE.read_text(encoding="utf-8"))
            generated_description = config["agents"]["lean_sdlc_luna"]["description"]
            self.assertEqual(generated_description, source_profile["description"])
            self.assertIn("Architect", generated_description)
            self.assertNotIn("lead", generated_description.lower())
            self.assertEqual(
                codex_home.joinpath("agents/lean_sdlc_luna.toml").read_text(
                    encoding="utf-8"
                ),
                LUNA_PROFILE.read_text(encoding="utf-8"),
            )

    def test_legacy_agent_boolean_converts_to_profile_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            config_path = codex_home / "config.toml"
            config_path.write_text(
                "[agents]\nlean_sdlc_luna = false\nmax_threads = 3\n",
                encoding="utf-8",
            )

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            content = config_path.read_text(encoding="utf-8")
            self.assertNotIn("lean_sdlc_luna = false", content)
            self.assertIn("max_threads = 3", content)
            self.assertIn("[agents.lean_sdlc_luna]", content)
            self.assertIsInstance(
                tomllib.loads(content)["agents"]["lean_sdlc_luna"], dict
            )

    def test_legacy_v2_boolean_converts_to_configured_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            config_path = codex_home / "config.toml"
            config_path.write_text(
                "[features]\nmulti_agent_v2 = false\nkeep = true\n",
                encoding="utf-8",
            )

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            content = config_path.read_text(encoding="utf-8")
            self.assertNotIn("multi_agent_v2 = false", content)
            self.assertIn("keep = true", content)
            self.assertIn("[features.multi_agent_v2]", content)
            self.assert_v2_configuration(tomllib.loads(content))

    def test_existing_tables_update_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            config_path = codex_home / "config.toml"
            original = (
                'title = "Personal"\n\n'
                "[features]\n"
                "multi_agent = false # old value\n"
                "keep = true\n\n"
                "[features.multi_agent_v2]\n"
                "enabled = false\n"
                'tool_namespace = "collaboration"\n'
                "hide_spawn_agent_metadata = true\n"
                "expose_spawn_agent_model_overrides = false\n"
                "wait_agent_enabled = false\n"
                'custom_v2 = "kept"\n\n'
                "[agents.lean_sdlc_luna]\n"
                'description = "old"\n'
                'config_file = "old.toml"\n'
                'custom = "kept"\n'
            )
            config_path.write_text(original, encoding="utf-8")

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            content = config_path.read_text(encoding="utf-8")
            self.assertIn('title = "Personal"', content)
            self.assertIn("multi_agent = true # old value", content)
            self.assertIn("keep = true", content)
            self.assertIn('custom_v2 = "kept"', content)
            self.assertIn('custom = "kept"', content)
            self.assert_v2_configuration(tomllib.loads(content))
            self.assertEqual(
                config_path.with_name("config.toml.bak").read_text(encoding="utf-8"),
                original,
            )

    def test_configuration_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            first = configure_codex(codex_home)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = {
                path.relative_to(codex_home): path.read_bytes()
                for path in codex_home.rglob("*")
                if path.is_file()
            }

            second = configure_codex(codex_home)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("kept", second.stdout)
            after = {
                path.relative_to(codex_home): path.read_bytes()
                for path in codex_home.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)

    def test_check_mode_reports_missing_and_valid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory) / "codex"
            missing = configure_codex(codex_home, "--check")
            self.assertNotEqual(missing.returncode, 0)
            self.assertFalse(codex_home.exists())

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            before = {
                path.relative_to(codex_home): path.read_bytes()
                for path in codex_home.rglob("*")
                if path.is_file()
            }
            checked = configure_codex(codex_home, "--check")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("is configured", checked.stdout)
            after = {
                path.relative_to(codex_home): path.read_bytes()
                for path in codex_home.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)

    def test_existing_owned_profile_is_backed_up_before_installation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            profile_path = codex_home / "agents/lean_sdlc_luna.toml"
            profile_path.parent.mkdir()
            original = (
                'name = "lean_sdlc_luna"\n'
                'description = "old profile"\n'
                'developer_instructions = "old"\n'
            )
            profile_path.write_text(original, encoding="utf-8")

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            self.assertEqual(
                profile_path.with_name("lean_sdlc_luna.toml.bak").read_text(
                    encoding="utf-8"
                ),
                original,
            )
            self.assertEqual(
                profile_path.read_text(encoding="utf-8"),
                LUNA_PROFILE.read_text(encoding="utf-8"),
            )

    def test_unrelated_configuration_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            config_path = codex_home / "config.toml"
            unrelated = (
                'model = "gpt-5.6-sol"\n'
                "[mcp_servers.example]\n"
                'command = "example"\n\n'
                '[projects."/work"]\n'
                'trust_level = "trusted"\n'
            )
            config_path.write_text(unrelated, encoding="utf-8")

            configured = configure_codex(codex_home)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            content = config_path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith(unrelated))
            tomllib.loads(content)


if __name__ == "__main__":
    unittest.main()
