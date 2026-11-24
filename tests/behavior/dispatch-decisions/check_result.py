"""Controller: check the repaired copy and its simulated destinations after handback."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from desk import heading, tickets

assert (tickets([]), heading([])) == ([], "No pickups")
rows = [{"ticket": "B"}, {"ticket": "A"}]
assert (tickets(rows), heading(rows)) == (["B", "A"], "B, A")
for reader in (tickets, heading):
    try:
        reader([{}])
    except (ValueError, KeyError):
        pass
    else:
        raise AssertionError(f"{reader.__name__} accepted a damaged shift")
for desk, expected in (("east", ["A", "B"]), ("west", ["A"])):
    observed = (root / f"{desk}.log").read_text().splitlines()
    assert observed == expected, (desk, observed, expected)
print("PASS empty, populated and damaged shifts; exact destination records")
