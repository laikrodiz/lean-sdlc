"""Controller-only preflight for a fresh, operator-mediated T3 Sol trial on macOS."""
import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


def bind(db, repo, helper, *, lead_owner, lead_helper):
    root = str(repo.resolve(strict=True))
    if helper.resolve(strict=True) != lead_helper.resolve(strict=True):
        raise ValueError("Controller helper differs from Lead startup helper")
    # macOS exposes the same temporary checkout under both /var and /private/var.
    alias = root[len("/private"):] if root.startswith("/private/var/") else root
    with sqlite3.connect(db.resolve(strict=True).as_uri() + "?mode=ro", uri=True) as conn:
        rows = conn.execute(
            "SELECT id, originator, model, reasoning_effort FROM threads "
            "WHERE cwd IN (?, ?) AND archived = 0 AND agent_role IS NULL", (root, alias)
        ).fetchall()
    if len(rows) != 1 or rows[0][1:] != ("T3 Code", "gpt-6.2-sol", "high"):
        raise ValueError("Expected exactly one active Sol High lead for this fresh project")
    # Use the same entry point as SessionStart. Do not set CODEX_SESSION_ID in the relay.
    event = json.dumps({"session_id": rows[0][0], "cwd": root})
    result = subprocess.run([sys.executable, "-B", str(helper)], input=event,
                            text=True, capture_output=True, check=True)
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    if f"Repository root: {root}. " not in context:
        raise ValueError("Startup resolved a different repository")
    if not context.startswith(f"Lean-SDLC Owner: {lead_owner}. "):
        raise ValueError("Controller lookup differs from Lead startup owner")
    return context


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("database", "fixture", "state_helper"):
        p.add_argument(name, type=Path)
    p.add_argument("--lead-owner", required=True)
    p.add_argument("--lead-helper", type=Path, required=True)
    a = p.parse_args()
    print(bind(a.database, a.fixture, a.state_helper,
               lead_owner=a.lead_owner, lead_helper=a.lead_helper))
