#!/usr/bin/env python3
"""Parse report markdown meta, tables, and rank tokens.

Stdlib only. Does not compute overall or rank.
"""

from __future__ import annotations

import re

META_LABELS = (
    "Project",
    "Date",
    "Audit mode",
    "Subject type",
    "Cadence",
    "Overall Score",
    "Rank",
    "Evidence coverage",
)

RANK_TOKEN_RE = re.compile(r"(Excellent|Good|Fair|Poor)(?:\s+\(.*\))?$")
_SEP_CELL_RE = re.compile(r":?-{3,}:?")


def strip_inline_md(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^`+|`+$", "", text)
    text = re.sub(r"\*\*", "", text)
    return text.strip()


def parse_rank(raw: str) -> str:
    """Exact rank token; optional trailing parenthetical. Slash lists are not a rank."""
    text = (raw or "").strip()
    m = RANK_TOKEN_RE.fullmatch(text)
    return m.group(1) if m else ""


rank_token = parse_rank


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(_SEP_CELL_RE.fullmatch(c.replace(" ", "")) for c in cells)


def parse_meta(md: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for label in META_LABELS:
        m = re.search(
            rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
            md,
            re.MULTILINE,
        )
        if m:
            meta[label] = strip_inline_md(m.group(1))
    return meta


def parse_tables(md: str) -> dict[str, list[list[str]]]:
    """Map lowercase heading → table rows (header first)."""
    tables: dict[str, list[list[str]]] = {}
    heading = ""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        h = re.match(r"^#{2,6}\s+(.+)$", lines[i])
        if h:
            heading = re.sub(r"\s+", " ", h.group(1)).strip().lower()
            heading = re.sub(r"^\d+\.\s+", "", heading)
            heading = re.sub(r"\s*\(.*\)$", "", heading)
            i += 1
            continue
        if lines[i].lstrip().startswith("|") and heading:
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                raw = split_cells(lines[i])
                if not is_sep_row(raw):
                    rows.append(raw)
                i += 1
            if rows:
                tables[heading] = rows
            continue
        i += 1
    return tables


def header_index(header: list[str], *names: str) -> int | None:
    lowered = [h.lower() for h in header]
    for name in names:
        if name in lowered:
            return lowered.index(name)
    for i, h in enumerate(lowered):
        for name in names:
            if name in h:
                return i
    return None
