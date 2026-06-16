# Taiwan Stock Rules Query Guide

Use this guide before opening full manual text.

## Source Order

1. `topic-map.md` - choose the relevant topic and manual.
2. `manual-outlines.md` - inspect the manual outline.
3. `assets/extracted-text/*.txt` - search or read the full extracted manual text.
4. `assets/source-files/*` - use the original file when extracted text is ambiguous.

## Common Searches

```bash
rg -n "交易時間|交易時段|撮合|委託|價格|漲跌幅|逐筆交易" assets/extracted-text
rg -n "盤中零股|零股|盤後定價" assets/extracted-text
rg -n "鉅額|逐筆交易|配對交易" assets/extracted-text
rg -n "信用交易|融資|融券|當沖|現股當日沖銷" assets/extracted-text
rg -n "借券|有價證券借貸|標借|標購|補正借券" assets/extracted-text
rg -n "開戶|綜合交易帳號|定期定額|錯帳|更正帳號|違約" assets/extracted-text
rg -n "ETF|ETN|權證|流動量|造市者" assets/extracted-text
rg -n "FIX|TCPIP|主機連線|行情|即時交易資訊|成交回報" assets/extracted-text
```

Architecture and transport questions:

```bash
rg -n "IGMP|Multicast|TCP/IP|Socket|Source Port|防火牆|主機房|備援機房|測試機房|PVC|VC|Heartbeat|第二路|成交回報" assets/extracted-text
```

When the question sounds like "到底是不是 TCP/multicast", route first to `references/broker-exchange-integration.md`, then verify exact facts in `O-105` for host sockets or `O-126/O-127` for market data.

## Answer Requirements

When answering:

- Name the source manual and update date.
- Quote or paraphrase only the relevant rule text.
- State whether the answer is about trading rules, broker computer operations, message/file formats, or market data protocols.
- If the question asks for protocol fields, read the full extracted manual and preserve field names exactly.
- If the question asks for a current rule with legal or production impact, verify against the TWSE source page before treating it as final.
