#!/usr/bin/env python3
"""Packaging contract: portable paths, version, one home per fact."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_version_file(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "0.3.0")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "0.3.0"', skill)

    def test_skill_scanner_path_is_portable(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("~/.claude/skills/101-business-analysis", skill)
        self.assertIn("<this-skill>/scripts/artifact_scanner.py", skill)
        self.assertIn("~/.agents/skills/", skill)

    def test_rank_bands_live_in_scoring_only(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        scoring = (ROOT / "references" / "scoring.md").read_text(encoding="utf-8")
        self.assertNotIn("8.5", skill)
        self.assertNotIn("5.4", skill)
        self.assertIn("8.5", scoring)
        self.assertIn("simple average", scoring.lower())

    def test_language_policy(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Language", skill)
        self.assertIn("This skill body is English", skill)
        self.assertIn("section titles", skill.lower())
        self.assertNotIn("profundiza en principio", skill)

    def test_fifteen_canonical_names_in_scoring(self) -> None:
        scoring = (ROOT / "references" / "scoring.md").read_text(encoding="utf-8")
        self.assertIn("Problem Definition", scoring)
        self.assertIn("Requirements Life Cycle", scoring)
        self.assertIn("Solution Options Evaluation", scoring)

    def test_report_skeleton_lives_in_template_only(self) -> None:
        """One home for the audit report skeleton: references/report_template.md."""
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        template = (ROOT / "references" / "report_template.md").read_text(
            encoding="utf-8"
        )
        skeleton_fence = "```markdown\n# Business Analysis 101 Report"
        self.assertNotIn(skeleton_fence, skill)
        self.assertIn(skeleton_fence, template)
        # Consecutive template section headers = pasted skeleton fingerprint
        pasted_headers = (
            "## Decision Readiness\n"
            "| Outcome | Conclusion | Evidence | Critical unknown / next evidence |\n"
        )
        self.assertNotIn(pasted_headers, skill)
        self.assertIn("references/report_template.md", skill)


if __name__ == "__main__":
    unittest.main()
