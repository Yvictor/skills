# Market Data Format Cards

Use this file for TWSE centralized-market real-time market-data format-number questions. Verify exact field layouts in the extracted `O-126` or `O-127` source text before implementing parsers.

Primary sources:

- `O-126-A10 TWSE集中市場即時交易資訊傳輸規格書(B.12.13)(202612)`, updated `115.05.15`.
- `O-127-A10 Market Information Specification(B.12.13)(202612)`, updated `115.05.15`.

## Common Answer

If the user asks "交易所即時行情傳輸股票會是格式幾", answer:

- 集中市場普通股競價交易即時行情資訊: 格式六.
- The transmission format code in the packet is PACK BCD `06`.

If the user asks whether real-time market data is TCP or multicast, answer:

- The market-data transmission line is described as TCP/IP/IP market-data network.
- The real-time market-data feed itself uses IP multicast, not a TCP socket stream.
- Recipients need IGMP-capable router/switch-router equipment.
- Each channel's market data is published in duplicate on two separate multicast groups/addresses.
- Delivery is not guaranteed by the multicast/broadcast function, so receivers must check transmission sequence numbers.

Related stock-market data formats:

| Question intent | TWSE format |
| --- | --- |
| 普通股個股基本資料 | 格式一 |
| 普通股競價交易成交統計資料 | 格式二 |
| 普通股競價交易委託統計資料 | 格式四 |
| 公告資訊 | 格式五 |
| 普通股競價交易即時行情資訊 | 格式六 |
| 普通股定價交易成交統計資料 | 格式七 |
| 普通股定價交易委託統計資料 | 格式八 |
| 普通股定價交易個股成交資料 | 格式九 |
| 新編臺灣指數資料 | 格式十 |
| 普通股競價交易開(收)盤價資料 | 格式十二 |
| 零股交易即時揭示資訊 | 格式十三 |
| 認購(售)權證全稱資料 | 格式十四 |
| 當日停止交易股票資料 | 格式十五 |
| 行情傳輸系統 HeartBeat 資料 | 格式十六 |
| 認購(售)權證競價交易即時行情資訊 | 格式十七 |
| 認購(售)權證競價交易開(收)盤價資料 | 格式十八 |
| 當日暫停/恢復交易股票資料 | 格式十九 |
| 普通股競價交易行情快照資訊 | 格式二十 |
| 即時指數基本資料 | 格式二十一 |
| 盤中零股交易個股基本資料 | 格式二十二 |
| 盤中零股交易即時行情資訊 | 格式二十三 |
| 認購(售)權證競價交易行情快照資訊 | 格式二十四 |
| 借券賣出可用餘額 | 格式二十五 |

Transmission format code lookup:

| TWSE format | PACK BCD code |
| --- | --- |
| 格式一 | `01` |
| 格式二 | `02` |
| 格式四 | `04` |
| 格式五 | `05` |
| 格式六 | `06` |
| 格式七 | `07` |
| 格式八 | `08` |
| 格式十三 | `13` |
| 格式十五 | `15` |
| 格式十六 | `16` |
| 格式十七 | `17` |
| 格式十八 | `18` |
| 格式十九 | `19` |
| 格式二十 | `20` |
| 格式二十一 | `21` |
| 格式二十二 | `22` |
| 格式二十三 | `23` |
| 格式二十四 | `24` |
| 格式二十五 | `25` |

## Transmission Line Mapping

For the "盤中即時行情傳送線路及對應格式" table in `O-126`:

| 傳送線路 | 即時行情資料格式 | 開(收)盤價資料格式 |
| --- | --- | --- |
| 第一 IP | 格式六 | 格式十二 |
| 第二 IP | 格式十七 | 格式十八 |

Use this table when the question is about feed line mapping. Use the format catalog when the question is about product/message identity. In the current B.12.13 catalog, format 17/18 are also described under warrant quote/open-close data, so quote the exact table or field section being used when answering implementation questions.

## Multicast Line Settings

`O-126/O-127` describe market-data channels as duplicate multicast groups. Common settings from Appendix E / 附錄五:

| Line | Transmission category | Multicast groups |
| --- | --- | --- |
| 1st IP | Stock real-time market data and basic data | `224.0.100.100:10000`, `224.0.200.200:20000` |
| 2nd IP | Call/put warrant real-time market data and basic data | `224.2.100.100:10002`, `224.2.200.200:20002` |
| 3rd IP | Stock and warrant snapshot/basic data | `224.4.100.100:10004`, `224.4.200.200:20004` |

## Implementation Notes

- Do not infer field positions from the format number alone; read the relevant format section in `assets/extracted-text/03_O-126-A10_TWSE集中市場即時交易資訊傳輸規格書_B.12.13_202612.txt`.
- Do not implement the real-time market-data feed as a TCP client just because the spec says TCP/IP protocol for lines; implement multicast receive with IGMP-capable network equipment and sequence-gap detection.
- For format six, confirm variable record length, transmission format code, stock code sentinel behavior, status bits, price/quantity encoding, and trial calculation behavior from the source section.
- Pin parser behavior to spec version `B.12.13` and source update date `115.05.15`.
