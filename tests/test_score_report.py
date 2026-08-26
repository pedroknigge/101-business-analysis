#!/usr/bin/env python3
"""score_report.py contract tests. Stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "score_report.py"
EXAMPLE = ROOT / "references" / "example-report.md"
sys.path.insert(0, str(ROOT / "scripts"))
import score_report  # noqa: E402

PRINCIPLES = score_report.CANONICAL


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def make_report(
    scores: list[int],
    overall: str,
    rank: str,
    *,
    skip: int | None = None,
    evidence: bool = True,
) -> str:
    rows = []
    for i, (name, score) in enumerate(zip(PRINCIPLES, scores), 1):
        if skip is not None and i == skip:
            continue
        ev = f"docs/file{i}.md" if evidence else ""
        rows.append(f"| {i} | {name} | {score} | {ev} | fix {i} |")
    table = "\n".join(rows)
    coverage = "**Evidence coverage:** 100%\n" if evidence and skip is None else ""
    return (
        "# Business Analysis 101 Report\n\n"
        "**Project:** /tmp/demo\n"
        "**Date:** 2026-08-25\n"
        "**Audit mode:** Deep\n"
        "**Subject type:** brief\n"
        "**Cadence:** unknown\n"
        f"**Overall Score:** {overall} / 10\n"
        f"**Rank:** {rank}\n"
        f"{coverage}\n"
        "## Scorecard\n\n"
        "| # | Principle | Score (0-10) | Key Evidence | Recommendation |\n"
        "|---|-----------|--------------|--------------|----------------|\n"
        f"{table}\n"
    )


class ScoreReportTests(unittest.TestCase):
    def test_help_exits_2(self) -> None:
        proc = run(["-h"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("usage:", proc.stderr)

    def test_missing_file_exits_1(self) -> None:
        proc = run(["/no/such/ba-report.md"])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not found", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_example_report_passes(self) -> None:
        proc = run([str(EXAMPLE)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("example-report.md", proc.stdout)

    def test_example_json_overall_and_rank(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            proc = run([str(EXAMPLE), "--json", str(out)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "ba-report/0.1")
            self.assertEqual(payload["overall"], 6.4)
            self.assertEqual(payload["rank"], "Fair")
            self.assertEqual(len(payload["scores"]), 15)
            self.assertEqual(payload["missing"], [])
            self.assertEqual(payload["subject_type"], "repo")

    def test_known_fifteen_scores(self) -> None:
        scores = [8, 7, 5, 6, 6, 8, 7, 4, 5, 8, 6, 5, 8, 5, 8]
        md = make_report(scores, "6.4", "Fair")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_missing_principle_nonzero(self) -> None:
        scores = [7] * 15
        md = make_report(scores, "7.0", "Good", skip=4)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing", proc.stderr.lower())

    def test_wrong_overall_fails(self) -> None:
        md = make_report([7] * 15, "9.9", "Good")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Overall Score", proc.stderr)

    def test_rank_edge_excellent_8_5(self) -> None:
        scores = [9] * 7 + [8] * 8
        md = make_report(scores, "8.5", "Excellent")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rank_edge_good_7_0(self) -> None:
        md = make_report([7] * 15, "7.0", "Good")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rank_edge_fair_5_5(self) -> None:
        scores = [6] * 7 + [5] * 8
        md = make_report(scores, "5.5", "Fair")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rank_edge_poor_5_4(self) -> None:
        scores = [6] * 6 + [5] * 9
        md = make_report(scores, "5.4", "Poor")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_json_only_roundtrip(self) -> None:
        payload = {
            "scores": {name.lower(): 7 for name in PRINCIPLES},
            "overall": 7.0,
            "rank": "Good",
        }
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.json"
            src.write_text(json.dumps(payload), encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_template_rank_placeholder_fails(self) -> None:
        md = make_report([9] * 15, "9.0", "Excellent / Good / Fair / Poor")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not a rank token", proc.stderr)

    def test_json_without_flag_does_not_rewrite(self) -> None:
        payload = {
            "scores": {name.lower(): 7 for name in PRINCIPLES},
            "overall": 7.0,
            "rank": "Good",
            "extra": "keep-me",
        }
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.json"
            src.write_text(json.dumps(payload), encoding="utf-8")
            proc = run([str(src)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            kept = json.loads(src.read_text(encoding="utf-8"))
        self.assertEqual(kept["extra"], "keep-me")

    def test_json_flag_without_input_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = run(["--json", str(Path(tmp) / "out.json")])
        self.assertEqual(proc.returncode, 2)

    def test_missing_principle_null_overall(self) -> None:
        md = make_report([10] * 15, "10.0", "Excellent", skip=4)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            out = Path(tmp) / "out.json"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src), "--json", str(out)])
            self.assertEqual(proc.returncode, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
        self.assertIsNone(payload["overall"])
        self.assertIsNone(payload["rank"])
        self.assertTrue(payload["missing"])

    def test_float_score_cell_fails(self) -> None:
        md = make_report([7] * 15, "7.0", "Good").replace(
            "| 1 | Problem Definition | 7 |",
            "| 1 | Problem Definition | 6.5 |",
        )
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not an integer", proc.stderr)

    def test_json_float_score_rejected(self) -> None:
        scores = {name.lower(): 7 for name in PRINCIPLES}
        scores["problem definition"] = 7.9  # type: ignore[assignment]
        payload = {"scores": scores, "overall": 7.0, "rank": "Good"}
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.json"
            src.write_text(json.dumps(payload), encoding="utf-8")
            proc = run([str(src)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not an integer", proc.stderr)


class ScoreReportUnitTests(unittest.TestCase):
    def test_norm_empty_and_alias(self) -> None:
        self.assertIsNone(score_report.norm_principle(""))
        self.assertIsNone(score_report.norm_principle("   "))
        self.assertEqual(score_report.norm_principle("Problem"), "problem definition")
        self.assertEqual(score_report.norm_principle("MoSCoW"), "classification & prioritization")
        self.assertEqual(score_report.norm_principle("Stakeholders"), "stakeholder engagement")

    def test_parse_int_rejects_float_and_slash(self) -> None:
        self.assertIsNone(score_report.parse_int_score("6.5"))
        self.assertIsNone(score_report.parse_int_score("8/10"))
        self.assertEqual(score_report.parse_int_score("8"), 8)
        self.assertEqual(score_report.parse_int_score("10"), 10)

    def test_parse_rank_exact_token(self) -> None:
        self.assertEqual(score_report.parse_rank("Excellent"), "Excellent")
        self.assertEqual(score_report.parse_rank("Excellent (world-class)"), "Excellent")
        self.assertEqual(score_report.parse_rank("Excellent / Good / Fair / Poor"), "")
        self.assertEqual(score_report.parse_rank("Fair"), "Fair")

    def test_overall_none_when_short(self) -> None:
        scores = {k: 10 for k in score_report.PRINCIPLE_KEYS[:-1]}
        self.assertIsNone(score_report.overall_from_scores(scores))

    def test_scorer_does_not_load_renderer(self) -> None:
        src = Path(score_report.__file__).read_text(encoding="utf-8")
        self.assertNotIn("render-report", src)
        self.assertNotIn("load_renderer", src)
        self.assertNotIn("importlib", src)


if __name__ == "__main__":
    unittest.main()
