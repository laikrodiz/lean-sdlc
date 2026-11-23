"""Controller only. Run with -B and the participant's project root."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
from end_of_day import collected_total
from shift_file import open_shift, save_shift

OLD = [("P-28", True), ("P-02", False), ("P-41", True)]
NEW = [("N-18", False), ("N-42", True), ("N-01", True)]
FRIDAY = Path(__file__).parent / "starter/samples/friday.json"
failures = []


def check(name, operation, expected):
    try:
        actual = operation()
        if actual != expected:
            raise AssertionError(f"{actual!r} != {expected!r}")
    except Exception as err:
        failures.append(name)
        print(f"FAIL {name}: {err}")
    else:
        print("PASS", name)


with tempfile.TemporaryDirectory() as folder:
    legacy = Path(folder) / "legacy.json"
    legacy.write_bytes(FRIDAY.read_bytes())
    fresh = Path(folder) / "new.json"
    save_shift(fresh, NEW)
    check("new spelling and ticket order", lambda: [(r["ticket"], r["state"]) for r in json.loads(fresh.read_text())],
          [(key, "collected" if flag else "ready") for key, flag in NEW])
    check("new file opens", lambda: open_shift(fresh), NEW)
    check("new daily count", lambda: collected_total(fresh), 2)
    check("old file opens", lambda: open_shift(legacy), OLD)
    check("old daily count", lambda: collected_total(legacy), 2)
    check("opening leaves old bytes unchanged", legacy.read_bytes, FRIDAY.read_bytes())
    check("shipped example preserved", (ROOT / "samples/friday.json").read_bytes, FRIDAY.read_bytes())
if failures:
    raise SystemExit(1)
