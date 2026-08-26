#!/usr/bin/env python3
"""Render a business-analysis markdown report into self-contained HTML.

Stdlib only. Offline (system fonts). Does not invent scores, overall, or rank
tokens — it styles whatever the markdown already contains. Math lives in
``scripts/score_report.py`` (ADR 0001). Markdown parse lives in
``scripts/report_parse.py``; CSS in ``scripts/report_theme.py``.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from report_parse import (  # noqa: E402
    META_LABELS,
    header_index,
    is_sep_row,
    parse_meta,
    parse_tables,
    rank_token,
    split_cells,
    strip_inline_md,
)
from report_theme import CSS  # noqa: E402

SKIP_BODY_HEADINGS = {
    "scorecard",
}

RANK_CLASS = {
    "Excellent": "excellent",
    "Good": "good",
    "Fair": "fair",
    "Poor": "poor",
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def extract_score(raw: str) -> str:
    m = re.search(r"(\d+(?:\.\d+)?)", raw or "")
    return m.group(1) if m else "—"


def score_number(raw: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)", raw or "")
    return float(m.group(1)) if m else None


def rank_class(rank: str) -> str:
    token = rank_token(rank)
    return RANK_CLASS.get(token, "na")


def project_name(path: str) -> str:
    if not path:
        return "untitled"
    cleaned = path.strip().strip("`").rstrip("/")
    return Path(cleaned).name or cleaned


def ticks(score: float | None) -> str:
    filled = 0 if score is None else max(0, min(10, int(round(score))))
    cells = []
    for i in range(10):
        cls = "on" if i < filled else "off"
        cells.append(f'<i class="{cls}"></i>')
    return '<span class="ticks">' + "".join(cells) + "</span>"


def render_scorecard(table: list[list[str]] | None) -> str:
    if not table or len(table) < 2:
        return ""
    header = table[0]
    i_prin = header_index(header, "principle")
    i_score = header_index(header, "score (0-10)", "score")
    if i_prin is None or i_score is None:
        return ""
    i_ev = header_index(header, "key evidence", "evidence")
    cards = []
    for row in table[1:]:
        if max(i_prin, i_score) >= len(row):
            continue
        prin = strip_inline_md(row[i_prin])
        score_raw = strip_inline_md(row[i_score])
        evidence = (
            strip_inline_md(row[i_ev]) if i_ev is not None and i_ev < len(row) else ""
        )
        n = score_number(score_raw)
        if n is None:
            band = "na"
        elif n >= 9:
            band = "excellent"
        elif n >= 7:
            band = "good"
        elif n >= 5:
            band = "fair"
        else:
            band = "poor"
        notes_html = f'<p class="notes">{inline(evidence)}</p>' if evidence else ""
        display = score_raw if n is None else (str(int(n)) if n == int(n) else score_raw)
        cards.append(
            f"""<article class="cat {band}">
  <header>
    <span class="cat-name">{esc(prin)}</span>
    <span class="pill {band}">{esc(display)}</span>
  </header>
  <div class="cat-score">
    <b>{esc(display)}</b>
    {ticks(n)}
  </div>
  {notes_html}
</article>"""
        )
    if not cards:
        return ""
    return (
        '<section class="scorecard"><h2>Scorecard</h2><div class="cat-grid">'
        + "".join(cards)
        + "</div></section>"
    )


def extract_section(md: str, title: str) -> tuple[str, str]:
    """Return one markdown section and the document without that section."""
    lines = md.splitlines(keepends=True)
    start: int | None = None
    end = len(lines)
    level = 0
    target = title.strip().lower()

    for i, line in enumerate(lines):
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if not heading:
            continue
        heading_level = len(heading.group(1))
        heading_title = re.sub(r"\s+", " ", heading.group(2)).strip().lower()
        if start is None:
            if heading_title == target:
                start = i
                level = heading_level
        elif heading_level <= level:
            end = i
            break

    if start is None:
        return "", md
    section = "".join(lines[start:end]).strip()
    remainder = "".join(lines[:start] + lines[end:])
    return section, remainder


def md_body_html(md: str) -> str:
    """Convert report markdown to HTML, skipping dashboard-duplicated sections."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    skip = False
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith("# ")):
        i += 1
    while i < len(lines):
        m = re.match(r"^\*\*([^:*]+):\*\*\s+", lines[i])
        if m and m.group(1) in META_LABELS:
            i += 1
            continue
        break

    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if not para:
            return
        text = " ".join(para)
        para = []
        out.append(f"<p>{inline(text)}</p>")

    while i < len(lines):
        line = lines[i]
        heading = re.match(r"^(#{2,6})\s+(.+)$", line)
        if heading:
            flush_para()
            level = len(heading.group(1))
            title = heading.group(2).strip()
            key = re.sub(r"\s+", " ", title).strip().lower()
            key = re.sub(r"^\d+\.\s+", "", key)
            key = re.sub(r"\s*\(.*\)$", "", key)
            skip = key in SKIP_BODY_HEADINGS
            if not skip:
                tag = f"h{min(level, 4)}"
                slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
                out.append(f'<{tag} id="{esc(slug)}">{inline(title)}</{tag}>')
            i += 1
            continue

        if skip:
            i += 1
            continue

        if line.startswith("```"):
            flush_para()
            fence = line[3:].strip()
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            lang = f' class="lang-{esc(fence)}"' if fence else ""
            out.append(f"<pre{lang}><code>{esc(chr(10).join(buf))}</code></pre>")
            continue

        if line.lstrip().startswith("|"):
            flush_para()
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = split_cells(lines[i])
                if not is_sep_row(cells):
                    rows.append(cells)
                i += 1
            if rows:
                thead = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body = []
                for row in rows[1:]:
                    tds = "".join(f"<td>{inline(c)}</td>" for c in row)
                    body.append(f"<tr>{tds}</tr>")
                out.append(
                    f"<div class='table-wrap'><table><thead><tr>{thead}</tr></thead>"
                    f"<tbody>{''.join(body)}</tbody></table></div>"
                )
            continue

        ul = re.match(r"^[-*]\s+(.+)$", line)
        ol = re.match(r"^(\d+)\.\s+(.+)$", line)
        if ul or ol:
            flush_para()
            ordered = bool(ol)
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < len(lines):
                um = re.match(r"^[-*]\s+(.+)$", lines[i])
                om = re.match(r"^\d+\.\s+(.+)$", lines[i])
                if ordered and om:
                    items.append(f"<li>{inline(om.group(1))}</li>")
                elif not ordered and um:
                    items.append(f"<li>{inline(um.group(1))}</li>")
                elif not lines[i].strip():
                    break
                else:
                    break
                i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        if not line.strip():
            flush_para()
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(out)


def render_html(md: str) -> str:
    meta = parse_meta(md)
    tables = parse_tables(md)
    readiness_md, article_md = extract_section(md, "Decision Readiness")
    readiness_html = ""
    if readiness_md:
        readiness_html = (
            '<section class="article decision-readiness">'
            + md_body_html(readiness_md)
            + "</section>"
        )
    rank = meta.get("Rank", "")
    rclass = rank_class(rank)
    score = extract_score(meta.get("Overall Score", ""))
    name = project_name(meta.get("Project", ""))
    kicker = ""
    m = re.search(r"(?im)^[-*]\s*(?:verdict|veredicto):\s*(.+)$", md)
    if m:
        kicker = f'<p class="hero-kicker">{inline(m.group(1))}</p>'

    chips = []
    for key in ("Audit mode", "Subject type", "Cadence", "Date", "Evidence coverage"):
        val = meta.get(key)
        if val:
            label = val if key != "Evidence coverage" else f"coverage {val}"
            chips.append(f'<span class="chip">{esc(label)}</span>')

    title = f"{name} — {rank or 'business analysis report'}"
    path = meta.get("Project", "")
    scorecard = tables.get("scorecard")
    if scorecard is None:
        for key, rows in tables.items():
            if "scorecard" in key:
                scorecard = rows
                break

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="sheet">
    <header class="masthead">
      <div class="wordmark"><b>Business Analysis</b><span>101 analyzer</span></div>
      <div class="mast-meta">{esc(path)}<br>{esc(meta.get("Date", ""))}</div>
    </header>
    {readiness_html}
    <section class="hero">
      <div class="score-block">
        <div class="label">Overall score</div>
        <div class="score">{esc(score)}</div>
        <div class="denom">/ 10</div>
      </div>
      <div class="status-block {rclass}">
        <div class="stamp stamp-{rclass}">{esc(rank_token(rank) or "UNSET")}</div>
        {kicker}
        <div class="chips">{"".join(chips)}</div>
      </div>
    </section>
    {render_scorecard(scorecard)}
    <div class="article">
      {md_body_html(article_md)}
    </div>
    <footer class="foot">
      <span>101-business-analysis</span>
      <span>markdown + html · evidence only</span>
    </footer>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print("usage: render-report.py INPUT.md [OUTPUT.html]", file=sys.stderr)
        return 2
    src = Path(argv[1])
    if not src.is_file():
        print(f"error: markdown not found: {src}", file=sys.stderr)
        return 1
    dest = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".html")
    try:
        dest.write_text(render_html(src.read_text(encoding="utf-8")), encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
