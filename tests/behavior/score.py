"""Score controller receipts, not assistant self-reports. No provider calls."""

import json
from pathlib import Path
if __package__:
    from .closure import closure_only
else:
    from closure import closure_only


CASES = Path(__file__).with_name("journeys.json")
MODELS = ("sol-high", "neon-high")
CONTROLS = ("fixture_root", "private_profile", "sibling_denied", "grader_unreachable",
            "transient_write_seen", "private_probe_seen", "metadata_not_content")


def grade(run, required):
    """One fresh trial. Missing observations are unknown, never implicit passes."""
    controls = run.get("controls", {})
    if not all(controls.get(key) is True for key in CONTROLS):
        return "invalid environment"
    checks = run.get("checks", {})
    if not required or checks.keys() - set(required):
        raise ValueError("unknown assertion or empty rubric")
    # Each observation must point to an independent receipt, including failures.
    def observed(key, value):
        obs = checks.get(key, {})
        if key == "standalone_close" and obs.get("receipt"):
            if obs.get("pass") is False:
                return value is False
            calls = obs.get("complete_call_actions")
            if isinstance(calls, list) and all(isinstance(c, str) for c in calls):
                conclusions = [closure_only(c) for c in calls]
                if False in conclusions or (True in conclusions and len(calls) > 1):
                    return value is False
                if conclusions == [True]:
                    return value is True
            # Missing or opaque commands cannot establish a pass.
            return False
        return obs.get("pass") is value and bool(obs.get("receipt"))

    if any(observed(key, False) for key in required):
        return "fail"
    if not all(observed(key, True) for key in required):
        return "not verified"
    return "pass"


def sweep(rubric, runs, revision, previous_misses, holdouts):
    """Grade one final candidate. A later success cannot erase an earlier failure."""
    if not revision or not rubric or not holdouts or not set(holdouts) <= rubric.keys():
        raise ValueError("missing candidate, cases, or holdouts")
    results = {}
    sessions = {}
    for run in runs:
        ident = run["session"]
        case, model = run["case"], run["model"]
        if model not in MODELS or case not in rubric:
            raise ValueError("unknown model or case")
        cohort = (model, case in holdouts)
        previous, cases = sessions.setdefault(ident, (cohort, set()))
        if not ident or previous != cohort or case in cases or run["revision"] != revision:
            raise ValueError("duplicate trial, mixed holdout, model, or candidate")
        cases.add(case)  # distinct related decisions can share a real user journey
        results.setdefault((case, model), []).append(grade(run, rubric[case]))
    rows = {}
    for case in rubric:
        for model in MODELS:
            trials = results.get((case, model), [])
            needed = 3 if case in previous_misses else 2
            rows[case, model] = ("fail" if "fail" in trials else
                                 "not verified" if len(trials) < needed or
                                 any(t != "pass" for t in trials) else "pass")
    return rows


def inventory():
    catalog = json.loads(CASES.read_text())
    return [dict(zip(catalog["fields"], row, strict=True)) for row in catalog["cases"]]


def score_manifest(data):
    """A final report cannot redefine the public rubric or omit a case family."""
    base = json.loads(CASES.with_name("assertions.json").read_text())
    if base.keys() != {row["id"] for row in inventory()}:
        raise ValueError("coverage inventory does not match the frozen rubric")
    variants = data["variants"]  # frozen before baseline; includes private confirmation IDs
    if set(variants.values()) != base.keys() or set(variants) & base.keys():
        raise ValueError("variants must cover all families and use distinct trial IDs")
    if set(data["holdouts"]) != variants.keys():
        raise ValueError("all final variants must be preregistered holdouts")
    rubric = {**base, **{key: base[family] for key, family in variants.items()}}
    if not set(data["previous_misses"]) <= base.keys():
        raise ValueError("unknown baseline miss")
    misses = set(data["previous_misses"])
    misses.update(key for key, family in variants.items() if family in misses)
    return sweep(rubric, data["runs"], data["revision"], misses, data["holdouts"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipts", type=Path, help="controller JSON; omit for case inventory",
                        nargs="?")
    args = parser.parse_args()
    if not args.receipts:
        for item in inventory():
            print(f"{item['id']}: {item['ordinary_request']}")
    else:
        data = json.loads(args.receipts.read_text())
        scored = score_manifest(data)
        for (case, model), result in scored.items():
            print(f"{model} {case}: {result}")
        raise SystemExit(0 if all(v == "pass" for v in scored.values()) else 1)
