#!/usr/bin/env python3
"""Audit the source-grounded expert self exam.

This does not prove an LLM will answer every prompt perfectly. It enforces that the
skill carries enough integration test coverage and the critical architecture
guardrails that failed in manual questioning.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAM = ROOT / "references" / "expert-self-exam.md"
HANDBOOK = ROOT / "references" / "broker-exchange-integration.md"
MATRIX = ROOT / "references" / "manual-domain-matrix.md"
MANIFEST = ROOT / "references" / "source-manifest.csv"
MIND_MAP = ROOT / "references" / "twse-broker-mind-map.md"


def fail(message: str) -> None:
    raise SystemExit(f"expert self-exam audit failed: {message}")


def main() -> None:
    exam = EXAM.read_text(encoding="utf-8")
    handbook = HANDBOOK.read_text(encoding="utf-8")
    matrix = MATRIX.read_text(encoding="utf-8")
    mind_map = MIND_MAP.read_text(encoding="utf-8")

    ids = re.findall(r"\| ([A-Z]\d{2}) \|", exam)
    if len(ids) < 40:
        fail(f"expected at least 40 exam items, found {len(ids)}")
    if len(ids) != len(set(ids)):
        fail("duplicate exam IDs found")

    required_prefixes = {"A": 8, "S": 8, "M": 8, "F": 5, "R": 8, "X": 6}
    for prefix, minimum in required_prefixes.items():
        count = sum(1 for item in ids if item.startswith(prefix))
        if count < minimum:
            fail(f"expected at least {minimum} {prefix} items, found {count}")

    required_exam_terms = [
        "IP multicast",
        "not a TCP socket stream",
        "IGMP",
        "Source IP + Source Port Number",
        "25 seconds",
        "60 seconds",
        "duplicate/redundant",
        "B37",
        "XTAI",
        "ROCO",
        "full-day backup",
    ]
    for term in required_exam_terms:
        if term not in exam:
            fail(f"missing exam guardrail term: {term}")

    required_handbook_terms = [
        "Do not treat all \"TCP/IP\" mentions as TCP streams.",
        "Centralized-market real-time market data is IP multicast",
        "Broker is client/session initiator; TWSE is server/listener.",
        "TWSE identifies a socket by `Source IP + Source Port Number`.",
        "Main and backup sites use the same host IP address.",
        "Second execution-report channels as duplicate/redundant delivery",
        "route 1 sends and receives route 1 replies; route 2 sends and receives route 2 replies",
        "224.8.100.100:10008",
    ]
    for term in required_handbook_terms:
        if term not in handbook:
            fail(f"missing handbook guardrail term: {term}")

    # Every source-manual row should appear in the manual domain matrix.
    manifest_lines = MANIFEST.read_text(encoding="utf-8").splitlines()[1:]
    titles = []
    for line in manifest_lines:
        parts = line.split(",", 3)
        if len(parts) < 2:
            fail(f"could not parse manifest line: {line}")
        titles.append(parts[1])
    if len(titles) != 48:
        fail(f"expected 48 source manuals, found {len(titles)}")
    for title in titles:
        if title not in matrix:
            fail(f"source manual missing from manual-domain-matrix.md: {title}")

    manual_prompts = re.findall(r"\| W\d{2} \|", exam)
    if len(manual_prompts) < 48:
        fail(f"expected at least 48 whole-manual prompts, found {len(manual_prompts)}")

    required_matrix_terms = [
        "違約",
        "借券",
        "開戶",
        "標借",
        "Do not answer \"借券\"",
        "all-source-manual coverage matrix",
    ]
    for term in required_matrix_terms:
        if term not in matrix:
            fail(f"missing matrix guardrail term: {term}")

    required_mind_map_terms = [
        "```mermaid",
        "48 TWSE Source Manuals",
        "Ambiguity Map",
        "O-010 ordinary and credit default",
        "O-004 tender borrowing",
        "O-126 market data Chinese",
        "Source IP plus Source Port",
        "IP multicast",
        "B40 discretionary investment account",
    ]
    for term in required_mind_map_terms:
        if term not in mind_map:
            fail(f"missing mind-map term: {term}")

    print(
        f"Expert self-exam audit passed: {len(ids)} integration items, "
        f"{len(manual_prompts)} manual-coverage prompts, and {len(titles)} source manuals."
    )


if __name__ == "__main__":
    main()
