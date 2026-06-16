#!/usr/bin/env python3
"""Build lightweight outlines from extracted TWSE manual text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(
    r"^(?:[壹貳參肆伍陸柒捌玖拾]+、|[一二三四五六七八九十]+、|第[一二三四五六七八九十0-9]+[章節]|[0-9]+(?:\.[0-9]+){0,3}\s+).{2,80}$"
)
SKILL_ROOT = Path(__file__).resolve().parents[1]


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def candidate_outline_lines(text: str, limit: int = 80) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = clean_line(raw)
        if not line or line.startswith("- ") or line.startswith("#"):
            continue
        if "\t" in raw and len(line) <= 100:
            lines.append(line)
        elif HEADING_RE.match(line):
            lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extraction-report", default=str(SKILL_ROOT / "references/extraction-report.json"))
    parser.add_argument("--output", default=str(SKILL_ROOT / "references/manual-outlines.md"))
    args = parser.parse_args()

    report = json.loads(Path(args.extraction_report).read_text(encoding="utf-8"))
    output: list[str] = [
        "# TWSE Manual Outlines",
        "",
        "Lightweight outlines extracted from the beginning and heading-like lines of each manual. Use this to choose the right full text file.",
        "",
    ]
    for item in report:
        text_path = Path(item["text_file"])
        if not text_path.is_absolute():
            text_path = SKILL_ROOT / text_path
        text = text_path.read_text(encoding="utf-8", errors="replace")
        lines = candidate_outline_lines(text)
        output.extend([f"## {int(item['index']):02d}. {item['title']}", "", f"- 更新日期: {item['updated']}", f"- 全文: `{item['text_file']}`", ""])
        if lines:
            output.extend(f"- {line}" for line in lines[:40])
        else:
            output.append("- No outline lines detected; read the full extracted text.")
        output.append("")

    Path(args.output).write_text("\n".join(output), encoding="utf-8")
    print(f"Wrote outlines for {len(report)} manuals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
