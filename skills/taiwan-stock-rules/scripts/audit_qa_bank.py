#!/usr/bin/env python3
"""Validate the 100-question original-source QA coverage reference.

This is intentionally lightweight and uses only the Python standard library so it can
run with `uv run python scripts/audit_qa_bank.py`.
"""

from __future__ import annotations

from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
QA_FILE = SKILL_ROOT / "references" / "knowledge-qa-100.md"
REFERENCES = SKILL_ROOT / "references"
SOURCE_FILES = SKILL_ROOT / "assets" / "source-files"


def parse_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for line in QA_FILE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"ID", "---"}:
            continue
        rows.append(cells)
    return rows


def main() -> int:
    rows = parse_rows()
    errors: list[str] = []

    if len(rows) != 100:
        errors.append(f"expected 100 QA rows, found {len(rows)}")

    seen: set[str] = set()
    for row in rows:
        if len(row) != 5:
            errors.append(f"row has {len(row)} cells, expected 5: {row}")
            continue
        item_id, question, answer, evidence, route = row
        if item_id in seen:
            errors.append(f"duplicate ID {item_id}")
        seen.add(item_id)
        if not item_id.isdigit() or len(item_id) != 3:
            errors.append(f"bad ID format: {item_id}")
        if not question.endswith("？"):
            errors.append(f"question should end with Chinese question mark: {item_id}")
        if not answer:
            errors.append(f"blank answer: {item_id}")
        if not evidence:
            errors.append(f"blank evidence: {item_id}")
        if "assets/source-files/" not in evidence:
            errors.append(f"evidence is not from original source files: {item_id}")
        if not route:
            errors.append(f"blank route: {item_id}")
        if route.endswith(".md") and not (REFERENCES / route).exists():
            errors.append(f"missing route file for {item_id}: {route}")
        match = evidence.strip("`").split(" - ", 1)[0]
        if match.startswith("assets/source-files/"):
            rel = match.split(" line ", 1)[0].split(" page ", 1)[0]
            path = SKILL_ROOT / rel
            if not path.exists():
                errors.append(f"missing evidence file for {item_id}: {rel}")

    expected_ids = [f"{i:03d}" for i in range(1, 101)]
    actual_ids = [row[0] for row in rows if row]
    if actual_ids != expected_ids:
        errors.append("IDs are not exactly 001..100 in order")

    if errors:
        print("QA bank audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("QA bank audit passed: 100 original-source items with valid evidence and routes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
