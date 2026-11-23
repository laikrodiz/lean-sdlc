import json

PICKED_UP = "picked_up"


def save_shift(path, parcels):
    rows = [{"ticket": ticket, "state": PICKED_UP if collected else "ready"}
            for ticket, collected in parcels]
    path.write_text(json.dumps(rows) + "\n", encoding="utf-8")


def open_shift(path):
    flags = {"ready": False, PICKED_UP: True}
    return [(row["ticket"], flags[row["state"]])
            for row in json.loads(path.read_text(encoding="utf-8"))]
