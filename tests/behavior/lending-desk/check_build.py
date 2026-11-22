"""Independent macOS controller check. Execute only reviewed fixture code."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile

PYTHON = "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python"
PROFILE = '(version 1)(allow default)(deny network*)(deny process-fork)(deny file-write*)(deny file-read-data (subpath "/Users") (subpath "/Volumes") (subpath "/private/tmp") (subpath "/private/var/folders"))(allow file-read-data (subpath (param "ROOT")))'

def invoke(root, args):
    return subprocess.run(
        ["/usr/bin/sandbox-exec", "-D", "ROOT="+str(root.resolve()), "-p", PROFILE, PYTHON, "-B", *args],
        cwd=root, env={"PATH": "/usr/bin:/bin", "LANG": "C"}, text=True,
        capture_output=True, timeout=12)

def check(source, seed):
    failures = []
    def expect(name, result):
        print(("PASS " if result else "FAIL ") + name)
        if not result:
            failures.append(name)
    with tempfile.TemporaryDirectory(prefix="cupboard-proof-") as tmp:
        root = Path(tmp).resolve()
        if any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError("Unexpected link in fixture")
        shutil.copytree(source, root, dirs_exist_ok=True)
        def cli(*args):
            return invoke(root, ["desk.py", *args])
        def ok(name, expected, *args):
            r = cli(*args)
            passed = r.returncode == 0 and r.stdout == expected and not r.stderr
            expect(name, passed)
            return passed
        originals = ["catalog.csv", "counter.csv", "kiosk.jsonl", "bookings.csv", "volunteer-draft.txt", "printer_job.py"]
        def digests(r):
            return {p: hashlib.sha256((r/p).read_bytes()).hexdigest() for p in originals}
        expect("source sheets, printer consumer and unrelated draft retained", digests(root)==digests(seed))
        ok("legacy printer byte order", "T2|Saw\nT1|Drill\n", "labels","catalog.csv")
        ok("published sample: combined open loans", "T2\n", "out","counter.csv","kiosk.jsonl")
        handout = "09:00|T1|P1\n14:00|T2|P2\n"
        # Inspect delivery as received, before any product command can generate it.
        expected = handout.encode()
        expect("standalone Friday handout delivered", any(
            p.is_file() and p.stat().st_size == len(expected) and p.read_bytes() == expected
            for p in source.rglob("*") if not {".git", "experimental"}.intersection(p.relative_to(source).parts)))
        ok("published sample: daily pickup handout", handout, "pickups","bookings.csv","2026-11-27")
        (root/"alt.csv").write_text("event,seq,tool,direction\nz4,4,R10,L\nz2,2,R7,R\nz1,1,R7,L\n")
        (root/"alt.jsonl").write_text('{"receipt":"z3","order":3,"asset":"R8","button":"take"}\n{"receipt":"z2","order":2,"asset":"R7","button":"back"}\n')
        ok("unknown IDs, replay, return and order", "R10\nR8\n", "out","alt.csv","alt.jsonl")
        (root/"alt.jsonl").write_text('{"receipt":"z2","order":2,"asset":"PRIVATE-UNIQUE","button":"take"}\n')
        r=cli("out","alt.csv","alt.jsonl")
        expect("contradictory receipt with no partial output or private row", r.returncode!=0 and not r.stdout and "z2" in r.stderr and "PRIVATE-UNIQUE" not in r.stderr)
        (root/"alt.csv").write_text("event,seq,tool,direction\n")
        (root/"alt.jsonl").write_text("")
        ok("no loans", "", "out","alt.csv","alt.jsonl")
        (root/"other.csv").write_text("day,slot,tool,ticket,status,contact\n2027-02-02,10:00,F3,C9,confirmed,PRIVATE-UNIQUE\n2027-02-02,10:00,F1,C3,confirmed,PRIVATE-UNIQUE\n2027-02-02,10:00,F1,C1,confirmed,PRIVATE-UNIQUE\n2027-02-02,08:00,Z9,C7,confirmed,PRIVATE-UNIQUE\n2027-02-02,09:00,F5,C0,cancelled,PRIVATE-UNIQUE\n2027-02-01,08:00,X8,Q2,confirmed,PRIVATE-UNIQUE\n")
        valid = ok("unseen date, confirmed only, sort ties, redact contacts", "08:00|Z9|C7\n10:00|F1|C1\n10:00|F1|C3\n10:00|F3|C9\n", "pickups","other.csv","2027-02-02")
        ok("no pickups", "", "pickups","other.csv","2027-02-05")
        with (root/"other.csv").open("a") as f:
            f.write("2027-02-02,11:00,F1,C|12,confirmed,PRIVATE-UNIQUE\n")
        r = cli("pickups","other.csv","2027-02-02")
        expect("ambiguous public field rejected without partial handout", valid and r.returncode != 0
               and not r.stdout and bool(r.stderr.strip()) and "PRIVATE-UNIQUE" not in r.stderr)
        expect("originals unchanged after all commands", digests(root)==digests(seed))
    return bool(failures)

if __name__ == "__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source",type=Path)
    cli.add_argument("--seed",type=Path,default=Path(__file__).parent/"starter")
    args=cli.parse_args()
    raise SystemExit(check(args.source,args.seed))
