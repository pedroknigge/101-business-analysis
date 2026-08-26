#!/usr/bin/env python3
"""HTML theme for architecture reports. Presentation only; no scoring."""

from __future__ import annotations

CSS = """
:root {
  --bg: #0b0f14;
  --paper: #121821;
  --ink: #e8eef6;
  --muted: #9aa8b8;
  --faint: #6e7c8c;
  --line: #1e2833;
  --line-strong: #2c3a4a;
  --excellent: #3dd68c;
  --good: #7ec8ff;
  --fair: #e8a317;
  --poor: #ff5d4a;
  --na: #6e7c8c;
  --font-display: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  --font-sans: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
.sheet {
  max-width: 1080px;
  margin: 0 auto;
  padding: 28px 22px 80px;
}
.masthead {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  border-bottom: 1px solid var(--line-strong);
  padding-bottom: 14px;
  margin-bottom: 28px;
}
.wordmark {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: -0.02em;
  font-size: 13px;
  line-height: 1.2;
}
.wordmark b { display: block; font-size: 22px; letter-spacing: -0.02em; }
.wordmark span {
  color: var(--muted);
  font-family: var(--font-mono);
  font-weight: 400;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.mast-meta {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--muted);
  text-align: right;
  line-height: 1.45;
}
.hero {
  display: grid;
  grid-template-columns: minmax(240px, 340px) 1fr;
  align-items: stretch;
  margin-bottom: 36px;
  border: 1px solid var(--line);
  background: var(--paper);
}
.score-block {
  padding: 22px 28px 24px;
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 220px;
}
.score-block .label {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}
.score {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(3.4rem, 7vw, 5.2rem);
  letter-spacing: -0.03em;
  line-height: 1;
  margin: 12px 0;
}
.denom {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}
.status-block {
  padding: 22px 24px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
}
.status-block.excellent { box-shadow: inset 6px 0 0 var(--excellent); }
.status-block.good { box-shadow: inset 6px 0 0 var(--good); }
.status-block.fair { box-shadow: inset 6px 0 0 var(--fair); }
.status-block.poor { box-shadow: inset 6px 0 0 var(--poor); }
.stamp {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(1.6rem, 3.6vw, 2.5rem);
  letter-spacing: -0.02em;
  line-height: 1.15;
  text-transform: uppercase;
}
.stamp-excellent { color: var(--excellent); }
.stamp-good { color: var(--good); }
.stamp-fair { color: var(--fair); }
.stamp-poor { color: var(--poor); }
.hero-kicker {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.5;
  max-width: 48ch;
}
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border: 1px solid var(--line-strong);
  padding: 5px 8px;
  color: var(--ink);
}
h2 {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 13px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0 0 14px;
  color: var(--muted);
}
.scorecard { margin-bottom: 36px; }
.cat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}
.cat {
  background: var(--paper);
  padding: 14px 16px 12px;
}
.cat header { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
.cat-name { font-weight: 600; font-size: 15px; }
.cat-score { display: flex; align-items: center; gap: 12px; margin-top: 10px; }
.cat-score b {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
  min-width: 1.4ch;
}
.ticks { display: flex; gap: 3px; flex: 1; }
.ticks i { display: block; height: 8px; flex: 1; background: var(--line-strong); }
.ticks i.on { background: var(--ink); }
.cat.poor .ticks i.on { background: var(--poor); }
.cat.fair .ticks i.on { background: var(--fair); }
.cat.good .ticks i.on { background: var(--good); }
.cat.excellent .ticks i.on { background: var(--excellent); }
.notes { margin: 8px 0 0; color: var(--muted); font-size: 14px; line-height: 1.45; }
.pill {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 7px;
  border: 1px solid currentColor;
  white-space: nowrap;
}
.pill.excellent { color: var(--excellent); }
.pill.good { color: var(--good); }
.pill.fair { color: var(--fair); }
.pill.poor { color: var(--poor); }
.pill.na { color: var(--na); }
.article {
  border-top: 1px solid var(--line-strong);
  padding-top: 28px;
}
.article h2 {
  font-size: 13px;
  margin: 32px 0 12px;
  color: var(--ink);
  letter-spacing: 0.12em;
}
.article h3 {
  font-family: var(--font-sans);
  font-size: 20px;
  font-weight: 600;
  margin: 28px 0 10px;
  letter-spacing: -0.01em;
  line-height: 1.3;
}
.article h4 { font-size: 16px; margin: 20px 0 8px; line-height: 1.35; }
.article p { margin: 0 0 12px; max-width: 68ch; }
.article ul, .article ol { margin: 0 0 16px; padding-left: 1.2em; max-width: 68ch; }
.article li { margin: 0 0 8px; }
code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: #0a1016;
  border: 1px solid var(--line);
  padding: 0.05em 0.35em;
}
pre {
  background: #070b10;
  border: 1px solid var(--line-strong);
  padding: 16px 18px;
  overflow-x: auto;
  margin: 0 0 20px;
}
pre code { background: none; border: 0; padding: 0; font-size: 13.5px; line-height: 1.55; }
.table-wrap { overflow-x: auto; margin: 0 0 20px; border: 1px solid var(--line); }
table { width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.45; }
th, td {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
th {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--paper);
}
.foot {
  margin-top: 48px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--faint);
  display: flex;
  justify-content: space-between;
  gap: 12px;
}
@media (max-width: 760px) {
  .hero, .cat-grid { grid-template-columns: 1fr; }
  .score-block { border-right: 0; border-bottom: 1px solid var(--line); min-height: 0; }
  .masthead { flex-direction: column; align-items: flex-start; }
  .mast-meta { text-align: left; }
}
@media print {
  body { background: #fff; color: #111; }
  .sheet { padding: 0; }
  .hero, .cat, pre, code { background: #fff; }
  .cat-grid, .hero { border-color: #111; background: #111; }
  a { color: inherit; }
}
"""
