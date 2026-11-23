import json


def collected_total(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    return sum(row["state"] == "picked_up" for row in rows)
