#!/usr/bin/env python3
"""Build navigational reference indexes for the Taiwan stock rules skill."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


TOPIC_RULES: list[tuple[str, list[str]]] = [
    ("core-trading", ["一般交易", "盤中零股", "零股交易", "盤後定價", "鉅額", "拍賣", "公開申購", "定期定額"]),
    ("margin-and-day-trading", ["信用交易", "現股當日沖銷", "借券賣出"]),
    ("securities-lending", ["有價證券借貸", "補正借券", "標借", "標購", "證金標購", "證金議借", "借貸款項"]),
    ("account-and-settlement", ["投資人開戶", "違約", "錯帳", "更正帳號", "綜合交易帳號", "聯合徵信", "聯徵中心", "保管及運用"]),
    ("etf-etn-warrants-liquidity", ["ETF", "ETN", "權證", "流動量", "股票造市者", "交易獎勵"]),
    ("market-data-and-protocols", ["即時交易資訊", "Market Information", "FIX", "TCPIP", "主機連線", "第二路", "成交回報", "資訊交換平台"]),
    ("broker-operations", ["統計檔案", "備援", "備用競價設備"]),
]
SKILL_ROOT = Path(__file__).resolve().parents[1]


def classify(title: str) -> list[str]:
    topics = [topic for topic, keywords in TOPIC_RULES if any(keyword in title for keyword in keywords)]
    return topics or ["other"]


def load_json(path: str) -> list[dict[str, str]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_manual_index(manifest: list[dict[str, str]], extraction: dict[str, dict[str, str]], output: Path) -> None:
    lines = [
        "# TWSE Broker Manual Index",
        "",
        "This index covers every file downloaded from `https://dsp.twse.com.tw/brokerManual/list`.",
        "",
        "| # | Manual | Updated | Type | Extracted text | SHA256 |",
        "|---:|---|---|---|---|---|",
    ]
    for item in manifest:
        report = extraction[item["index"]]
        source_type = Path(item["file"]).suffix.lower().lstrip(".")
        lines.append(
            "| {index} | {title} | {updated} | {source_type} | `{text_file}` | `{sha}` |".format(
                index=item["index"],
                title=item["title"].replace("|", "\\|"),
                updated=item["updated"],
                source_type=source_type,
                text_file=report["text_file"],
                sha=item["sha256"][:12],
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_topic_map(manifest: list[dict[str, str]], extraction: dict[str, dict[str, str]], output: Path) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in manifest:
        for topic in classify(item["title"]):
            grouped[topic].append(item)

    descriptions = {
        "core-trading": "一般交易、零股、盤後定價、鉅額交易、拍賣、公開申購、定期定額。",
        "margin-and-day-trading": "信用交易、現股當日沖銷、借券賣出相關作業。",
        "securities-lending": "有價證券借貸、標借、標購、證金標購/議借、補正借券。",
        "account-and-settlement": "開戶、違約、錯帳更正、綜合帳戶、徵信、款項保管運用。",
        "etf-etn-warrants-liquidity": "ETF、ETN、權證、流動量提供者、股票造市與交易獎勵。",
        "market-data-and-protocols": "行情資訊、FIX、TCP/IP、主機連線、成交回報、資訊交換平台。",
        "broker-operations": "券商統計檔案、備援、備用競價設備等作業。",
        "other": "未分類或低頻專門手冊。",
    }

    lines = [
        "# Taiwan Stock Rules Topic Map",
        "",
        "Use this map to choose which extracted manuals to read for a Taiwan stock market rule question.",
        "",
        "Search command pattern:",
        "",
        "```bash",
        "rg -n \"<keyword>\" assets/extracted-text",
        "```",
        "",
    ]
    for topic, _keywords in TOPIC_RULES + [("other", [])]:
        items = grouped.get(topic, [])
        if not items:
            continue
        lines.extend([f"## {topic}", "", descriptions[topic], ""])
        for item in items:
            report = extraction[item["index"]]
            lines.append(f"- `{item['index']}` {item['title']} ({item['updated']}): `{report['text_file']}`")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(SKILL_ROOT / "references/source-manifest.json"))
    parser.add_argument("--extraction-report", default=str(SKILL_ROOT / "references/extraction-report.json"))
    parser.add_argument("--output-dir", default=str(SKILL_ROOT / "references"))
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    extraction = {item["index"]: item for item in load_json(args.extraction_report)}
    output_dir = Path(args.output_dir)
    write_manual_index(manifest, extraction, output_dir / "manual-index.md")
    write_topic_map(manifest, extraction, output_dir / "topic-map.md")
    print(f"Indexed {len(manifest)} manuals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
