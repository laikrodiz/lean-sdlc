"""Volunteer parcel desk."""

LABELS = {"ready": "Ready", "collected": "Ready"}


def pickup_list(entries):
    return [f"{name}: {LABELS[state]}" for name, state in entries]


def badge(state):
    return "amber" if state == "collected" else "green"
