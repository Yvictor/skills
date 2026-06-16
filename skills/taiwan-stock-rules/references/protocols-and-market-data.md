# Protocols, Market Data, Connectivity, And Broker System Operations

This file synthesizes the computer-operation and protocol manuals. Use full extracted text for exact layouts.

## Protocol Families

The TWSE manual bundle includes several protocol surfaces:

- Order-entry and broker operation files/messages in product-specific manuals.
- Host connection manuals: `O-101`, `O-105`, `O-106`, `O-107`, `O-108`.
- FIX 4.4 manuals: `O-124` Chinese, `O-125` English.
- Market information transmission specs: `O-126` Chinese, `O-127` English.
- Backup/contingency manuals: `O-104`, `O-128`.
- Statistical/report files: `O-016`.

Do not mix these layers. A trading rule answer may mention FIX, but exact FIX tags and workflows belong in the FIX manuals.

## Host Connection And TCP/IP

Use:

- `O-101-A10 主機連線電腦作業手冊`
- `O-105-A10 TCPIP網路主機連線電腦作業手冊`
- `O-106-A10 資訊交換平台主機連線電腦作業手冊`
- `O-107-A10 證券商申請第二成交回報通道及TCPIP網路擴充版成交回報電腦作業手冊`
- `O-108-A10 第二路檔案傳輸電腦作業手冊`

System implications:

- These manuals are about broker-host connectivity, trading/report/file/session flows, and related infrastructure; do not use them to infer centralized-market quote feed transport.
- Broker host connection is modeled as TCP/IP socket/session connectivity over TWSE IP trading network lines.
- Connection/session state is separate from order state.
- Backup channels and second execution-report channels must be modeled as infrastructure capabilities.
- A reconnect/recovery path should not silently replay business messages without idempotency controls.

Sources: `O-101` updated `115.03.16`; `O-105/O-106/O-107/O-108` updated `104.12.09`.

## FIX 4.4

Use:

- `O-124-A10 FIX4.4電文規範作業手冊`
- `O-125-A10 TWSE FIX 4.4 Specification`

Synthesis:

- FIX is a protocol surface for order/routing workflows; it does not replace market-segment rules.
- Validate market segment, price type, time-in-force, account restrictions, and product eligibility before building FIX messages.
- Use the FIX manual for exact tags, values, session rules, acknowledgements, and rejects.
- The English and Chinese versions should be cross-checked when implementing production integrations.
- Source-derived `TargetSubID` examples: general trading `0`, after-hours odd lot `2`, after-hours fixed-price `7`, intraday odd lot `C`, tender borrowing `4`, auction `5`, general tender purchase `6`, securities-finance tender purchase `B`.

Sources: `O-124` updated `114.05.05`; `O-125` updated `114.09.03`.

## Market Data

Use:

- `O-126-A10 TWSE集中市場即時交易資訊傳輸規格書(B.12.13)(202612)`
- `O-127-A10 Market Information Specification(B.12.13)(202612)`
- `market-data-format-cards.md` for common format-number lookups.

Synthesis:

- Market-data feeds are not order-entry APIs.
- Real-time market-data transmission is multicast, not a TCP socket stream.
- `O-126` says quote recipients need IGMP-capable router/switch-router equipment to connect to the IP market-data transmission network.
- `O-126` says each line uses TCP/IP protocol, but also explicitly says IP market information is sent with the Multicast transmission protocol, with identical content sent through two multicast groups.
- `O-127` says each channel's market data is published in duplicate on two separate multicast addresses.
- Because this multicast/broadcast delivery has no guaranteed delivery mechanism, receivers must use the transmission sequence number to check whether data is complete.
- Treat market-data message versions, field layouts, and feed contents as versioned contracts.
- Build consumers with schema/version awareness; do not hard-code assumptions from older B versions.
- Use the English spec for cross-language implementers and the Chinese spec for local terminology.
- Common lookup: 集中市場普通股競價交易即時行情資訊 is 格式六; the packet transmission format code is PACK BCD `06`.
- Related stock quote formats: 普通股競價交易開(收)盤價資料 is 格式十二, 普通股競價交易行情快照資訊 is 格式二十, and 盤中零股交易即時行情資訊 is 格式二十三.
- Example multicast groups from the transmission setting table: first IP `224.0.100.100:10000` and `224.0.200.200:20000`; second IP `224.2.100.100:10002` and `224.2.200.200:20002`; third IP `224.4.100.100:10004` and `224.4.200.200:20004`.

Sources: `O-126` and `O-127`, both updated `115.05.15`.

## Architecture Answer Patterns

Use these direct answers for recurring connectivity questions:

| User question | Answer |
| --- | --- |
| 交易所主機連線是不是 TCP？ | For broker host connection/order/report/file workflows, yes: use the host/FIX/TCPIP manuals and describe TCP/IP socket/session connectivity. |
| 行情是不是 TCP 傳輸？ | No if the user means the real-time quote feed payload. The market-data line is described as TCP/IP/IP network, but `O-126/O-127` specify IP multicast with duplicate multicast groups. |
| 行情有沒有保證送達？ | No guaranteed delivery is stated for the broadcast/multicast function; use transmission sequence numbers to detect gaps. |
| 有沒有 multicast？ | Yes for centralized-market real-time market data; no evidence to apply multicast to broker order-entry/host-connection workflows. |

## Backup And Contingency

Use:

- `O-104-A10 集中市場當日全量備援電腦作業手冊`
- `O-128-A10 證券商備用競價設備系統-證券商使用手冊`

Synthesis:

- Backup mechanisms are operational continuity systems, not regular market access paths.
- Model them as controlled modes with explicit activation, role, and reconciliation requirements.
- Never assume primary and backup systems can run active-active without checking the manual.

Sources: `O-104` updated `115.03.13`; `O-128` updated `114.08.27`.

## Statistics And Reports

`O-016-A10 各類資訊統計檔案電腦作業手冊` is the place to start for statistical/report file questions. Do not search trading manuals first when the user asks for daily statistics, report file formats, or broker report ingestion.

Source: `O-016-A10 各類資訊統計檔案電腦作業手冊`, updated `115.06.01`.

## Implementation Checklist

Before implementing a protocol integration:

1. Identify market segment and actor first.
2. Identify protocol family second.
3. Confirm session/connection behavior.
4. Confirm message/file code.
5. Confirm field lengths, encodings, numeric units, date/time format, and allowed values.
6. Confirm positive and negative acknowledgement behavior.
7. Confirm reconciliation reports and recovery behavior.
8. Add version pinning to the implementation docs.
