"""Opt-in workstation release notices; never install or trust code."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time


def stable(tag):
    match = re.fullmatch(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", tag)
    return tuple(map(int, match.groups())) if match else ()


def settings():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "state/lean-sdlc/release-policy.json"


def load(path):
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
        json.dump(data, handle)
    os.replace(handle.name, path)


def refresh(data, lookup, now):
    if not data.get("follow") or now - data.get("checked", 0) < 86400:
        return data
    updated = dict(data, checked=now)
    try:
        tags = [line.split("refs/tags/")[-1] for line in lookup().splitlines()]
        latest = max((stable(t) for t in tags if stable(t)), default=())
        if latest:
            updated["latest"] = ".".join(map(str, latest))
    except (OSError, subprocess.SubprocessError):
        pass
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["status", "follow-stable", "pin", "refresh"])
    args = parser.parse_args()
    path = settings()
    data = load(path)
    if args.action in ("follow-stable", "pin"):
        data = {"follow": args.action == "follow-stable"}
        save(path, data)
    elif args.action == "refresh":
        updated = refresh(data, lambda: subprocess.check_output(
            ["git", "ls-remote", "--tags", "--refs", "https://github.com/laikrodiz/lean-sdlc.git"],
            text=True, stderr=subprocess.DEVNULL, timeout=4, env=dict(os.environ, GIT_TERMINAL_PROMPT="0")), time.time())
        if updated != data:
            save(path, updated)
        data = updated
    print(json.dumps(data or {"follow": False}))


if __name__ == "__main__":
    main()
