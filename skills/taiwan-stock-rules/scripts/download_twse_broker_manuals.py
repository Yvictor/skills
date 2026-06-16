#!/usr/bin/env python3
"""Download TWSE broker operation manuals listed on dsp.twse.com.tw."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, unquote, urljoin, urlparse, urlunparse

import requests


LIST_URL = "https://dsp.twse.com.tw/brokerManual/list"
USER_AGENT = "Mozilla/5.0 (compatible; codex-skill-builder/1.0)"
SKILL_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ManualLink:
    title: str
    updated: str
    detail_url: str


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def request_bytes(url: str) -> bytes:
    response = requests.get(quote_url(url), headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    return response.content


def quote_url(url: str) -> str:
    parsed = urlparse(url)
    path = quote(unquote(parsed.path), safe="/%")
    query = quote(unquote(parsed.query), safe="=&?/:,+%")
    return urlunparse((parsed.scheme, parsed.netloc, path, parsed.params, query, parsed.fragment))


def parse_manual_links(html: str, base_url: str) -> list[ManualLink]:
    links: list[ManualLink] = []
    row_pattern = re.compile(r"<tr\b.*?</tr>", flags=re.I | re.S)
    anchor_pattern = re.compile(
        r'<a\s+href=["\']([^"\']+)["\'][^>]*>\s*(O-[^<]+?)\s*</a>',
        flags=re.I | re.S,
    )
    date_pattern = re.compile(
        r"<font>\s*更新日期\s*</font>\s*<span>\s*([0-9]{2,3}\.[0-9]{2}\.[0-9]{2})\s*</span>",
        flags=re.I | re.S,
    )
    for row in row_pattern.findall(html):
        anchor = anchor_pattern.search(row)
        if not anchor:
            continue
        date = date_pattern.search(row)
        links.append(
            ManualLink(
                title=normalize_text(re.sub(r"<[^>]+>", " ", anchor.group(2))),
                updated=date.group(1) if date else "",
                detail_url=urljoin(base_url, anchor.group(1)),
            )
        )
    return links


def find_download_url(detail_html: str, detail_url: str) -> str:
    candidates = re.findall(r'href=["\']([^"\']+)["\']', detail_html, flags=re.I)
    ranked: list[str] = []
    for href in candidates:
        absolute = urljoin(detail_url, href)
        lower = absolute.lower()
        if any(token in lower for token in ("download", "file", "attachment")):
            ranked.append(absolute)
        elif any(lower.endswith(ext) for ext in (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".txt")):
            ranked.append(absolute)
    if ranked:
        return ranked[0]
    # Some detail URLs directly return the file.
    return detail_url


def filename_from_response(url: str, content: bytes, title: str) -> str:
    parsed = urlparse(url)
    path_name = Path(unquote(parsed.path)).name
    suffix = Path(path_name).suffix.lower()
    if not suffix:
        if content.startswith(b"%PDF"):
            suffix = ".pdf"
        elif content.startswith(b"PK\x03\x04"):
            suffix = ".zip"
        elif content[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            suffix = ".doc"
        else:
            suffix = ".bin"
    safe_title = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", title, flags=re.UNICODE).strip("_")
    return f"{safe_title}{suffix}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = path.with_suffix(".csv")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(SKILL_ROOT / "assets/source-files"))
    parser.add_argument("--manifest", default=str(SKILL_ROOT / "references/source-manifest.json"))
    parser.add_argument("--sleep", type=float, default=0.2)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    html = request_bytes(LIST_URL).decode("utf-8", errors="replace")
    manuals = parse_manual_links(html, LIST_URL)
    if not manuals:
        print("No manuals found", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    for index, manual in enumerate(manuals, start=1):
        detail_bytes = request_bytes(manual.detail_url)
        download_url = find_download_url(detail_bytes.decode("utf-8", errors="ignore"), manual.detail_url)
        file_bytes = detail_bytes if download_url == manual.detail_url else request_bytes(download_url)
        filename = filename_from_response(download_url, file_bytes, manual.title)
        path = output_dir / filename
        path.write_bytes(file_bytes)
        rows.append(
            {
                "index": str(index),
                "title": manual.title,
                "updated": manual.updated,
                "detail_url": manual.detail_url,
                "download_url": download_url,
                "file": path.relative_to(SKILL_ROOT).as_posix(),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
            }
        )
        print(f"{index:02d} {manual.title} -> {path.name}", file=sys.stderr)
        time.sleep(args.sleep)

    write_manifest(Path(args.manifest), rows)
    print(f"Downloaded {len(rows)} manuals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
