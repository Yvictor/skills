#!/usr/bin/env python3
"""Extract text from downloaded TWSE broker operation manuals."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader


SKILL_ROOT = Path(__file__).resolve().parents[1]


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def extract_word(path: Path) -> str:
    result = subprocess.run(
        ["textutil", "-convert", "txt", "-stdout", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8", errors="replace")


def extract_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n--- page {page_number} ---\n\n{text}")
    return "".join(pages)


def output_name(index: str, title: str) -> str:
    safe_title = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", title, flags=re.UNICODE).strip("_")
    return f"{int(index):02d}_{safe_title}.txt"


def skill_path(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else SKILL_ROOT / path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(SKILL_ROOT / "references/source-manifest.json"))
    parser.add_argument("--output-dir", default=str(SKILL_ROOT / "assets/extracted-text"))
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    extraction_rows: list[dict[str, str]] = []
    for item in manifest:
        source = skill_path(item["file"])
        suffix = source.suffix.lower()
        if suffix in {".doc", ".docx"}:
            text = extract_word(source)
            method = "textutil"
        elif suffix == ".pdf":
            text = extract_pdf(source)
            method = "pypdf"
        else:
            raise ValueError(f"unsupported file type: {source}")

        text = clean_text(text)
        out_path = output_dir / output_name(item["index"], item["title"])
        header = (
            f"# {item['title']}\n\n"
            f"- 更新日期: {item['updated']}\n"
            f"- 來源檔案: {item['file']}\n"
            f"- 原始 URL: {item['download_url']}\n"
            f"- SHA256: {item['sha256']}\n"
            f"- 抽取方式: {method}\n\n"
            "---\n\n"
        )
        out_path.write_text(header + text, encoding="utf-8")
        extraction_rows.append(
            {
                "index": item["index"],
                "title": item["title"],
                "updated": item["updated"],
                "source_file": item["file"],
                "text_file": out_path.relative_to(SKILL_ROOT).as_posix(),
                "method": method,
                "chars": str(len(text)),
            }
        )
        print(f"{int(item['index']):02d} {method} {len(text):8d} chars {out_path.name}")

    report_path = SKILL_ROOT / "references/extraction-report.json"
    report_path.write_text(json.dumps(extraction_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(extraction_rows)} manuals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
