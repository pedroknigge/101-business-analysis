#!/usr/bin/env python3
"""Scan a path or a brief for Business Analysis artifacts and keyword signals.

Stdlib only. Does not score. Agents must not invent this output.

Usage:
  python3 artifact_scanner.py <path> [--json] [--max-depth 6] [--max-files 4000]
  python3 artifact_scanner.py --text FILE.md [--json]
  python3 artifact_scanner.py --stdin [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
    "target",
    "build",
    "dist",
    ".next",
    "out",
    "coverage",
    ".idea",
    ".vscode",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "htmlcov",
    "vendor",
    "bin",
    "obj",
    "tmp",
    "temp",
    "logs",
    "log",
    ".turbo",
    ".cache",
    "cache",
}

PLANTED_DIR_PREFIXES = (
    ("evals",),
    ("tests", "fixtures"),
)

DOC_EXTS = {".md", ".rst", ".txt", ".adoc", ".markdown"}
MODEL_EXTS = {".bpmn", ".xml", ".drawio", ".mmd", ".mermaid"}
DATA_EXTS = {".sql", ".dbml", ".prisma"}
STORY_EXTS = {".feature", ".md"}

ARTIFACT_NAME_RE = {
    "prd": re.compile(r"\b(prd|product[-_ ]?requirements?)\b", re.I),
    "brd": re.compile(r"\b(brd|business[-_ ]?requirements?)\b", re.I),
    "srs": re.compile(r"\b(srs|software[-_ ]?requirements?)\b", re.I),
    "user_stories": re.compile(r"\b(user[-_ ]?stor(y|ies)|backlog)\b", re.I),
    "acceptance": re.compile(r"\b(acceptance[-_ ]?criteria|gherkin)\b", re.I),
    "stakeholders": re.compile(r"\b(stakeholder|raci|persona)\b", re.I),
    "process": re.compile(r"\b(bpmn|process[-_ ]?(map|model)|swimlane|value[-_ ]?stream)\b", re.I),
    "decisions": re.compile(r"\b(adr|decision[-_ ]?log|architecture[-_ ]?decision)\b", re.I),
    "okrs": re.compile(r"\b(okr|kpi|success[-_ ]?metric|north[-_ ]?star)\b", re.I),
    "risks": re.compile(r"\b(risk[-_ ]?register|raid)\b", re.I),
    "glossary": re.compile(r"\b(glossary|ubiquitous[-_ ]?language|data[-_ ]?dictionary)\b", re.I),
    "use_cases": re.compile(r"\b(use[-_ ]?case)\b", re.I),
    "assumptions": re.compile(r"\b(assumption[-_ ]?log)\b", re.I),
    "traceability": re.compile(r"\b(traceabilit(y|ies)|rtm)\b", re.I),
}

SIGNAL_PATTERNS = {
    "problem": re.compile(r"\b(problems?|root cause|opportunit(?:y|ies)|pain points?|as-is)\b", re.I),
    "stakeholder": re.compile(r"\b(stakeholders?|personas?|raci|sponsor|end users?)\b", re.I),
    "value": re.compile(r"\b(kpis?|okrs?|success|outcomes?|north[-_ ]?star|measurable)\b", re.I),
    "constraint": re.compile(r"\b(constraints?|budget|deadline|regulation|compliance|assumptions?)\b", re.I),
    "requirement": re.compile(r"\b(must|shall|requirements?|user stor(?:y|ies)|acceptance criteria)\b", re.I),
    "story_template": re.compile(r"\bas a\b.+\bi (want|need)\b.+\bso that\b", re.I | re.S),
    "gherkin": re.compile(r"\bgiven\b.+\bwhen\b.+\bthen\b", re.I | re.S),
    "moscow": re.compile(r"\b(must have|should have|could have|won'?t have|moscow|kano)\b", re.I),
    "options": re.compile(r"\b(option|alternative|trade-?off|vs\.|compared to)\b", re.I),
    "trace": re.compile(r"\b(traces? to|traceabilit|covers requirement)\b", re.I),
    "process": re.compile(r"\b(as-is|to-be|bpmn|swimlane|handoff|value stream)\b", re.I),
    "data": re.compile(r"\b(entity|data model|erd|decision table|domain object)\b", re.I),
    "scope": re.compile(r"\b(out of scope|non-goal|won't|gold[- ]?plat)\b", re.I),
    "validation": re.compile(r"\b(uat|outcome|measure(d|ment)|did it work|post[-_ ]?release)\b", re.I),
}

READ_CAP = 200_000


def is_planted_rel(rel: Path) -> bool:
    parts = rel.parts
    for prefix in PLANTED_DIR_PREFIXES:
        if parts[: len(prefix)] == prefix:
            return True
    return False


def classify_filename(name: str) -> list[str]:
    hits = []
    for key, rx in ARTIFACT_NAME_RE.items():
        if rx.search(name):
            hits.append(key)
    return hits


def scan_text(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for key, rx in SIGNAL_PATTERNS.items():
        counts[key] = len(rx.findall(text))
    return counts


def infer_subject_type(path: Path | None, artifacts: Counter[str], is_text: bool) -> str:
    if is_text:
        if artifacts.get("process") or artifacts.get("brd"):
            return "process" if artifacts.get("process") and not artifacts.get("prd") else "brief"
        if artifacts.get("prd") or artifacts.get("brd") or artifacts.get("srs"):
            return "spec"
        return "brief"
    if path is None:
        return "brief"
    if path.is_file():
        kinds = classify_filename(path.name)
        if "prd" in kinds or "brd" in kinds or "srs" in kinds:
            return "spec"
        return "spec" if path.suffix.lower() in DOC_EXTS else "brief"
    if artifacts.get("prd") or artifacts.get("brd") or artifacts.get("user_stories"):
        return "repo"
    return "repo"


def collect_files(root: Path, max_depth: int, max_files: int) -> list[Path]:
    out: list[Path] = []
    root = root.resolve()
    for path in root.rglob("*"):
        if len(out) >= max_files:
            break
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if is_planted_rel(rel):
            continue
        if len(rel.parts) > max_depth:
            continue
        if path.is_file():
            out.append(path)
    return out


def scan_path(root: Path, max_depth: int, max_files: int) -> dict[str, Any]:
    files = collect_files(root, max_depth, max_files)
    artifacts: Counter[str] = Counter()
    keyword_hits: Counter[str] = Counter()
    docs: list[str] = []
    evidence_files: list[str] = []
    for path in files:
        rel = str(path.relative_to(root))
        kinds = classify_filename(path.name)
        suffix = path.suffix.lower()
        if suffix in DOC_EXTS or suffix in MODEL_EXTS or suffix in DATA_EXTS or kinds:
            if suffix in DOC_EXTS:
                docs.append(rel)
            for k in kinds:
                artifacts[k] += 1
            if suffix in MODEL_EXTS:
                artifacts["process"] += 1
            if suffix in DATA_EXTS:
                artifacts["data_model"] += 1
            if suffix == ".feature":
                artifacts["acceptance"] += 1
            if kinds or suffix in DOC_EXTS | MODEL_EXTS | DATA_EXTS | STORY_EXTS:
                evidence_files.append(rel)
        if suffix in DOC_EXTS or suffix == ".feature":
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:READ_CAP]
            except OSError:
                continue
            for key, n in scan_text(text).items():
                if n:
                    keyword_hits[key] += n
            for k in classify_filename(text[:2000]):
                artifacts[k] += 1
    return {
        "root": str(root),
        "file_count": len(files),
        "docs_files": sorted(docs)[:80],
        "evidence_files": sorted(set(evidence_files))[:80],
        "artifacts": dict(artifacts),
        "keyword_hits": dict(keyword_hits),
    }


def scan_blob(text: str, label: str) -> dict[str, Any]:
    keyword_hits = {k: n for k, n in scan_text(text).items() if n}
    artifacts: Counter[str] = Counter()
    for k in classify_filename(label):
        artifacts[k] += 1
    for k in classify_filename(text[:4000]):
        artifacts[k] += 1
    if keyword_hits.get("story_template"):
        artifacts["user_stories"] += 1
    if keyword_hits.get("gherkin"):
        artifacts["acceptance"] += 1
    if keyword_hits.get("stakeholder"):
        artifacts["stakeholders"] += 1
    if keyword_hits.get("moscow"):
        artifacts["prioritization"] += 1
    return {
        "root": label,
        "file_count": 1,
        "docs_files": [label],
        "evidence_files": [label],
        "artifacts": dict(artifacts),
        "keyword_hits": keyword_hits,
        "char_count": len(text),
    }


def gaps_from(artifacts: dict[str, int], hits: dict[str, int]) -> list[str]:
    missing = []
    checks = [
        ("problem", artifacts.get("prd") or hits.get("problem"), "No problem / need signal"),
        ("stakeholders", artifacts.get("stakeholders") or hits.get("stakeholder"), "No stakeholder signal"),
        ("value", artifacts.get("okrs") or hits.get("value"), "No value / success-metric signal"),
        ("requirement", artifacts.get("user_stories") or artifacts.get("srs") or hits.get("requirement"), "No requirements signal"),
        ("options", hits.get("options"), "No options / alternatives signal"),
        ("scope", hits.get("scope"), "No out-of-scope / non-goal signal"),
        ("trace", artifacts.get("traceability") or hits.get("trace"), "No traceability signal"),
        ("validation", hits.get("validation"), "No outcome-validation signal"),
    ]
    for _key, present, label in checks:
        if not present:
            missing.append(label)
    return missing


def assemble(raw: dict[str, Any], subject_hint: str | None, is_text: bool) -> dict[str, Any]:
    artifacts = Counter(raw.get("artifacts") or {})
    hits = raw.get("keyword_hits") or {}
    subject = subject_hint or infer_subject_type(None, artifacts, is_text)
    summary = {
        "subject_type": subject,
        "artifact_counts": dict(artifacts),
        "keyword_hits": hits,
        "gaps": gaps_from(artifacts, hits),
        "docs_file_count": len(raw.get("docs_files") or []),
        "file_count": raw.get("file_count", 0),
    }
    return {
        "summary": summary,
        "docs_files": raw.get("docs_files") or [],
        "evidence_files": raw.get("evidence_files") or [],
        "root": raw.get("root", ""),
        "char_count": raw.get("char_count"),
    }


def format_human(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = [
        f"Root: {payload.get('root')}",
        f"Subject type: {s.get('subject_type')}",
        f"Files: {s.get('file_count')}  Docs: {s.get('docs_file_count')}",
        f"Artifacts: {s.get('artifact_counts') or '{}'}",
        f"Keyword hits: {s.get('keyword_hits') or '{}'}",
        "Gaps:",
    ]
    gaps = s.get("gaps") or []
    if not gaps:
        lines.append("- (none flagged)")
    else:
        lines.extend(f"- {g}" for g in gaps)
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("path", nargs="?", help="File or directory to scan")
    parser.add_argument("--text", help="Scan a single text/markdown file as a brief")
    parser.add_argument("--stdin", action="store_true", help="Scan stdin as a brief")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--max-files", type=int, default=4000)
    args = parser.parse_args(argv[1:])

    if args.stdin:
        blob = sys.stdin.read()
        raw = scan_blob(blob, "stdin")
        payload = assemble(raw, "brief", True)
    elif args.text:
        src = Path(args.text)
        if not src.is_file():
            print(f"error: text file not found: {src}", file=sys.stderr)
            return 1
        raw = scan_blob(src.read_text(encoding="utf-8", errors="ignore"), str(src))
        payload = assemble(raw, infer_subject_type(src, Counter(raw["artifacts"]), True), True)
    elif args.path:
        src = Path(args.path)
        if not src.exists():
            print(f"error: path not found: {src}", file=sys.stderr)
            return 1
        if src.is_file():
            raw = scan_blob(src.read_text(encoding="utf-8", errors="ignore"), str(src))
            payload = assemble(raw, infer_subject_type(src, Counter(raw["artifacts"]), True), True)
        else:
            raw = scan_path(src, args.max_depth, args.max_files)
            payload = assemble(raw, infer_subject_type(src, Counter(raw["artifacts"]), False), False)
    else:
        parser.print_usage(sys.stderr)
        return 2

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_human(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
