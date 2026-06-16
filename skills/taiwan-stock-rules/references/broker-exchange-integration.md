# TWSE Broker-Exchange Integration Handbook

Use this file when the user asks how securities firms connect to TWSE, how order/report/file/FIX/market-data channels differ, what happens during failures, or how to design a broker-side system.

This is a synthesized professional model. For exact field layouts, message IDs, and line settings, reopen the cited source manual.

## Source Map

| Area | Primary manuals |
| --- | --- |
| Classic broker host connection | `O-101-A10 主機連線電腦作業手冊`, updated `115.03.16` |
| TCP/IP trading network and socket layer | `O-105-A10 TCPIP網路主機連線電腦作業手冊`, updated `104.12.09` |
| FIX order/session surface | `O-124-A10 FIX4.4電文規範作業手冊`, updated `114.05.05`; `O-125-A10 TWSE FIX 4.4 Specification`, updated `114.09.03` |
| Centralized-market real-time market data | `O-126-A10 TWSE集中市場即時交易資訊傳輸規格書(B.12.13)(202612)` and `O-127-A10 Market Information Specification(B.12.13)(202612)`, both updated `115.05.15` |
| Second execution-report channel | `O-107-A10 證券商申請第二成交回報通道及TCPIP網路擴充版成交回報電腦作業手冊`, updated `104.12.09` |
| Second file-transfer channel | `O-108-A10 第二路檔案傳輸電腦作業手冊`, updated `104.12.09` |
| Full-day backup / spare auction equipment | `O-104-A10 集中市場當日全量備援電腦作業手冊`, updated `115.03.13`; `O-128-A10 證券商備用競價設備系統-證券商使用手冊`, updated `114.08.27` |

## Non-Negotiable Architecture Rules

1. Do not treat all "TCP/IP" mentions as TCP streams.
2. Broker host/order/report/file/FIX connectivity is point-to-point socket/session oriented.
3. Centralized-market real-time market data is IP multicast with IGMP-capable network equipment and duplicate multicast groups.
4. Market-data multicast has no guaranteed delivery; sequence numbers and duplicate feeds are receiver controls, not optional decorations.
5. Host connection manuals do not define quote-feed transport; market-data manuals do.
6. Market-data specs do not define order-entry workflow; trading/FIX/host manuals do.
7. Backup lines, second channels, and full-day backup are controlled operational modes, not active-active business semantics unless the relevant manual says so.

## Big Picture

TWSE-broker integration is not one API. It is a set of surfaces:

```text
Broker OMS / back office / APs
  |
  | order, report, query, file, FIX workflows
  v
Broker socket/FIX/file interface
  |
Dedicated broker firewall
  |
Dedicated broker router
  |
TWSE IP trading network: point-to-point fixed-IP VC/PVC
  |
TWSE routers / main, backup, test sites
  |
TWSE trading, report, file, and host systems

Market-data receiver is separate:

TWSE market-data system
  |
Telecom/IP market-data network
  |
Multicast groups, duplicated per channel
  |
IGMP-capable broker/information-company network
  |
Feed handler with sequence-gap and duplicate-feed handling
```

## Broker Host Connection Versus Market Data

| Question | Correct answer |
| --- | --- |
| 下單/回報/檔傳是不是 TCP socket? | Yes for the TCP/IP host-connection/FIX surfaces. Broker side initiates or manages point-to-point sessions as specified by the relevant manual. |
| 即時行情是不是 TCP stream? | No. `O-126/O-127` specify IP multicast. The lines are described in TCP/IP/IP-network terms, but the feed payload is multicast. |
| 有沒有 multicast? | Yes for centralized-market real-time market data. Do not apply multicast to broker order-entry unless another source says so. |
| 行情會不會掉資料? | Yes, the multicast/broadcast function does not guarantee delivery. Receivers must use transmission sequence numbers and duplicate multicast groups to detect gaps. |
| 主機連線手冊能不能回答行情傳輸? | Only for shared network vocabulary. Use `O-126/O-127` for market-data transport and layouts. |

## Trading Network Topology

From `O-105`, the TWSE IP trading network is a private trading network where broker-TWSE links are point-to-point fixed-IP virtual circuits.

Broker side:

- Data line enters a dedicated broker router.
- The router must be dedicated to the IP trading network and have at least one WAN port and one LAN port.
- The firewall must also be dedicated to the IP trading network and installed between the dedicated router and the trading host.
- TWSE manages and assigns broker IP addresses.
- Each broker data line can receive one trading IP and one test IP.
- Different data lines use different IP addresses.
- A backup ADSL line uses the original line's assigned IP and does not receive a separate IP.
- A broker may apply for multiple lines/IPs; multiple head/branch companies may share one IP/line.

TWSE side:

- Main data center: two routers in backup/HA relationship.
- Backup data center: two routers in backup/HA relationship.
- Test data center: one router.
- Each broker data line sets PVCs to TWSE-side routers; ADSL can connect by only one PVC to one TWSE router.
- Main and backup sites use the same host IP address.
- Normal operation uses the main site. Backup-site VC is normally not enabled.
- During main-site failure, TWSE closes the main-site VC and enables the backup-site VC. Broker line/IP settings should not need changes, but full-day backup checks still apply.
- Test site uses different IPs, and brokers must use test IPs for testing.

## Socket Layer Model

`O-105` uses a socket layer to preserve legacy TMP AP behavior while moving transport to TCP/IP.

Key model:

- Broker APs such as order entry, execution report receipt, and file transfer sit behind a broker-side socket communication layer.
- Socket layer establishes/re-establishes sockets, sends data, receives data, and performs heartbeat/connection confirmation.
- TMP messages are wrapped with socket-level header/trailer fields into SLM, then sent as TCP byte stream data.
- Receiver strips the SLM wrapper and passes TMP back to AP.
- One socket performs one function. Different functions require different sockets.
- Source port numbers are configured by the broker during application and must differ per socket.
- Broker is client/session initiator; TWSE is server/listener.
- TWSE identifies a socket by `Source IP + Source Port Number`.
- Reusing the same `Source IP + Source Port Number` is treated as socket reconstruction and terminates the original session.

Operational timing:

- After `connect()`, the broker waits up to 25 seconds for TWSE acceptance/error/no-message handling.
- If no AP TMP message needs sending for 60 seconds, the broker sends a heartbeat/connection-confirmation SLM.
- After receiving a message from TWSE, the broker waits up to 25 seconds for the next message/heartbeat; no message can indicate network component or TWSE hardware/software issues and should trigger session close/rebuild.
- Any send/receive error path generally closes the socket session and rebuilds after cause handling.
- After each socket session is established, the AP should perform host connection subsystem startup notice, login, and application subsystem startup before business work.

## Market-Data Multicast Model

`O-126/O-127` define centralized-market real-time market-data transmission.

Connection requirements:

- Recipient uses an IGMP-capable router or switch router to connect to the IP market-data transmission network.
- Transmission circuits are described as using TCP/IP protocol.
- IP market information is sent with the Multicast transmission protocol.
- Each channel's market data is published in duplicate on two multicast addresses/groups.
- The TCP/IP broadcast/multicast function has no guaranteed delivery, so a transmission sequence number field is added for receiver completeness checks.

Common multicast settings:

| Line | Transmission category | Multicast groups |
| --- | --- | --- |
| First IP | Stock real-time market data and securities basic data | `224.0.100.100:10000`, `224.0.200.200:20000` |
| Second IP | Call/put warrant real-time market data and securities basic data | `224.2.100.100:10002`, `224.2.200.200:20002` |
| Third IP | Stock and warrant 5-second snapshot/basic data | `224.4.100.100:10004`, `224.4.200.200:20004` |
| Fourth IP | Statistics, announcement, securities-borrowing sell information | `224.6.100.100:10006`, `224.6.200.200:20006` |
| Fifth IP | Intraday odd-lot real-time market data and intraday odd-lot securities basic data | `224.8.100.100:10008`, `224.8.200.200:20008` |

Receiver design implications:

- Join the correct multicast groups; do not open a TCP client for the real-time quote feed.
- Decode PACK BCD fields and versioned message layouts.
- Track transmission sequence number per format/feed where specified.
- Compare duplicate multicast groups and fail over or reconcile when one side gaps.
- Treat HeartBeat format 16 as network/feed health evidence, not as proof that every business message was received.
- Format 16 HeartBeat is sent about every 30 seconds; status values include `S`, `L`, `R`, and `T`, where `R` means restart after transmission abnormality and interrupted HeartBeat data is not retransmitted.

## FIX Surface

FIX is another order/session surface, not the market-data multicast feed and not a replacement for market rules.

Core facts from `O-124/O-125`:

- FIX messages are variable length and made of `tag=value` fields separated by SOH.
- Standard Header precedes Body and Standard Trailer closes the message.
- Broker-to-TWSE `SenderCompID` represents the connected broker as market + broker ID + FIX Socket ID.
- Broker-to-TWSE `TargetCompID` is `XTAI` for TWSE centralized market and `ROCO` for TPEx.
- `SenderSubID` is the actual broker ID accepting the customer order.
- `TargetSubID` identifies market segment/AP-CODE-like board: examples include general trading `0`, after-hours odd lot `2`, after-hours fixed-price `7`, intraday odd lot `C`, tender borrowing `4`, auction `5`, general tender purchase `6`, and securities-finance tender purchase `B`.
- Do not answer FIX tag questions from memory; reopen the FIX manual for exact tag numbers and allowed values.

## Execution Reports And Second Channels

Execution report workflows are separate from order entry and market data.

From `O-107`:

- Older host connection allowed one execution-report PVC/socket; second-channel rules allow two execution-report channels under constraints.
- A broker may apply for two TCP/IP execution-report socket sessions.
- A broker may apply for one TCP/IP execution-report socket and one X.25 execution-report PVC.
- A broker may not apply for two X.25 execution-report PVCs.
- Two execution-report channels carry the same report content.
- TCP/IP expanded execution report can carry up to 48 execution-report records per report message.
- Original version carries up to 4 records per message.
- X.25 still uses the original version.
- Expanded-vs-original execution report is chosen in login message `L040` via `AP-CODE`: `3` original, `A` expanded.
- Expanded report data uses message format `R7`; startup/reply and connection confirmation/end messages remain compatible with original flow as specified.

Design implication:

- Treat second execution-report channels as duplicate/redundant delivery of the same business reports, not as partitioned order streams.
- Second execution-report channels as duplicate/redundant delivery must be de-duplicated by business keys, not treated as two independent streams.
- De-duplicate and reconcile by execution identifiers/sequence fields, not by channel alone.

## File Transfer And Second Route

From `O-108`:

- Original host connection allowed one file-transfer PVC/socket.
- Second file-transfer route allows two TCP/IP file-transfer socket sessions.
- It can also allow one X.25 file-transfer PVC plus one TCP/IP file-transfer socket, but new applications should use TCP/IP as principle.
- Two X.25 file-transfer PVCs are not allowed.
- Second route exists to improve timeliness, operational flexibility, route dispersion, and backup.
- After applying for two routes, route 1 sends and receives route 1 replies; route 2 sends and receives route 2 replies.
- Adding route 2 adds two sockets: file send and file receive.
- Broker can select route 1 or route 2 as the primary receive path for TWSE-initiated sending.
- `B37` changes the primary two-route FT receive path and takes effect the next business day.
- Route 2 inherits the same head/branch shared FT setting as route 1.

Design implication:

- Preserve route identity in logs and state machines.
- Reply matching must use the same route as the sent file.
- Do not assume route 2 changes business semantics; it changes transport and operational resilience.

## Backup And Failure Diagnosis

Use layered diagnosis:

| Symptom | Likely layer to inspect first |
| --- | --- |
| No quote packets or sequence gaps | Market-data multicast group, IGMP, telecom path, duplicate group comparison, feed handler sequence tracking |
| TCP socket connect fails | Broker router/firewall, Source IP/Source Port config, TWSE listener, line/VC, socket ID/password/function allocation |
| Connected but no TWSE message within 25 seconds | Socket session health, network components, TWSE hardware/software, heartbeat expectations |
| Repeated heartbeat/timeout errors | Network/firewall/router/session stability, AP inactivity versus true failure, SLM-030/SLM-040 handling |
| Execution reports appear duplicated | Expected if using second execution-report channel; de-duplicate business reports |
| File reply arrives on unexpected route | Check route 1/route 2 send-receive pairing and B37 primary receive-path setting |
| Main site failover | TWSE VC switch from main to backup; same host IP; broker still runs full-day backup checks |

Minimum observability for a professional broker system:

- Router/firewall interface errors, drops, session logs, and line status.
- TCP retransmission/reset/timeout metrics for socket sessions.
- Socket lifecycle logs: source IP/port, destination, SLM-010/020/030/040, close/rebuild reasons.
- AP-level startup notice, login, application startup, and logout/close records.
- Order acknowledgement, execution report, query, resend/recovery, and reconciliation logs.
- Market-data multicast packet counters, per-format sequence gaps, duplicate group health, HeartBeat format 16 status.
- Backup activation records, main/backup/test IP context, and reconciliation results.

## Answer Discipline

When answering architecture questions:

- Say which manual family applies before giving the conclusion.
- Use `TCP socket` only for host/FIX/order/report/file sessions.
- Use `IP multicast` for centralized-market real-time market data.
- Explain whether the question is about transport, message format, or business workflow.
- If the user asks "會不會掉包/漏訊", answer at both network and application layers: multicast can lose packets; TCP can retransmit but sessions can timeout/rebuild; business completeness relies on sequence/report/reconciliation controls.
- If the user asks for a diagram, include broker side, TWSE side, network type, and backup/test separation.
