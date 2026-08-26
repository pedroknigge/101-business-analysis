#!/usr/bin/env python3
"""compare-eval.py contract tests. Stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARE = ROOT / "scripts" / "compare-eval.py"
STATED = ROOT / "evals" / "expected" / "stated-solution.json"
SOLID = ROOT / "evals" / "expected" / "solid-prd.json"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(COMPARE), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CompareEvalTests(unittest.TestCase):
    def test_help_exits_2(self) -> None:
        proc = run(["-h"])
        self.assertEqual(proc.returncode, 2)

    def test_stated_solution_ceiling_hit(self) -> None:
        report = {
            "scores": {
                "problem definition": 2,
                "stakeholder engagement": 2,
                "value & success criteria": 1,
                "elicitation completeness": 2,
                "solution options evaluation": 1,
                "scope discipline": 3,
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            proc = run([str(STATED), str(path)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_stated_solution_too_high_fails(self) -> None:
        report = {
            "scores": {
                "problem definition": 9,
                "stakeholder engagement": 2,
                "value & success criteria": 1,
                "elicitation completeness": 2,
                "solution options evaluation": 1,
                "scope discipline": 3,
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            proc = run([str(STATED), str(path)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("above ceiling", proc.stderr)

    def test_solid_prd_floor_hit(self) -> None:
        report = {
            "scores": {
                "problem definition": 8,
                "stakeholder engagement": 8,
                "value & success criteria": 8,
                "requirements quality": 8,
                "classification & prioritization": 8,
                "solution options evaluation": 8,
                "traceability": 7,
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            proc = run([str(SOLID), str(path)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_solid_prd_too_low_fails(self) -> None:
        report = {
            "scores": {
                "problem definition": 2,
                "stakeholder engagement": 8,
                "value & success criteria": 8,
                "requirements quality": 8,
                "classification & prioritization": 8,
                "solution options evaluation": 8,
                "traceability": 7,
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            proc = run([str(SOLID), str(path)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("below floor", proc.stderr)

    def test_baseline_regression(self) -> None:
        old = {"scores": {"problem definition": 7, "scope discipline": 6}}
        new = {"scores": {"problem definition": 4, "scope discipline": 6}}
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "old.json"
            b = Path(tmp) / "new.json"
            a.write_text(json.dumps(old), encoding="utf-8")
            b.write_text(json.dumps(new), encoding="utf-8")
            proc = run(["--baseline", str(a), str(b)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("new low score", proc.stderr)


if __name__ == "__main__":
    unittest.main()
