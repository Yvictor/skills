---
name: taiwan-stock-rules
description: |
  Taiwan stock market rules knowledge from Taiwan Stock Exchange broker operation manuals. Use when answering questions or building systems about TWSE/TPEX Taiwan equity trading rules, broker computer operation manuals, order types, trading sessions, odd-lot trading, after-hours fixed-price trading, block trading, margin trading, securities lending, day trading, account opening, settlement/default handling, ETF/ETN operations, warrants/ETF liquidity providers, market data/FIX/TCPIP specifications, and broker operational procedures.
---

# Taiwan Stock Rules

Use this skill for Taiwan stock market rule and broker-operation questions that require TWSE manual knowledge. Start from the synthesized references, then verify exact details against extracted source text.

Primary source: https://dsp.twse.com.tw/brokerManual/list

## Source Bundle

This skill is built from the TWSE `證券商作業手冊` listing. Use these resources:

- `references/rule-model.md`: integrated mental model for interpreting the broker manuals.
- `references/rule-cards.md`: concrete synthesized rule cards for common Taiwan stock market and broker-system questions.
- `references/knowledge-qa-100.md`: 100 concrete original-source-file-derived QA checks used to test whether the skill can answer TWSE broker-manual fact questions.
- `references/trading-markets.md`: synthesized guide for regular, odd-lot, after-hours, block, auction, and subscription markets.
- `references/financing-lending-and-shortfall.md`: synthesized guide for credit trading, day trading, securities lending, tender borrow/purchase, and shortfall repair.
- `references/accounts-settlement-and-exceptions.md`: synthesized guide for accounts, error accounts, account correction, settlement defaults, and exception handling.
- `references/products-liquidity-and-issuance.md`: synthesized guide for ETF, ETN, warrants, liquidity providers, and market makers.
- `references/protocols-and-market-data.md`: synthesized guide for FIX, TCP/IP host connections, market-data multicast, backup systems, and report files.
- `references/market-data-format-cards.md`: market-data format lookup cards, including common stock quote format numbers.
- `references/system-design-checklists.md`: implementation and answer-quality checklists.
- `references/source-manifest.json`: downloaded manual inventory with title, update date, source URL, local file, size, and SHA256.
- `references/manual-index.md`: table of every manual and its extracted text file.
- `references/topic-map.md`: topic-to-manual routing map.
- `references/manual-outlines.md`: lightweight outline for each manual.
- `references/query-guide.md`: common search patterns and answer requirements.
- `assets/source-files/`: original downloaded TWSE files.
- `assets/extracted-text/`: extracted text from source files.
- `references/`: curated rule references generated from the extracted manuals.

When exact rules, field names, message formats, cutoff times, or recent changes matter, consult the relevant extracted source text and cite the manual title/update date in your answer.

## Workflow

1. Identify the user’s domain: general trading, odd lots, after-hours fixed-price, block trading, margin trading, securities lending, day trading, account opening, ETF/ETN, default handling, FIX/TCPIP/market data, or broker back-office operations.
2. Read `references/rule-cards.md` for the closest concrete rule card.
3. Read `references/rule-model.md` to frame the answer as market segment + actor/account + lifecycle + protocol + risk/exception control.
4. If the user asks a short fact question like "格式幾", "哪一本手冊", "哪個作業", "能不能用", or "限制是多少", check `references/knowledge-qa-100.md` for a matching QA before opening full extracted text.
5. Read the synthesized topic reference that matches the domain:
   - Trading market workflows: `references/trading-markets.md`
   - Credit/day trading/lending/shortfalls: `references/financing-lending-and-shortfall.md`
   - Accounts/settlement/defaults/exceptions: `references/accounts-settlement-and-exceptions.md`
   - ETF/ETN/warrants/liquidity/market making: `references/products-liquidity-and-issuance.md`
   - FIX/TCPIP/market data/connectivity: `references/protocols-and-market-data.md`
   - Market-data format numbers: `references/market-data-format-cards.md`
   - Implementation review: `references/system-design-checklists.md`
6. For connectivity architecture questions, do not collapse protocol families:
   - Host connection, order, report, and FIX workflows use point-to-point TCP/IP socket/session style manuals.
   - TWSE centralized-market real-time market-data transmission (`O-126/O-127`) uses IP multicast with IGMP-capable routers/switch routers, duplicate multicast groups per channel, and sequence numbers because delivery is not guaranteed.
   - If the user asks whether "行情" is TCP, answer that the line/network is described as TCP/IP, but the market-data feed itself is multicast, not a TCP socket stream.
7. Open `references/topic-map.md`, `references/manual-index.md`, or `references/source-manifest.json` to confirm source manuals and update dates.
8. Use `references/query-guide.md` for search patterns, then read the relevant extracted text file when the answer needs exact numbers, field names, message formats, cutoff times, or edge-case rules.
9. Answer with the synthesized rule, applicable scope, implementation implication, and source manual title/update date.
10. If multiple manuals conflict, prefer the newest manual for that topic and call out the conflict.

## Maintenance

Run maintenance commands from this skill directory.

Refresh source files with:

```bash
uv run --with requests python scripts/download_twse_broker_manuals.py
```

After refreshing, re-run text extraction and regenerate curated references before relying on changed files.

Extract text with:

```bash
uv run --with pypdf python scripts/extract_twse_manual_text.py
```

Regenerate indexes with:

```bash
uv run python scripts/build_reference_indexes.py
uv run python scripts/build_manual_outlines.py
```

Regenerate the 100-question source-file QA bank with:

```bash
uv run --with pypdf python scripts/build_source_file_qa.py
uv run python scripts/audit_qa_bank.py
```
