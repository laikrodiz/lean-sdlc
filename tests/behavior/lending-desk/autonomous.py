"""Prepare a blind T3 worker bundle and grade a finished, reviewed macOS trial."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

import check_build

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PREFIX = ("Use $lean-sdlc to implement this locally. You may edit this project, run "
          "local checks, and use support agents. No additional Engineers. Do not commit or push.")
OBSERVATIONS = (
    "sol_high_executed", "no_operator_or_followup", "independent_task_split",
    "visible_intent_before_investigation", "visible_acceptance_before_edit", "lead_owned_gate_before_writes",
    "scout_before_implementation", "maintainer_after_behavior_settled",
    "independent_verifier_on_frozen_inputs", "lead_inspected_evidence_before_standalone_closure",
    "no_engineers_or_publication", "honest_handoff",
)


def seed(dest, variant):
    shutil.copytree(HERE / "starter", dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    if variant == "confirmation":
        # Same user-facing result; different IDs, stream order and replay count.
        (dest / "counter.csv").write_text("event,seq,tool,direction\nu7,70,T2,L\nu3,30,T1,L\nu7,70,T2,L\n")
        rows = [dict(receipt="u3", order=30, asset="T1", button="take"),
                dict(receipt="u5", order=50, asset="T1", button="back")]
        (dest / "kiosk.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
    elif variant != "baseline":
        raise ValueError("unknown fixture variant")


def pack(dest, variant):
    paths = subprocess.check_output(["git", "ls-files", "-z", "--", ".agents/plugins", "plugins/lean-sdlc"],
                                    cwd=REPO).decode().split("\0")
    prompt = PREFIX + "\n\n" + (HERE / "single-request.txt").read_text().strip() + "\n"
    digest = hashlib.sha256()
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "Friday cupboard"
        seed(project, variant)
        with zipfile.ZipFile(dest, "x", zipfile.ZIP_DEFLATED) as z:
            for name in sorted(filter(None, paths)):
                path = REPO / name
                if path.is_symlink() or not path.is_file():
                    raise ValueError(f"invalid plugin path: {name}")
                data = path.read_bytes()
                digest.update(name.encode() + b"\0" + hashlib.sha256(data).digest())
                z.writestr("marketplace/" + name, data)
            for path in sorted(project.rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(tmp))
            z.writestr("START.txt", prompt)
            z.writestr("CANDIDATE.sha256", digest.hexdigest() + "\n")
    return digest.hexdigest()


def trace_status(receipts):
    # Receipts come from the controller, never from the participant's self-report.
    if not receipts:
        return "unverified"
    if set(receipts) - set(OBSERVATIONS):
        raise ValueError("unknown observation")
    states = []
    for name in OBSERVATIONS:
        item = receipts.get(name, {})
        state = item.get("status", "unverified")
        if state not in ("pass", "fail", "unverified"):
            raise ValueError(f"invalid status: {name}")
        if state != "unverified" and not (isinstance(item.get("event_id"), str) and item["event_id"].strip()):
            raise ValueError(f"missing controller event ID: {name}")
        states.append(state)
    return "fail" if "fail" in states else "pass" if all(s == "pass" for s in states) else "unverified"


def ledger_status(build):
    ledger = build / "tasks.csv"
    if not ledger.is_file() or ledger.is_symlink():
        return False
    with ledger.open(newline="") as f:
        rows = list(csv.DictReader(f))
    product = [r for r in rows if r["Task ID"] != "TASK-000"]
    return (len(product) >= 2 and sum(r["Task ID"] == "TASK-000" for r in rows) == 1
            and len({r["Task ID"] for r in rows}) == len(rows)
            and len({r["Owner"] for r in product}) == 1
            and all(re.fullmatch(r"[0-9]{8}", r["Owner"]) for r in product)
            and all(r["Status"] == "Done" and r["Evidence"].strip() for r in rows))


def next_step(product, ledger, trace, variant, revision):
    if trace == "unverified":
        return "stop: incomplete workflow evidence"
    if not product or not ledger or trace == "fail":
        return "diagnose and revise" if revision < 3 else "stop: revision limit"
    return "run fresh confirmation" if variant == "baseline" else "confirmation passed"


def advance(history):
    """Replay immutable controller receipts. Never promote a lone confirmation."""
    variant, revision, candidate = "baseline", 1, None
    seen_runs, seen_candidates = set(), set()
    decision = "run baseline"
    for record in history:
        if decision.startswith("stop:") or decision == "confirmed":
            raise ValueError("receipt after terminal decision")
        key = record["run_id"]
        digest = record["candidate"]
        if not key or key in seen_runs or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("missing identity or reused run")
        if (record["variant"], record["revision"]) != (variant, revision):
            raise ValueError("unexpected variant or revision")
        if ((variant == "confirmation" and digest != candidate)
                or (variant == "baseline" and digest in seen_candidates)):
            raise ValueError("unexpected candidate change or unchanged revision")
        if record["trace"] not in ("pass", "fail", "unverified") or any(
            type(record[k]) is not bool for k in ("product", "ledger")
        ):
            raise ValueError("invalid grade")
        seen_runs.add(key)
        seen_candidates.add(digest)
        candidate = digest
        decision = next_step(record["product"], record["ledger"], record["trace"], variant, revision)
        if decision == "run fresh confirmation":
            variant = "confirmation"
        elif decision == "diagnose and revise":
            variant, revision = "baseline", revision + 1
        elif decision == "confirmation passed":
            decision = "confirmed"
    return {"action": decision, "variant": variant, "revision": revision}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="op", required=True)
    a = subs.add_parser("prepare")
    a.add_argument("archive", type=Path)
    b = subs.add_parser("grade")
    b.add_argument("build", type=Path)
    b.add_argument("--trace", type=Path, help="controller-only observations from this run")
    b.add_argument("--revision", type=int, choices=range(1, 4), default=1)
    b.add_argument("--run-id", required=True, help="actual host run ID")
    b.add_argument("--candidate", required=True, help="digest checked against the loaded plugin")
    b.add_argument("--report", type=Path, required=True, help="new controller-only JSON receipt")
    advance_cmd = subs.add_parser("advance", help="decide the next round from ordered receipts")
    advance_cmd.add_argument("reports", type=Path, nargs="*")
    for cmd in (a, b):
        cmd.add_argument("--variant", choices=("baseline", "confirmation"), default="baseline")
    args = p.parse_args()
    if args.op == "advance":
        print(json.dumps(advance([json.loads(path.read_text()) for path in args.reports])))
        return 0
    if args.op == "prepare":
        print("Candidate:", pack(args.archive, args.variant))
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        starter = Path(tmp) / "seed"
        seed(starter, args.variant)
        product = not check_build.check(args.build, starter)
    ledger = ledger_status(args.build)
    identity = dict(run_id=args.run_id, candidate=args.candidate, variant=args.variant, revision=args.revision)
    if not re.fullmatch("[0-9a-f]{64}", args.candidate) or not args.run_id:
        p.error("invalid trial identity")
    data = json.loads(args.trace.read_text()) if args.trace else {}
    if args.trace and any(data.get(k) != v for k, v in identity.items()):
        p.error("trace belongs to another trial")
    trace = trace_status(data.get("checks", {}))
    decision = next_step(product, ledger, trace, args.variant, args.revision)
    record = dict(**identity, product=product, ledger=ledger, trace=trace, next=decision)
    with args.report.open("x") as out:
        print(json.dumps(record), file=out)
    print(json.dumps(record))
    return 0 if product and ledger and trace == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
