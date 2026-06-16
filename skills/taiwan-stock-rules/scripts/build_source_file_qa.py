#!/usr/bin/env python3
"""Build 100 QA items from original TWSE source files.

The generated QA bank uses `assets/source-files` as the authority. PDF source
files are parsed with pypdf; Word source files are read directly through macOS
`textutil`. The generated evidence points back to the original source file and
page/line or text line, not to `assets/extracted-text`.

Run from the skill root:

    uv run --with pypdf python scripts/build_source_file_qa.py
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader


SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = SKILL_ROOT / "assets" / "source-files"
OUT = SKILL_ROOT / "references" / "knowledge-qa-100.md"


@dataclass(frozen=True)
class Evidence:
    source_file: str
    locator: str
    text: str


@dataclass(frozen=True)
class QA:
    question: str
    answer: str
    evidence: Evidence
    route: str


def clean_cell(text: str) -> str:
    return " ".join(text.replace("|", "/").split())


def clean_format_description(text: str) -> str:
    return re.sub(r"\s*\.{2,}\s*\d+\s*$", "", clean_cell(text)).strip()


def normalize_search(text: str) -> str:
    return (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("１", "1")
        .replace("　", " ")
    )


@lru_cache(maxsize=None)
def pdf_pages(path: Path) -> list[list[str]]:
    reader = PdfReader(str(path))
    pages: list[list[str]] = []
    for page in reader.pages:
        pages.append((page.extract_text() or "").splitlines())
    return pages


@lru_cache(maxsize=None)
def word_lines(path: Path) -> list[str]:
    proc = subprocess.run(
        ["textutil", "-convert", "txt", "-stdout", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout.splitlines()


def word_evidence(filename: str, needle: str) -> Evidence:
    path = SOURCE_FILES / filename
    normalized_needle = normalize_search(needle)
    for line_no, line in enumerate(word_lines(path), start=1):
        if normalized_needle in normalize_search(line):
            return Evidence(f"assets/source-files/{filename}", f"line {line_no}", line.strip())
    raise ValueError(f"missing source evidence in {filename}: {needle}")


def pdf_evidence(filename: str, needle: str) -> Evidence:
    path = SOURCE_FILES / filename
    normalized_needle = normalize_search(needle)
    for page_no, lines in enumerate(pdf_pages(path), start=1):
        for line_no, line in enumerate(lines, start=1):
            if normalized_needle in normalize_search(line):
                return Evidence(f"assets/source-files/{filename}", f"page {page_no} line {line_no}", line.strip())
    raise ValueError(f"missing PDF evidence in {filename}: {needle}")


def o126_format_catalog_qas() -> list[QA]:
    filename = "O-126-A10_TWSE集中市場即時交易資訊傳輸規格書_B.12.13_202612.pdf"
    pages = pdf_pages(SOURCE_FILES / filename)
    rows: list[QA] = []
    pattern = re.compile(r"^(格式[一二三四五六七八九十百]+)：(.+?)(?:\\s+\\.{2,}|$)")
    # Page 13 is the table of contents for current data formats.
    for line_no, line in enumerate(pages[12], start=1):
        match = pattern.search(line.strip())
        if not match:
            continue
        fmt, description = match.groups()
        description = clean_format_description(description)
        rows.append(
            QA(
                question=f"{description} 是格式幾？",
                answer=fmt,
                evidence=Evidence(f"assets/source-files/{filename}", f"page 13 line {line_no}", line.strip()),
                route="market-data-format-cards.md",
            )
        )
    if len(rows) != 23:
        raise ValueError(f"expected 23 O-126 format rows, found {len(rows)}")
    return rows


def o126_format_code_qas() -> list[QA]:
    filename = "O-126-A10_TWSE集中市場即時交易資訊傳輸規格書_B.12.13_202612.pdf"
    facts = [
        ("PACK BCD “01”表示格式一", "格式一的傳輸格式代碼用 PACK BCD 表示是多少？", "01"),
        ("PACK BCD “02”表示格式二", "格式二的傳輸格式代碼用 PACK BCD 表示是多少？", "02"),
        ("PACK BCD “04”表示格式四", "格式四的傳輸格式代碼用 PACK BCD 表示是多少？", "04"),
        ("PACK BCD “05”表示格式五", "格式五的傳輸格式代碼用 PACK BCD 表示是多少？", "05"),
        ("PACK BCD “06”表示格式六", "格式六的傳輸格式代碼用 PACK BCD 表示是多少？", "06"),
        ("PACK BCD “07”表示格式七", "格式七的傳輸格式代碼用 PACK BCD 表示是多少？", "07"),
        ("PACK BCD “08”表示格式八", "格式八的傳輸格式代碼用 PACK BCD 表示是多少？", "08"),
        ("PACK BCD “13”表示格式十三", "格式十三的傳輸格式代碼用 PACK BCD 表示是多少？", "13"),
        ("PACK BCD “15”表示格式十五", "格式十五的傳輸格式代碼用 PACK BCD 表示是多少？", "15"),
        ("PACK BCD “16”表示格式十六", "格式十六的傳輸格式代碼用 PACK BCD 表示是多少？", "16"),
        ("PACK BCD “17”表示格式十七", "格式十七的傳輸格式代碼用 PACK BCD 表示是多少？", "17"),
        ("PACK BCD “18”表示格式十八", "格式十八的傳輸格式代碼用 PACK BCD 表示是多少？", "18"),
        ("PACK BCD “19”表示格式十九", "格式十九的傳輸格式代碼用 PACK BCD 表示是多少？", "19"),
        ("PACK BCD “20”表示格式二十", "格式二十的傳輸格式代碼用 PACK BCD 表示是多少？", "20"),
        ("PACK BCD“21”表示格式二十一", "格式二十一的傳輸格式代碼用 PACK BCD 表示是多少？", "21"),
        ("PACK BCD “22”表示格式二十二", "格式二十二的傳輸格式代碼用 PACK BCD 表示是多少？", "22"),
        ("PACK BCD “23”表示格式二十三", "格式二十三的傳輸格式代碼用 PACK BCD 表示是多少？", "23"),
        ("PACK BCD “24”表示格式二十四", "格式二十四的傳輸格式代碼用 PACK BCD 表示是多少？", "24"),
        ("PACK BCD “25”表示格式二十五", "格式二十五的傳輸格式代碼用 PACK BCD 表示是多少？", "25"),
    ]
    return [
        QA(q, a, pdf_evidence(filename, needle), "market-data-format-cards.md")
        for needle, q, a in facts
    ]


def o126_transmission_qas() -> list[QA]:
    filename = "O-126-A10_TWSE集中市場即時交易資訊傳輸規格書_B.12.13_202612.pdf"
    facts = [
        ("01 第一 IP 格式 6 格式 12", "盤中即時行情第一 IP 的即時行情資料格式是幾？", "格式 6"),
        ("01 第一 IP 格式 6 格式 12", "盤中即時行情第一 IP 的開收盤價資料格式是幾？", "格式 12"),
        ("02 第二 IP 格式 17 格式 18", "盤中即時行情第二 IP 的即時行情資料格式是幾？", "格式 17"),
        ("02 第二 IP 格式 17 格式 18", "盤中即時行情第二 IP 的開收盤價資料格式是幾？", "格式 18"),
        ("格式六：個股買、賣、成交價量揭示時即時傳送", "格式六何時傳送？", "個股買、賣、成交價量揭示時即時傳送"),
        ("格式二十：每 5 秒傳送一次個股買、賣、成交價量的最近一筆行情揭示", "格式二十的傳送頻率是？", "每 5 秒傳送一次最近一筆行情揭示"),
        ("格式二十三：零股買、賣、成交價量揭示時即時傳送", "格式二十三何時傳送？", "零股買、賣、成交價量揭示時即時傳送"),
        ("格式二十五：約 07:40-17:10 借券賣出可用餘額資訊", "格式二十五大約在什麼時間傳送借券賣出可用餘額資訊？", "約 07:40-17:10"),
    ]
    return [
        QA(q, a, pdf_evidence(filename, needle), "market-data-format-cards.md")
        for needle, q, a in facts
    ]


def word_source_qas() -> list[QA]:
    facts = [
        ("O-019-A10_盤後定價交易電腦作業手冊.docx", "AP-CODE = 7", "盤後定價交易子系統的連線 AP-CODE 是多少？", "AP-CODE = 7", "trading-markets.md"),
        ("O-019-A10_盤後定價交易電腦作業手冊.docx", "併入一般交易回報", "盤後定價交易成交回報是否併入一般交易回報？", "是，併入一般交易回報", "trading-markets.md"),
        ("O-019-A10_盤後定價交易電腦作業手冊.docx", "補送成交回報子系統", "盤後定價成交回報資料漏失時由哪個子系統補送？", "補送成交回報子系統", "trading-markets.md"),
        ("O-019-A10_盤後定價交易電腦作業手冊.docx", "價格必須為 0", "盤後定價交易輸入訊息的 PRICE 必須是多少？", "0", "trading-markets.md"),
        ("O-019-A10_盤後定價交易電腦作業手冊.docx", "小於等於499", "盤後定價交易輸入訊息的數量上限是多少？", "499", "trading-markets.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "PVC申報作業(B97)：於08:00 ~ 18:00", "權證暨 ETF 流動量提供者 PVC 申報作業 B97 的時間是？", "08:00 ~ 18:00", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "PVC查詢作業(B98)：於08:00 ~ 18:00", "權證暨 ETF 流動量提供者 PVC 查詢作業 B98 的時間是？", "08:00 ~ 18:00", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "若超過50次", "權證暨 ETF 流動量提供者 PVC 檔案欄位錯誤累計超過幾次會不繼續處理？", "50 次", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "檔案代號 :B97", "權證暨 ETF 流動量提供者 PVC 申報檔的檔案代號是？", "B97", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "“01”  權證流動量專用線路新增", "WK-CODE 01 代表什麼？", "權證流動量專用線路新增", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "“02”  權證流動量專用線路刪除", "WK-CODE 02 代表什麼？", "權證流動量專用線路刪除", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "“03”  ETF流動量專用線路新增", "WK-CODE 03 代表什麼？", "ETF 流動量專用線路新增", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "“04”  ETF流動量專用線路刪除", "WK-CODE 04 代表什麼？", "ETF 流動量專用線路刪除", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "請再作一次”B98” 查詢確認", "權證暨 ETF 流動量提供者 PVC 申報正確後要再做哪個查詢確認？", "B98 查詢確認", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "申報ETF流動量提供者專用線路只能為FIX線路", "ETF 流動量提供者專用線路只能用什麼線路申報？", "FIX 線路", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "檔案代號 :B98", "權證暨 ETF 流動量提供者 PVC 查詢檔的檔案代號是？", "B98", "products-liquidity-and-issuance.md"),
        ("O-026-A10_權證暨ETF流動量提供者專用電腦作業手冊.doc", "”****” 表示要求所有總分公司", "B98 查詢的 RQST-BRKID 填 **** 代表什麼？", "要求所有總分公司", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "必需等到交易所回覆錯誤訊息檔回來", "ETN 證券商端傳送申報作業檔後，下一筆傳送前要等什麼？", "交易所回覆錯誤訊息檔", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "若欄位需填入中文，編碼請使用BIG5碼", "ETN 證券商端檔案欄位若需填中文要用什麼編碼？", "BIG5 碼", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "若超過30次", "ETN 證券商端欄位錯誤累計超過幾次會不繼續處理？", "30 次", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申購賣回基本資料檔(PRF)查詢作業(ME3)", "ETN 證券商端 PRF 基本資料檔查詢作業代號是？", "ME3", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "查詢開放時間為0800 – 1530", "ETN 證券商端 PRF 查詢開放時間是？", "0800-1530", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "交易所0800主動傳送", "ETN 證券商端 PRF 基本資料檔交易所幾點主動傳送？", "0800", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "剩餘可供申請單位數查詢作業(MEN)", "ETN 證券商端剩餘可供申請單位數查詢作業代號是？", "MEN", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申請申購賣回檔申報作業(ME4)", "ETN 證券商端申請申購賣回檔申報作業代號是？", "ME4", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申請申購賣回檔查詢作業(ME5)", "ETN 證券商端申請申購賣回檔查詢作業代號是？", "ME5", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申請賣回部位圈存檔查詢作業(ME6)", "ETN 證券商端申請賣回部位圈存檔查詢作業代號是？", "ME6", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "初審回覆檔查詢作業(MEC)", "ETN 證券商端初審回覆檔查詢作業代號是？", "MEC", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "T日實際申購賣回價金檔查詢作業(MEF)", "ETN 證券商端 T 日實際申購賣回價金檔查詢作業代號是？", "MEF", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申購足額明細確認檔查詢作業(MEG)", "ETN 證券商端申購足額明細確認檔查詢作業代號是？", "MEG", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申購足額明細確認檔申報作業(MEH)", "ETN 證券商端申購足額明細確認檔申報作業代號是？", "MEH", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申購賣回足額明細確認檔(複審)查詢作業(MEK)", "ETN 證券商端申購賣回足額明細確認檔複審查詢作業代號是？", "MEK", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "申購/賣回款項應收應付檔查詢作業(MEO)", "ETN 證券商端申購/賣回款項應收應付檔查詢作業代號是？", "MEO", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "投資人名冊檔查詢作業(MEP)", "ETN 證券商端投資人名冊檔查詢作業代號是？", "MEP", "products-liquidity-and-issuance.md"),
        ("O-033-A10_ETN申購賣回平台--證券商端電腦作業手冊.doc", "終止上市款項應收應付檔查詢作業(MES)", "ETN 證券商端終止上市款項應收應付檔查詢作業代號是？", "MES", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "交易日前一日(T-1日)16:30至19:00", "ETN 發行人端 PRF ME1 必須在什麼時間申報？", "T-1 日 16:30 至 19:00", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "T日15:30至18:00發行人可查詢賣回圈存結果", "ETN 發行人端 T 日賣回圈存結果查詢時間是？", "T 日 15:30 至 18:00", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "T+1日09:00前發行人必須申報T日實際申購賣回價金檔", "ETN 發行人端 T 日實際申購賣回價金檔必須何時前申報？", "T+1 日 09:00 前", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "T+1日09:30至12:00前", "ETN 發行人端複審價金確認時間是？", "T+1 日 09:30 至 12:00 前", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "T+1日12:30至15:30前可查詢申購賣回款項應收應付檔", "ETN 發行人端申購賣回款項應收應付檔何時可查？", "T+1 日 12:30 至 15:30 前", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "交易日(T日)09:00至15:30前，可進行申請增加庫存造市用單位數", "ETN 發行人端增加庫存造市用單位數可在何時申請？", "T 日 09:00 至 15:30 前", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "後續可透過MEV查詢報價豁免日期檔檢查", "ETN 發行人端報價豁免日期檔申報後可用哪個代號查詢檢查？", "MEV", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "賣回部分無論發行人註記任何字元，皆為確認Y", "ETN 發行人端賣回部分複審確認如何處理？", "無論註記任何字元，皆為確認 Y", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "下市日13:30申贖平台產製ETN投資人名冊", "ETN 發行人端投資人名冊在下市日幾點產製？", "13:30", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "下市日2:00後可查詢終止上市款項應收應付檔", "ETN 發行人端終止上市款項應收應付檔下市日何時後可查？", "2:00 後", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "發行人不得辦理自行發行ETN之申購賣回申請", "ETN 發行人可否辦理自行發行 ETN 的申購賣回申請？", "不得辦理", "products-liquidity-and-issuance.md"),
        ("O-034-A10_ETN申購賣回平台--發行人端電腦作業手冊.doc", "用戶ID固定為「自營商代號」+「IR01」", "ETN 發行人管理員用戶 ID 規則是什麼？", "自營商代號 + IR01", "products-liquidity-and-issuance.md"),
        ("O-124-A10_FIX4.4電文規範作業手冊.doc", "一般交易為0、盤後零股交易為2、盤後定價交易為7、盤中零股為C", "FIX TargetSubID 中一般交易、盤後零股、盤後定價、盤中零股分別是什麼？", "0、2、7、C", "protocols-and-market-data.md"),
        ("O-032-A10_證券商受託辦理定期定額買賣有價證券業務.doc", "每次傳送檔案之筆數最多8000筆", "定期定額業務每次傳送檔案最多幾筆？", "8000 筆", "trading-markets.md"),
        ("O-032-A10_證券商受託辦理定期定額買賣有價證券業務.doc", "普通交易，請輸入交易單位，最多499交易單位", "定期定額普通交易 CAJ-MTHQTY 最多幾個交易單位？", "499 交易單位", "trading-markets.md"),
    ]
    return [
        QA(q, a, word_evidence(filename, needle), route)
        for filename, needle, q, a, route in facts
    ]


def render(rows: list[QA]) -> str:
    lines = [
        "# Knowledge QA 100",
        "",
        "This QA bank is generated from original files in `assets/source-files`, not from synthesized references or `assets/extracted-text`. PDF evidence uses source page/line from pypdf; Word evidence uses source text lines from `textutil`.",
        "",
        "| ID | Question | Answer | Source Evidence | Route |",
        "| --- | --- | --- | --- | --- |",
    ]
    for idx, row in enumerate(rows, start=1):
        evidence = f"{row.evidence.source_file} {row.evidence.locator} - {clean_cell(row.evidence.text)}"
        lines.append(
            f"| {idx:03d} | {clean_cell(row.question)} | {clean_cell(row.answer)} | `{evidence}` | {row.route} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    rows = (
        o126_format_catalog_qas()
        + o126_format_code_qas()
        + o126_transmission_qas()
        + word_source_qas()
    )
    if len(rows) != 100:
        raise SystemExit(f"expected 100 rows, generated {len(rows)}")
    OUT.write_text(render(rows), encoding="utf-8")
    print(f"wrote {OUT.relative_to(SKILL_ROOT)} with {len(rows)} source-file QA items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
