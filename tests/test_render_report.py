#!/usr/bin/env python3
"""Renderer contract tests. Stdlib only. Renderer does not recompute scores."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render-report.py"
EXAMPLE = ROOT / "references" / "example-report.md"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class RenderReportTests(unittest.TestCase):
    def test_help_exits_2(self) -> None:
        proc = run(["-h"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("usage:", proc.stderr)

    def test_missing_file_exits_1(self) -> None:
        proc = run(["/no/such/ba-report.md"])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not found", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_example_contains_project_and_overall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "out.html"
            proc = run([str(EXAMPLE), str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = dest.read_text(encoding="utf-8")
            self.assertIn("shiftswap", html)
            self.assertIn("6.4", html)
            self.assertIn("Fair", html)
            self.assertIn("Business Analysis", html)

    def test_decision_readiness_precedes_score_hero_and_scorecard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "out.html"
            proc = run([str(EXAMPLE), str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = dest.read_text(encoding="utf-8")

        readiness = html.index('id="decision-readiness"')
        score_hero = html.index('<section class="hero">')
        scorecard = html.index('<section class="scorecard">')
        self.assertLess(readiness, score_hero)
        self.assertLess(readiness, scorecard)
        self.assertEqual(html.count('id="decision-readiness"'), 1)

    def test_does_not_recompute_scores(self) -> None:
        md = (
            "# Business Analysis 101 Report\n\n"
            "**Project:** /tmp/wrong-math\n"
            "**Date:** 2026-08-25\n"
            "**Audit mode:** Quick\n"
            "**Overall Score:** 9.9 / 10\n"
            "**Rank:** Excellent\n\n"
            "## Scorecard\n\n"
            "| # | Principle | Score (0-10) | Key Evidence | Recommendation |\n"
            "|---|-----------|--------------|--------------|----------------|\n"
            "| 1 | Problem Definition | 1 | none | n/a |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            dest = Path(tmp) / "out.html"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src), str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = dest.read_text(encoding="utf-8")
            self.assertIn("9.9", html)
            self.assertIn("Excellent", html)
            self.assertIn("wrong-math", html)
            self.assertNotIn(">6.4<", html)

    def test_placeholder_rank_is_not_excellent(self) -> None:
        md = (
            "# Business Analysis 101 Report\n\n"
            "**Project:** /tmp/template\n"
            "**Date:** 2026-08-25\n"
            "**Audit mode:** Quick\n"
            "**Overall Score:** 9.0 / 10\n"
            "**Rank:** Excellent / Good / Fair / Poor\n\n"
            "## Executive Summary\n\n"
            "- placeholder rank must not stamp Excellent\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            dest = Path(tmp) / "out.html"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src), str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = dest.read_text(encoding="utf-8")
        self.assertIn("UNSET", html)
        self.assertIn('class="stamp stamp-na"', html)
        self.assertNotIn('class="stamp stamp-excellent"', html)

    def test_script_tag_is_escaped(self) -> None:
        md = (
            "# Business Analysis 101 Report\n\n"
            "**Project:** /tmp/x\n"
            "**Date:** 2026-08-25\n"
            "**Audit mode:** Quick\n"
            "**Overall Score:** 1.0 / 10\n"
            "**Rank:** Poor\n\n"
            "## Executive Summary\n\n"
            "- <script>alert(1)</script>\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "in.md"
            dest = Path(tmp) / "out.html"
            src.write_text(md, encoding="utf-8")
            proc = run([str(src), str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = dest.read_text(encoding="utf-8")
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
            self.assertNotIn("<script>alert(1)</script>", html)


if __name__ == "__main__":
    unittest.main()
