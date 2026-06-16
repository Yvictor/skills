# Expert Self Exam

Use this exam before claiming the skill can answer professional Taiwan broker-exchange integration questions. These questions are deliberately phrased like an engineer or trading-system user would ask, not like a table lookup.

Passing standard:

- Answer must choose the correct manual family.
- Answer must distinguish transport, protocol/session, message format, and business workflow.
- Answer must include the implementation implication.
- If the question is about exact values, answer with the exact value and source manual/update date.

## Architecture And Transport

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| A01 | 跟交易所連線到底有沒有 multicast？ | Yes for centralized-market real-time market data; no evidence to use multicast for broker order-entry/host-connection workflows. | `O-126/O-127`, updated `115.05.15`; `O-105`, updated `104.12.09` |
| A02 | 行情也是 TCP 傳輸的嗎？ | The line/network is described as TCP/IP, but the real-time market-data feed uses IP multicast with duplicate multicast groups; it is not a TCP socket stream. | `O-126/O-127`, updated `115.05.15` |
| A03 | 下單和成交回報也是 multicast 嗎？ | No. Host/order/report/file workflows use socket/session style connectivity; broker is client and TWSE is server/listener for TCP/IP host sockets. | `O-105`, updated `104.12.09` |
| A04 | 為什麼行情接收端要看序號？ | Because TCP/IP broadcast/multicast delivery has no guaranteed delivery mechanism; sequence numbers let receivers check completeness. | `O-126/O-127`, updated `115.05.15` |
| A05 | 券商端防火牆放在哪裡？ | Dedicated IP trading network firewall between the broker dedicated router and the trading host. | `O-105`, updated `104.12.09` |
| A06 | 交易所端機房架構有哪些？ | Main data center, backup data center, and test data center. Main and backup each have two routers in backup/HA; test has one router. | `O-105`, updated `104.12.09` |
| A07 | 主機房切備援機房時券商要改 IP 嗎？ | Normally no. Main and backup hosts use the same IP; TWSE closes main VC and enables backup VC. Broker still performs full-day backup checks. | `O-105`, updated `104.12.09`; `O-104`, updated `115.03.13` |
| A08 | 測試機房是不是跟正式主備用同一個 IP？ | No. Test data center uses different IPs; broker must use test IPs for testing. | `O-105`, updated `104.12.09` |

## Socket, Session, And Recovery

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| S01 | Socket 是怎麼被交易所辨識的？ | By `Source IP + Source Port Number`; the same combination can establish only one session. | `O-105`, updated `104.12.09` |
| S02 | 同一個 Source IP + Source Port 又重連會怎樣？ | It is treated as socket session reconstruction; the original session is terminated and its function is interrupted. | `O-105`, updated `104.12.09` |
| S03 | 一個 Socket 可以同時下單又收成交回報嗎？ | No. Each socket performs one function; different functions use different sockets and source ports. | `O-105`, updated `104.12.09` |
| S04 | TMP 在 TCP byte stream 上怎麼切訊息？ | Socket layer wraps TMP with header/trailer into SLM so receiver can separate messages, then strips SLM wrapper back to TMP for AP. | `O-105`, updated `104.12.09` |
| S05 | connect 後多久沒收到交易所訊息要處理？ | Broker waits 25 seconds for TWSE accept/error/no-message handling; no message leads to close/rebuild handling. | `O-105`, updated `104.12.09` |
| S06 | 多久沒有 AP 訊息時券商要送 heartbeat？ | If no AP TMP message needs sending for 60 seconds after the previous socket message, send connection-confirmation/heartbeat SLM. | `O-105`, updated `104.12.09` |
| S07 | 收到交易所訊息後多久沒下一筆要重建？ | Broker waits 25 seconds; no TWSE message may indicate network/TWSE issue and should close and rebuild the session. | `O-105`, updated `104.12.09` |
| S08 | Socket 建好後 AP 馬上可以送業務訊息嗎？ | It should perform host connection subsystem startup notice, login, and application subsystem startup after each socket establishment. | `O-105`, updated `104.12.09` |

## Market Data

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| M01 | 普通股競價交易即時行情是格式幾？ | Format 6; transmission format code is PACK BCD `06`. | `O-126/O-127`, updated `115.05.15` |
| M02 | 格式十六是什麼？ | Centralized-market market-data system HeartBeat data. | `O-126/O-127`, updated `115.05.15` |
| M03 | 行情 HeartBeat 大約多久送一次？ | About every 30 seconds for format 16 during the specified transmission window. | `O-126/O-127`, updated `115.05.15` |
| M04 | HeartBeat 狀態 R 代表什麼？ | Restart of HeartBeat transmission after transmission abnormality; interrupted HeartBeat data is not retransmitted. | `O-126/O-127`, updated `115.05.15` |
| M05 | 第一 IP 股票即時行情 multicast group 是什麼？ | `224.0.100.100:10000` and `224.0.200.200:20000`. | `O-126/O-127`, updated `115.05.15` |
| M06 | 第二 IP 是股票還是權證？ | Call/put warrant real-time market data and securities basic data. | `O-126/O-127`, updated `115.05.15` |
| M07 | 第三 IP 傳什麼？ | Stock and call/put warrant 5-second snapshot data plus securities basic data. | `O-126/O-127`, updated `115.05.15` |
| M08 | 行情 receiver 要不要 IGMP？ | Yes. Recipient needs IGMP-capable router/switch-router connected to the IP market-data transmission network. | `O-126/O-127`, updated `115.05.15` |

## FIX And Host Protocol Boundaries

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| F01 | FIX 是不是行情 feed？ | No. FIX is an order/session protocol surface; market-data multicast is specified by `O-126/O-127`. | `O-124/O-125`; `O-126/O-127` |
| F02 | TWSE 集中市場 FIX TargetCompID 是什麼？ | `XTAI`; TPEx is `ROCO`. | `O-124/O-125` |
| F03 | FIX SenderCompID 怎麼組？ | For broker-to-TWSE, it represents market + broker ID + FIX Socket ID. | `O-124/O-125` |
| F04 | FIX TargetSubID 的一般交易、盤後零股、盤後定價、盤中零股是什麼？ | `0`, `2`, `7`, `C`. | `O-124/O-125` |
| F05 | FIX tag 問題可以只靠這份摘要回答嗎？ | No. Reopen FIX manual for exact tag numbers, values, and session rules. | `O-124/O-125` |

## Execution Reports, File Transfer, And Redundancy

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| R01 | 第二成交回報通道兩路內容是不是切分？ | No. Two channels carry the same report content; treat as duplicate/redundant delivery. | `O-107`, updated `104.12.09` |
| R02 | 可以申請兩個 TCP/IP 成交回報 Socket Session 嗎？ | Yes. | `O-107`, updated `104.12.09` |
| R03 | 可以申請兩個 X.25 成交回報 PVC 嗎？ | No. | `O-107`, updated `104.12.09` |
| R04 | 擴充版成交回報一筆訊息最多幾筆成交資料？ | Up to 48 records; original version up to 4. | `O-107`, updated `104.12.09` |
| R05 | 成交回報原始版/擴充版怎麼選？ | In connection subsystem login message `L040`, `AP-CODE` `3` means original, `A` means expanded. | `O-107`, updated `104.12.09` |
| R06 | 第二路檔傳後，第一路送的資料可不可以第二路收回覆？ | No. Basic rule is route 1 send route 1 receive, route 2 send route 2 receive. | `O-108`, updated `104.12.09` |
| R07 | 第二路檔傳新增幾個 socket？ | Two sockets: file send and file receive. | `O-108`, updated `104.12.09` |
| R08 | B37 是做什麼？ | Declares/changes the primary receive path for two-route file transfer, effective next business day. | `O-108`, updated `104.12.09` |

## Failure And Monitoring Scenarios

| ID | Question | Expected answer | Source |
| --- | --- | --- | --- |
| X01 | 行情少一段資料時先看什麼？ | Multicast group reception, IGMP/network path, duplicate group comparison, per-format sequence numbers, and feed handler logs. | `O-126/O-127` |
| X02 | TCP socket 連不上先看什麼？ | Broker dedicated router/firewall, line/VC, source IP/port configuration, TWSE listener, socket ID/password/function allocation. | `O-105` |
| X03 | 25 秒沒有交易所訊息代表什麼？ | Could indicate network component or TWSE hardware/software issue; close and rebuild the socket session per flow. | `O-105` |
| X04 | 主機房切備援後還要做什麼？ | Broker does not change line/IP, but must follow full-day backup query/check procedures. | `O-105/O-104` |
| X05 | 看到重複成交回報一定是錯嗎？ | Not necessarily. With second execution-report channel, duplicate business content is expected; system should de-duplicate and reconcile. | `O-107` |
| X06 | 檔案回覆路徑不對可能是哪裡錯？ | Route 1/route 2 send-receive pairing or B37 primary receive-path configuration. | `O-108` |

## Spot-Check Prompts

These prompts are good final validation prompts because they expose whether the answer is integrated rather than copied:

- 「行情也是用 TCP 傳輸的嗎？你要確定。」
- 「交易所跟券商的主機連線跟即時行情傳輸差在哪？」
- 「如果 Source IP/Port 重複建 socket，交易所會怎麼看？」
- 「兩路成交回報是不是一邊一半？」
- 「主機房切備援，券商系統要改 IP 嗎？」
- 「第二路檔傳是 active-active 嗎？回覆會走哪一路？」
- 「行情掉包要怎麼偵測，跟 TCP retransmission 是同一件事嗎？」
- 「FIX 的 TargetSubID 跟 TMP 的 AP-CODE 有什麼關係？」

## Whole-Manual Coverage Prompts

Use these prompts to verify the agent has the whole manual set in its mental model, not only connectivity.

| ID | Manual | Prompt | Expected routing answer |
| --- | --- | --- | --- |
| W01 | O-010 | 客戶交割失敗算一般下單錯誤嗎？ | Route to ordinary/credit default handling, not order reject or error-account correction. |
| W02 | O-016 | 我要吃每日統計檔，該看行情 multicast 嗎？ | Route to statistics/report file manual, not real-time market data. |
| W03 | O-126 | 股票即時行情格式和傳輸方式怎麼判斷？ | Route to market-data spec: format 6 and IP multicast. |
| W04 | O-127 | 英文實作團隊要確認行情架構，看哪本？ | Use English market information specification as cross-check. |
| W05 | O-101 | AP 開機通知、登錄、啟動這類主機流程看哪本？ | Route to main host connection manual. |
| W06 | O-001 | 一般交易委託、回報、取消減量查詢看哪本？ | Route to regular trading manual. |
| W07 | O-104 | 主機房切備援後要做全量檢核看哪本？ | Route to full-day backup manual. |
| W08 | O-021 | 借券後台結算/管理看哪本？ | Route to SBL back-office manual. |
| W09 | O-027 | 證券業務借貸款項是不是借券？ | No; route to money-lending operations, not SBL. |
| W10 | O-007 | 融資融券、信用交易檔案看哪本？ | Route to credit/margin trading manual. |
| W11 | O-026 | 權證/ETF 流動量提供者專線申報看哪本？ | Route to LP dedicated-line workflow. |
| W12 | O-125 | FIX 英文 tag/session 規格看哪本？ | Route to English FIX specification. |
| W13 | O-128 | 證券商備用競價設備怎麼用看哪本？ | Route to spare auction equipment manual. |
| W14 | O-008 | 投資人開戶資料交換看哪本？ | Route to investor account-opening computer workflow. |
| W15 | O-124 | FIX 中文規格、CompID/SubID 看哪本？ | Route to Chinese FIX 4.4 manual. |
| W16 | O-037 | 盤中零股看哪本？ | Route to intraday odd-lot manual. |
| W17 | O-002 | 盤後零股/零股交易看哪本？ | Route to after-hours odd-lot manual, not intraday odd-lot. |
| W18 | O-019 | 盤後定價 AP-CODE=7 這種問題看哪本？ | Route to after-hours fixed-price manual. |
| W19 | O-031 | 投信 ETF 端申購買回看哪本？ | Route to investment-trust ETF manual. |
| W20 | O-030 | 證券商 ETF 作業看哪本？ | Route to broker ETF manual. |
| W21 | O-020 | 有價證券借貸前台看哪本？ | Route to SBL front-office manual. |
| W22 | O-022 | 證券商有價證券借貸制度看哪本？ | Route to broker SBL system manual. |
| W23 | O-011 | 補正借券是一般借券嗎？ | No; route to shortfall repair borrowing manual. |
| W24 | O-006 | 公開申購配售看哪本？ | Route to public subscription/allocation manual. |
| W25 | O-034 | ETN 發行人端看哪本？ | Route to ETN issuer-side platform manual. |
| W26 | O-033 | ETN 證券商端看哪本？ | Route to ETN broker-side platform manual. |
| W27 | O-038 | 股票造市者獎勵/月費折讓檔看哪本？ | Route to stock market maker/incentive participant manual. |
| W28 | O-035 | 流動量提供者報價規則看哪本？ | Route to LP quote-rule manual, not line declaration. |
| W29 | O-029 | 現股當沖短券缺口怎麼處理看哪本？ | Route to day-trading manual and then repair/lending manuals as needed. |
| W30 | O-036 | 聯徵中心負面資料查詢看哪本？ | Route to negative-data query manual. |
| W31 | O-121 | 借券相關資料查詢平台看哪本？ | Route to information-exchange platform SBL query manual. |
| W32 | O-024 | 證金標購看哪本？ | Route to securities-finance tender purchase manual. |
| W33 | O-004 | 標借看哪本？ | Route to tender borrowing manual, not generic SBL. |
| W34 | O-018 | 標購看哪本？ | Route to tender purchase manual. |
| W35 | O-005 | 上市證券拍賣看哪本？ | Route to auction manual. |
| W36 | O-012 | 借戶賣出股票申報看哪本？ | Route to borrower sell-stock declaration manual. |
| W37 | O-025 | 綜合交易帳號看哪本？ | Route to comprehensive trading account manual. |
| W38 | O-032 | 定期定額買賣看哪本？ | Route to DCA/periodic fixed-amount trading manual. |
| W39 | O-009 | 錯帳和更正帳號看哪本？ | Route to error-account/account-correction manual. |
| W40 | O-003 逐筆 | 鉅額逐筆交易看哪本？ | Route to sequential block-trading manual. |
| W41 | O-003 配對 | 鉅額配對交易看哪本？ | Route to paired block-trading manual. |
| W42 | O-013 | 證券商聯合徵信看哪本？ | Route to joint credit information manual. |
| W43 | O-108 | 第二路檔案傳輸看哪本？ | Route to second file-transfer manual. |
| W44 | O-107 | 第二成交回報和擴充版成交回報看哪本？ | Route to second execution-report/expanded report manual. |
| W45 | O-106 | 資訊交換平台主機連線看哪本？ | Route to information-exchange platform host connection manual. |
| W46 | O-105 | Source IP/Port、socket heartbeat、防火牆架構看哪本？ | Route to TCP/IP host connection manual. |
| W47 | O-023 | 證金議借看哪本？ | Route to securities-finance negotiated lending manual. |
| W48 | O-028 | 客戶委託保管及運用款項看哪本？ | Route to customer entrusted fund custody/use operations manual. |
