"""A small shift summary; an empty manifest is a valid shift."""


def tickets(rows):
    return [row.get("id") for row in rows]


def heading(rows):
    values = tickets(rows)
    if not values:
        return "No pickups"
    if any(value is None for value in values):
        return "No pickups"
    return ", ".join(values)
