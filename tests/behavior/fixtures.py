"""Fresh public pilot fixtures. Never run maintenance in a user-supplied directory."""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from score import inventory

REPO = Path(__file__).resolve().parents[2]
HELPERS = REPO / "plugins/lean-sdlc/skills/lean-sdlc/scripts"


def command(root, *args):
    result = subprocess.run(args, cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"fixture setup failed: {result.stdout} {result.stderr}")
    return result


def initialize(root):
    command(root, sys.executable, "-B", HELPERS / "init_repo.py", root)
    command(root, sys.executable, "-B", HELPERS / "lean_check.py", root, "--task", "TASK-000")
    transact(root, "close", "TASK-000", "--owner", "bootstrap", "--evidence",
             "Initial structural check passed; starting project files retained.")


def transact(root, *args):
    return command(root, sys.executable, "-B", HELPERS / "tasks.py", "--repo", root, *args)


def populate(root, family):
    if any(root.iterdir()):
        raise ValueError("fixture directory must be empty")
    if family not in {case["id"] for case in inventory()}:
        raise ValueError(f"unknown family: {family}")
    if family not in {"discuss", "diagnose", "shape", "initialize", "storage"}:
        initialize(root)
    if family not in {"storage", "cleanup"}:
        (root / "duration.py").write_text(
            "def minutes(seconds):\n    return seconds // 60\n\n"
            "def render(seconds):\n    return f'{seconds} min'\n")
        (root / "test_duration.py").write_text(
            "from duration import render\nassert render(120) == '2 min', render(120)\n")
        (root / "user-notes.txt").write_text("Unrelated draft. Keep unchanged.\n")
    elif family in {"storage", "cleanup"}:
        (root / "README.md").write_text(
            "make cache recreates cache/pad.bin locally. The offline handoff is unique.\n")
        (root / "Makefile").write_text(".PHONY: cache\ncache:\n\tmkdir -p cache\n"
                                       "\tdd if=/dev/zero of=cache/pad.bin bs=8192 count=20\n")
        for name in ("cache", "handoff"):
            (root / name).mkdir()
        (root / "cache/pad.bin").write_bytes(bytes(8192 * 20))
        private = root / "handoff/private.bin"
        private.write_bytes(b"synthetic-only" * 8192)
        private.chmod(0o600)
    if family in {"discuss", "shape", "scout", "premise", "refactor"}:
        (root / "desk.py").write_text("from duration import render\nlabel = render(120)\n")
        (root / "kiosk.py").write_text("def label(ticks):\n    return str(ticks // 1000)\n")
        (root / "receipts.csv").write_text("ticks,unit\n120000,ms\n")
        (root / "retention.ini").write_text("[support]\ndays=30\n")
        (root / "README.md").write_text("Desktop input is seconds. Kiosk input is milliseconds. "
                                       "Support uses 30 days for lookup, not deletion.\n")
    if family in {"initialize", "upgrade"}:
        if family == "upgrade":
            old = REPO / "tests/fixtures/AGENTS-v1.24.3.txt"
            (root / "AGENTS.md").write_bytes(old.read_bytes())
        with (root / "AGENTS.md").open("a") as f:
            f.write("\nTeam rule: preserve the signed shift manifest.\n")
        (root / "README.md").write_text("The signed shift manifest is kept offline.\n")
    if family in {"backlog", "resume", "checkpoint"}:
        if family == "backlog":
            transact(root, "backlog-add", "--title", "Dispatch label", "--context", "Project")
        else:
            for number in range(1, 4 if family == "checkpoint" else 2):
                context = "Quick Fix" if family == "checkpoint" else "Project"
                transact(root, "start", "--check", "--owner", "00000011", "--context",
                         context, "--title", f"Dispatch string {number}",
                         "--acceptance", "Print the shift label", "--proof", "Run example")
                if family == "checkpoint" and number < 3:
                    transact(root, "close", f"TASK-{number:03}", "--owner", "00000011",
                             "--evidence", "Synthetic prior shift inspected the example")
    if family in {"operations", "scratch", "wait", "topic"}:
        (root / "package.py").write_text(
            "from pathlib import Path\nimport sys\n"
            "if sys.argv[1:] != ['desk']:\n    sys.exit('unknown target')\n"
            "Path('parcel-package.txt').write_text('desk-1\\n')\nprint('PACKED desk-1')\n")
        (root / "docs/OPERATIONS.md").write_text(
            "# Local desk package\nPreviously verified input: desk-1. "
            "Run `python3 package.py desk`. Require PACKED desk-1 and the matching file. "
            "No publish or recovery procedure.\n")
        (root / "build").mkdir()
        (root / "build/shift-draft.txt").write_text("Retain the offline shift draft.\n")
    if family in {"documentation", "docs-families", "handoff", "frozen", "support-profile"}:
        (root / "docs/shift-guide.md").write_text(
            "# Operator guide\nRun python3 dispatch.py --seconds 60. "
            "The documented output is 1 minute.\n")
        (root / "dispatch.py").write_text(
            "import argparse\np = argparse.ArgumentParser()\n"
            "p.add_argument('--elapsed', type=int, required=True)\n"
            "print(f'{p.parse_args().elapsed // 60} min')\n")


def control():
    # Old and fixed outputs must be distinguishable; the read-only reproduction
    # must not create local bytecode. These are controller checks, not model runs.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        populate(root, "diagnose")
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        env.pop("PYTHONPYCACHEPREFIX", None)
        def probe(flags):
            return subprocess.run([sys.executable, *flags, "test_duration.py"], cwd=root,
                                  capture_output=True, env=env)
        broken = probe(["-B"])
        assert broken.returncode != 0 and b"120 min" in broken.stderr
        assert not (root / "__pycache__").exists()
        assert probe([]).returncode != 0 and (root / "__pycache__").is_dir()
        mod = root / "duration.py"
        mod.write_text(mod.read_text().replace("{seconds} min", "{minutes(seconds)} min"))
        assert probe(["-B"]).returncode == 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        populate(root, "storage")
        cache = root / "cache/pad.bin"
        expected = cache.read_bytes()
        cache.unlink()
        subprocess.run(["make", "cache"], cwd=root, capture_output=True, check=True)
        assert cache.read_bytes() == expected
        assert (root / "handoff/private.bin").stat().st_mode & 0o777 == 0o600
    for case in inventory():
        with tempfile.TemporaryDirectory() as tmp:
            populate(Path(tmp), case["id"])


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("family", choices=["controls", *(case["id"] for case in inventory())])
    args = cli.parse_args()
    if args.family == "controls":
        if not __debug__:
            sys.exit("controls require enabled assertions")
        control()
        print("PASS: output oracle, bytecode side effect, cache restoration, private fixture")
    else:
        folder = Path(tempfile.mkdtemp(prefix="parcel-"))
        populate(folder, args.family)
        print(folder)
