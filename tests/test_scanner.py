#!/usr/bin/env python3
"""artifact_scanner.py contract tests. Stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "artifact_scanner.py"
BRIEF = ROOT / "tests" / "fixtures" / "tiny-brief" / "request.md"
SOLID = ROOT / "evals" / "fixtures" / "solid-prd"
STATED = ROOT / "evals" / "fixtures" / "stated-solution"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class ScannerTests(unittest.TestCase):
    def test_help_exits_0_or_2(self) -> None:
        proc = run(["-h"])
        self.assertIn(proc.returncode, {0, 2})

    def test_missing_path_exits_1(self) -> None:
        proc = run(["/no/such/ba-subject", "--json"])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not found", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_json_mode_keys_on_brief(self) -> None:
        proc = run([str(BRIEF), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        summary = data["summary"]
        self.assertIn("subject_type", summary)
        self.assertIn("keyword_hits", summary)
        self.assertIn("gaps", summary)
        hits = summary["keyword_hits"]
        self.assertGreater(hits.get("requirement", 0) + hits.get("stakeholder", 0), 0)

    def test_text_flag(self) -> None:
        proc = run(["--text", str(BRIEF), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertTrue(data["summary"]["keyword_hits"])

    def test_solid_prd_has_options_and_few_gaps(self) -> None:
        proc = run([str(SOLID), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        hits = data["summary"]["keyword_hits"]
        self.assertGreater(hits.get("options", 0), 0)
        self.assertGreater(hits.get("stakeholder", 0), 0)
        self.assertGreater(hits.get("moscow", 0) + hits.get("requirement", 0), 0)
        gaps = data["summary"]["gaps"]
        self.assertNotIn("No options / alternatives signal", gaps)

    def test_stated_solution_flags_options_gap(self) -> None:
        proc = run([str(STATED), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        gaps = data["summary"]["gaps"]
        self.assertIn("No options / alternatives signal", gaps)

    def test_planted_evals_are_skipped_when_scanning_skill_root(self) -> None:
        proc = run([str(ROOT), "--json", "--max-depth", "4"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        blob = " ".join(data.get("docs_files") or [])
        self.assertNotIn("evals/fixtures", blob)
        self.assertNotIn("evals/fixtures".replace("/", "\\"), blob)
        self.assertNotIn("tests/fixtures", blob)

    def test_human_mode_mentions_subject(self) -> None:
        proc = run([str(BRIEF)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Subject type", proc.stdout)


if __name__ == "__main__":
    unittest.main()
