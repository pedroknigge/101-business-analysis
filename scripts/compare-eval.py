#!/usr/bin/env python3
"""Compare a computed report JSON to eval expected.json or a baseline JSON.

Stdlib only. Does not re-audit the tree.

  compare-eval.py EXPECTED.json REPORT.json
      Floors / ceilings per principle (and optional overall). Exit 1 on misses.

  compare-eval.py --baseline OLD.json NEW.json
      Exit 1 if NEW has principle scores lower than OLD.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_report  # noqa: E402

USAGE = (
    "usage: compare-eval.py EXPECTED.json REPORT.json\n"
    "       compare-eval.py --baseline OLD.json NEW.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def score_map(payload: dict) -> dict[str, int]:
    raw = payload.get("scores") or {}
    out: dict[str, int] = {}
    if not isinstance(raw, dict):
        return out
    for name, value in raw.items():
        key = score_report.norm_principle(str(name))
        if key is None:
            continue
        try:
            out[key] = int(value)
        except (TypeError, ValueError):
            continue
    return out


def match_readiness_expect(field: str, expected, got) -> list[str]:
    """Assert one readiness field. str=exact; list=allowed set; dict may use startswith."""
    errors: list[str] = []
    if got is None or got == "":
        errors.append(f"decision_readiness.{field}: missing")
        return errors
    got_s = str(got)
    if isinstance(expected, list):
        allowed = [str(x) for x in expected]
        if got_s not in allowed:
            errors.append(
                f"decision_readiness.{field}: {got_s!r} not in {allowed}"
            )
        return errors
    if isinstance(expected, dict):
        if "startswith" in expected:
            prefix = str(expected["startswith"])
            if not got_s.startswith(prefix):
                errors.append(
                    f"decision_readiness.{field}: {got_s!r} does not start with {prefix!r}"
                )
            return errors
        if "in" in expected:
            allowed = [str(x) for x in expected["in"]]
            if got_s not in allowed:
                errors.append(
                    f"decision_readiness.{field}: {got_s!r} not in {allowed}"
                )
            return errors
        if "eq" in expected:
            want = str(expected["eq"])
            if got_s != want:
                errors.append(
                    f"decision_readiness.{field}: {got_s!r} != {want!r}"
                )
            return errors
        errors.append(f"decision_readiness.{field}: unsupported expect object")
        return errors
    want = str(expected)
    if got_s != want:
        errors.append(f"decision_readiness.{field}: {got_s!r} != {want!r}")
    return errors


def eval_against_expected(expected: dict, report: dict) -> list[str]:
    errors: list[str] = []
    scores = score_map(report)
    floors = expected.get("floors") or {}
    ceilings = expected.get("ceilings") or {}
    if not isinstance(floors, dict) or not isinstance(ceilings, dict):
        return ["floors/ceilings must be objects"]
    for name, floor in floors.items():
        key = score_report.norm_principle(str(name)) or str(name).lower()
        got = scores.get(key)
        try:
            want = int(floor)
        except (TypeError, ValueError):
            errors.append(f"{name}: floor not an integer")
            continue
        if got is None:
            errors.append(f"{name}: missing (floor {want})")
        elif got < want:
            errors.append(f"{name}: {got} below floor {want}")
    for name, ceiling in ceilings.items():
        key = score_report.norm_principle(str(name)) or str(name).lower()
        got = scores.get(key)
        try:
            want = int(ceiling)
        except (TypeError, ValueError):
            errors.append(f"{name}: ceiling not an integer")
            continue
        if got is None:
            errors.append(f"{name}: missing (ceiling {want})")
        elif got > want:
            errors.append(f"{name}: {got} above ceiling {want}")
    if "overall_floor" in expected:
        try:
            overall = float(report.get("overall"))
            if overall < float(expected["overall_floor"]):
                errors.append(
                    f"overall {overall} below floor {expected['overall_floor']}"
                )
        except (TypeError, ValueError):
            errors.append("overall missing for overall_floor")
    if "overall_ceiling" in expected:
        try:
            overall = float(report.get("overall"))
            if overall > float(expected["overall_ceiling"]):
                errors.append(
                    f"overall {overall} above ceiling {expected['overall_ceiling']}"
                )
        except (TypeError, ValueError):
            errors.append("overall missing for overall_ceiling")
    readiness_expect = expected.get("decision_readiness")
    if readiness_expect is not None:
        if not isinstance(readiness_expect, dict):
            errors.append("decision_readiness expect must be an object")
        else:
            got_ready = report.get("decision_readiness")
            if not isinstance(got_ready, dict):
                errors.append("decision_readiness missing from report")
            else:
                for field, want in readiness_expect.items():
                    errors.extend(
                        match_readiness_expect(str(field), want, got_ready.get(field))
                    )
    return errors


def baseline_regressions(old: dict, new: dict) -> list[str]:
    errors: list[str] = []
    old_scores = score_map(old)
    new_scores = score_map(new)
    for key in score_report.PRINCIPLE_KEYS:
        a = old_scores.get(key)
        b = new_scores.get(key)
        if a is None or b is None:
            continue
        if b < a:
            errors.append(f"new low score: {key} {a} -> {b}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] in {"-h", "--help"}:
        print(USAGE, file=sys.stderr)
        return 2
    baseline = len(argv) >= 2 and argv[1] == "--baseline"
    paths = argv[2:] if baseline else argv[1:]
    if len(paths) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    left = Path(paths[0])
    right = Path(paths[1])
    if not left.is_file() or not right.is_file():
        print("error: json not found", file=sys.stderr)
        return 1
    try:
        a = load(left)
        b = load(right)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = baseline_regressions(a, b) if baseline else eval_against_expected(a, b)
    if errors:
        print(f"{len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
