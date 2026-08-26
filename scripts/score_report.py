#!/usr/bin/env python3
"""Validate Decision Readiness, overall, and rank in BA audit reports.

Stdlib only. The agent classifies evidence and assigns 0–10 per principle.
This script does not invent principle scores. Formula and rank bands live in
``references/scoring.md``.

Exit 0 if readiness, arithmetic, and rank are valid; exit 1 otherwise; exit 2 on usage.
"""

from __future__ import annotations

import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from report_parse import header_index, parse_meta, parse_rank, parse_tables  # noqa: E402

SCHEMA = "ba-report/0.1"

CANONICAL = [
    "Problem Definition",
    "Stakeholder Engagement",
    "Value & Success Criteria",
    "Constraints & Assumptions",
    "Elicitation Completeness",
    "Requirements Quality",
    "Classification & Prioritization",
    "Solution Options Evaluation",
    "Traceability",
    "Process Modeling",
    "Data & Decision Modeling",
    "Scope Discipline",
    "Collaboration & Communication",
    "Solution Evaluation",
    "Requirements Life Cycle",
]

PRINCIPLE_KEYS = [name.lower() for name in CANONICAL]

ALIASES = {
    "problem definition": "problem definition",
    "problem": "problem definition",
    "need / problem": "problem definition",
    "need/problem": "problem definition",
    "root cause": "problem definition",
    "stakeholder engagement": "stakeholder engagement",
    "stakeholders": "stakeholder engagement",
    "stakeholder identification": "stakeholder engagement",
    "stakeholder analysis": "stakeholder engagement",
    "value & success criteria": "value & success criteria",
    "value and success criteria": "value & success criteria",
    "value": "value & success criteria",
    "success criteria": "value & success criteria",
    "constraints & assumptions": "constraints & assumptions",
    "constraints and assumptions": "constraints & assumptions",
    "constraints": "constraints & assumptions",
    "assumptions": "constraints & assumptions",
    "elicitation completeness": "elicitation completeness",
    "elicitation": "elicitation completeness",
    "requirements quality": "requirements quality",
    "requirement quality": "requirements quality",
    "classification & prioritization": "classification & prioritization",
    "classification and prioritization": "classification & prioritization",
    "prioritization": "classification & prioritization",
    "moscow": "classification & prioritization",
    "solution options evaluation": "solution options evaluation",
    "options evaluation": "solution options evaluation",
    "solution options": "solution options evaluation",
    "traceability": "traceability",
    "requirements traceability": "traceability",
    "process modeling": "process modeling",
    "process": "process modeling",
    "as-is / to-be": "process modeling",
    "data & decision modeling": "data & decision modeling",
    "data and decision modeling": "data & decision modeling",
    "data modeling": "data & decision modeling",
    "decision modeling": "data & decision modeling",
    "scope discipline": "scope discipline",
    "scope": "scope discipline",
    "gold-plating": "scope discipline",
    "collaboration & communication": "collaboration & communication",
    "collaboration and communication": "collaboration & communication",
    "communication": "collaboration & communication",
    "solution evaluation": "solution evaluation",
    "outcome validation": "solution evaluation",
    "requirements life cycle": "requirements life cycle",
    "requirements lifecycle": "requirements life cycle",
    "life cycle management": "requirements life cycle",
}

RANKS = ("Excellent", "Good", "Fair", "Poor")

READINESS_ROWS = {
    "right problem": "Right problem",
    "best available option": "Best available option",
    "measurable value": "Measurable value",
}
RIGHT_PROBLEM_CONCLUSIONS = ("Validated", "Provisional", "Unknown")
MEASURABLE_VALUE_CONCLUSIONS = (
    "Realized",
    "Measurement-ready",
    "Measurable with gaps",
    "Not measurable",
    "Unknown",
)
DECISION_READINESS_HEADING_RE = re.compile(
    r"^#{2,6}\s+(?:\d+\.\s+)?Decision Readiness(?:\s+\(.*\))?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

USAGE = "usage: score_report.py INPUT.md|INPUT.json [--json OUT.json]"
SCORE_INT_RE = re.compile(r"0*(?:10|[0-9])$")


def package_version() -> str:
    path = ROOT / "VERSION"
    try:
        return path.read_text(encoding="utf-8").strip() or "0.2.0"
    except OSError:
        return "0.2.0"


VERSION = package_version()


def round_half_up(value: Decimal, ndigits: int = 1) -> float:
    if ndigits == 0:
        quant = Decimal("1")
    else:
        quant = Decimal("0." + "0" * (ndigits - 1) + "1")
    return float(value.quantize(quant, rounding=ROUND_HALF_UP))


def fold(name: str) -> str:
    text = (name or "").strip().lower()
    text = re.sub(r"^\d+[\.\):]\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def norm_principle(name: str) -> str | None:
    text = fold(name)
    if not text:
        return None
    if text in ALIASES:
        return ALIASES[text]
    if text in PRINCIPLE_KEYS:
        return text
    stripped = re.sub(r"\s*\(.*\)$", "", text).strip()
    if stripped and stripped in ALIASES:
        return ALIASES[stripped]
    if stripped and stripped in PRINCIPLE_KEYS:
        return stripped
    return None


def overall_from_scores(scores: dict[str, int]) -> float | None:
    if any(k not in scores for k in PRINCIPLE_KEYS):
        return None
    total = sum(Decimal(scores[k]) for k in PRINCIPLE_KEYS)
    return round_half_up(total / Decimal(15), 1)


def rank_for(overall: float) -> str:
    if overall >= 8.5:
        return "Excellent"
    if overall >= 7.0:
        return "Good"
    if overall >= 5.5:
        return "Fair"
    return "Poor"


def parse_overall(raw: str) -> float | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        return float(text.split("/")[0].strip())
    except ValueError:
        return None


def parse_coverage(raw: str) -> int | None:
    text = (raw or "").strip().rstrip("%")
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def parse_int_score(raw: str) -> int | None:
    text = (raw or "").strip()
    if not text or text in {"—", "-", "n/a", "N/A"}:
        return None
    if not SCORE_INT_RE.fullmatch(text):
        return None
    n = int(text)
    if 0 <= n <= 10:
        return n
    return None


def scorecard_table(tables: dict[str, list[list[str]]]) -> list[list[str]] | None:
    for key, rows in tables.items():
        if "scorecard" in key:
            return rows
    for rows in tables.values():
        if rows and header_index(rows[0], "principle") is not None:
            return rows
    return None


def validate_decision_readiness(md: str, tables: dict[str, list[list[str]]]) -> list[str]:
    if not DECISION_READINESS_HEADING_RE.search(md):
        return ["Decision Readiness section missing"]

    table = tables.get("decision readiness")
    if table is None:
        return ["Decision Readiness table missing"]

    header = table[0]
    i_outcome = header_index(header, "outcome")
    i_conclusion = header_index(header, "conclusion")
    if i_outcome is None or i_conclusion is None:
        return ["Decision Readiness table needs Outcome and Conclusion columns"]

    conclusions: dict[str, str] = {}
    for row in table[1:]:
        if i_outcome >= len(row):
            continue
        outcome = fold(row[i_outcome])
        if outcome not in READINESS_ROWS:
            continue
        conclusions[outcome] = row[i_conclusion].strip() if i_conclusion < len(row) else ""

    errors: list[str] = []
    for outcome, label in READINESS_ROWS.items():
        if outcome not in conclusions:
            errors.append(f"Decision Readiness row missing: {label}")

    right_problem = conclusions.get("right problem")
    if right_problem is not None and right_problem not in RIGHT_PROBLEM_CONCLUSIONS:
        allowed = ", ".join(RIGHT_PROBLEM_CONCLUSIONS)
        errors.append(
            f"Decision Readiness conclusion for Right problem must be one of: {allowed} "
            f"(got {right_problem!r})"
        )

    best_option = conclusions.get("best available option")
    if best_option is not None:
        recommendation = best_option.removeprefix("Recommended:").strip()
        template_placeholder = recommendation in {"…", "...", "… / Not decision-ready"}
        if best_option != "Not decision-ready" and (
            not best_option.startswith("Recommended:")
            or not recommendation
            or template_placeholder
        ):
            errors.append(
                "Decision Readiness conclusion for Best available option must be "
                "'Not decision-ready' or 'Recommended: <option>' "
                f"(got {best_option!r})"
            )

    measurable_value = conclusions.get("measurable value")
    if measurable_value is not None and measurable_value not in MEASURABLE_VALUE_CONCLUSIONS:
        allowed = ", ".join(MEASURABLE_VALUE_CONCLUSIONS)
        errors.append(
            f"Decision Readiness conclusion for Measurable value must be one of: {allowed} "
            f"(got {measurable_value!r})"
        )

    return errors


def scores_from_table(table: list[list[str]] | None) -> tuple[dict[str, int], dict[str, str], list[str]]:
    scores: dict[str, int] = {}
    evidence: dict[str, str] = {}
    errors: list[str] = []
    if not table or len(table) < 2:
        return scores, evidence, errors
    header = table[0]
    i_prin = header_index(header, "principle")
    i_score = header_index(header, "score (0-10)", "score")
    i_ev = header_index(header, "key evidence", "evidence")
    if i_prin is None or i_score is None:
        errors.append("Scorecard table needs Principle and Score columns")
        return scores, evidence, errors
    for row in table[1:]:
        if i_prin >= len(row):
            continue
        key = norm_principle(row[i_prin])
        if key is None:
            continue
        raw = row[i_score] if i_score < len(row) else ""
        score = parse_int_score(raw)
        if score is None:
            errors.append(f"{key}: score is not an integer 0–10 ({raw!r})")
            continue
        scores[key] = score
        if i_ev is not None and i_ev < len(row):
            evidence[key] = row[i_ev].strip()
    return scores, evidence, errors


def scores_from_json(payload: dict) -> tuple[dict[str, int], list[str]]:
    raw = payload.get("scores") or {}
    scores: dict[str, int] = {}
    errors: list[str] = []
    if not isinstance(raw, dict):
        return scores, ["scores must be an object"]
    for name, value in raw.items():
        key = norm_principle(str(name))
        if key is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int):
            errors.append(f"{key}: score is not an integer ({value!r})")
            continue
        n = value
        if n < 0 or n > 10:
            errors.append(f"{key}: score {n} out of 0–10")
            continue
        scores[key] = n
    return scores, errors


def coverage_pct(evidence: dict[str, str], scores: dict[str, int]) -> int | None:
    if not scores:
        return None
    covered = sum(1 for k in PRINCIPLE_KEYS if (evidence.get(k) or "").strip())
    return int(round_half_up(Decimal(covered) * Decimal(100) / Decimal(15), 0))


def missing_principles(scores: dict[str, int]) -> list[str]:
    return [name for name, key in zip(CANONICAL, PRINCIPLE_KEYS) if key not in scores]


def validate_scores(
    scores: dict[str, int],
    *,
    reported_overall: float | None,
    reported_rank: str,
    reported_coverage: int | None,
    evidence: dict[str, str] | None = None,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    missing = missing_principles(scores)
    if missing:
        errors.append("missing principles: " + ", ".join(missing))
        overall = None
        rank = None
    else:
        overall = overall_from_scores(scores)
        rank = rank_for(overall) if overall is not None else None
        if overall is None:
            errors.append("overall: no principle scores")
        elif reported_overall is not None and abs(reported_overall - overall) > 0.001:
            errors.append(f"Overall Score {reported_overall} != computed {overall}")
        elif reported_overall is None:
            errors.append("Overall Score header missing")
        got_rank = parse_rank(reported_rank)
        if overall is not None:
            if not (reported_rank or "").strip():
                errors.append("Rank header missing")
            elif not got_rank:
                errors.append(f"Rank {reported_rank!r} is not a rank token")
            elif got_rank != rank:
                errors.append(f"Rank {got_rank!r} != computed {rank!r}")
    expect_cov = coverage_pct(evidence, scores) if evidence is not None else None
    if (
        evidence is not None
        and reported_coverage is not None
        and expect_cov is not None
        and reported_coverage != expect_cov
    ):
        errors.append(f"Evidence coverage {reported_coverage}% != computed {expect_cov}%")
    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        "overall": overall,
        "rank": rank,
        "evidence_coverage": reported_coverage if reported_coverage is not None else expect_cov,
        "scores": {k: scores[k] for k in PRINCIPLE_KEYS if k in scores},
        "missing": missing,
        "errors": errors,
    }
    return errors, payload


def validate_markdown(md: str) -> tuple[list[str], dict]:
    meta = parse_meta(md)
    tables = parse_tables(md)
    readiness_errors = validate_decision_readiness(md, tables)
    table = scorecard_table(tables)
    scores, evidence, parse_errors = scores_from_table(table)
    if table is None:
        parse_errors.append("Scorecard table missing")
    errors, payload = validate_scores(
        scores,
        reported_overall=parse_overall(meta.get("Overall Score", "")),
        reported_rank=meta.get("Rank", ""),
        reported_coverage=parse_coverage(meta.get("Evidence coverage", "")),
        evidence=evidence,
    )
    payload["project"] = meta.get("Project", "")
    payload["date"] = meta.get("Date", "")
    payload["audit_mode"] = meta.get("Audit mode", "")
    payload["subject_type"] = meta.get("Subject type", "")
    payload["cadence"] = meta.get("Cadence", "")
    payload["errors"] = readiness_errors + parse_errors + errors
    return payload["errors"], payload


def validate_json_payload(data: dict) -> tuple[list[str], dict]:
    scores, parse_errors = scores_from_json(data)
    overall_raw = data.get("overall")
    reported_overall: float | None
    if overall_raw is None or overall_raw == "":
        reported_overall = None
    else:
        try:
            reported_overall = float(overall_raw)
        except (TypeError, ValueError):
            reported_overall = None
            parse_errors.append(f"overall is not a number: {overall_raw!r}")
    errors, payload = validate_scores(
        scores,
        reported_overall=reported_overall,
        reported_rank=str(data.get("rank") or ""),
        reported_coverage=data.get("evidence_coverage")
        if isinstance(data.get("evidence_coverage"), int)
        else parse_coverage(str(data.get("evidence_coverage") or "")),
        evidence=None,
    )
    payload["project"] = data.get("project", "")
    payload["date"] = data.get("date", "")
    payload["audit_mode"] = data.get("audit_mode", "")
    payload["subject_type"] = data.get("subject_type", "")
    payload["cadence"] = data.get("cadence", "")
    payload["errors"] = parse_errors + errors
    return payload["errors"], payload


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(USAGE, file=sys.stderr)
        return 2
    src: Path | None = None
    json_out: Path | None = None
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--json" and i + 1 < len(args):
            json_out = Path(args[i + 1])
            i += 2
        elif args[i].startswith("-"):
            print(USAGE, file=sys.stderr)
            return 2
        else:
            src = Path(args[i])
            i += 1
    if src is None:
        print(USAGE, file=sys.stderr)
        return 2
    if not src.is_file():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 1
    try:
        text = src.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if src.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if not isinstance(data, dict):
            print("error: json root must be an object", file=sys.stderr)
            return 1
        errors, payload = validate_json_payload(data)
    else:
        errors, payload = validate_markdown(text)
    dest = json_out
    if dest is not None:
        dest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if errors:
        print(f"{src}: {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print(str(src))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
