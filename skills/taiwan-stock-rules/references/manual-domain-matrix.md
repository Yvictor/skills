# Manual Domain Matrix

Use this file when the user asks broad "do you understand the whole TWSE broker manual set?" questions or when a question could belong to more than one workflow. This is the all-source-manual coverage matrix: every downloaded source manual is represented here as a role in the broker-exchange mental model.

The matrix does not replace exact source lookup. It tells the agent which manual family owns the concept, what not to confuse it with, and which synthesized reference to open next.

## Whole-System Mental Model

Think of a broker system as these cooperating domains:

1. **Market/order domains** decide what business action is being sent: regular, odd-lot, after-hours, block, auction, subscription, DCA, ETF/ETN, lending, tender, default repair.
2. **Account/risk domains** decide whether the actor/account is eligible: investor account, comprehensive account, credit account, negative data, default status, liquidity provider, market maker, issuer.
3. **Post-trade/repair domains** handle facts after execution: execution reports, error accounts, account correction, day-trade shortfall, borrowing/procurement, default, settlement repair.
4. **Protocol/transport domains** decide how data moves: host TMP/socket, FIX, file transfer, second channels, market-data multicast, backup systems.
5. **Reference/report domains** provide state proof: statistics files, query/report files, TWSE correct/error replies, market-data formats, backup checks.

When answering, identify the domain owner first. Do not answer "借券" or "違約" from the general trading manual; route to the specific repair/risk manual.

## Manual Coverage Matrix

| # | Manual | Expert role | Do not confuse with | Next reference |
| --- | --- | --- | --- | --- |
| 1 | O-010-A10 普通違約及信用違約電腦作業手冊 | Ordinary and credit-default declaration, query, offset, and handling lifecycle after settlement failure. | Order rejection, error-account correction, or day-trade shortfall. | `accounts-settlement-and-exceptions.md` |
| 2 | O-016-A10 各類資訊統計檔案電腦作業手冊 | Statistical/report file formats for daily operational evidence and ingestion. | Real-time market data or order-entry messages. | `protocols-and-market-data.md` |
| 3 | O-126-A10 TWSE集中市場即時交易資訊傳輸規格書(B.12.13)(202612) | Chinese source for centralized-market real-time market-data formats, multicast transport, PACK BCD, sequence numbers, and feed lines. | TCP host sockets, FIX, or legal trading rules. | `market-data-format-cards.md`, `broker-exchange-integration.md` |
| 4 | O-127-A10 Market Information Specification(B.12.13)(行情資訊傳輸作業手冊英文版)(202612) | English cross-check for market-data transmission architecture and format terms. | Order routing or execution reports. | `market-data-format-cards.md`, `broker-exchange-integration.md` |
| 5 | O-101-A10 主機連線電腦作業手冊 | Main host connection framework: connection subsystem, single-message/file-transfer, AP startup/login, broker-host lifecycle. | Market-data multicast or FIX tag details. | `broker-exchange-integration.md`, `protocols-and-market-data.md` |
| 6 | O-001-A10 一般交易電腦作業手冊 | Base regular-trading order, acknowledgement, execution-report, cancel/reduction/query, and ordinary market workflow. | Odd-lot, block, after-hours, or post-trade repair workflows. | `trading-markets.md` |
| 7 | O-104-A10 集中市場當日全量備援電腦作業手冊 | Full-day backup checks and operational reconciliation after backup activation. | Ordinary line backup or second execution-report channel. | `broker-exchange-integration.md` |
| 8 | O-021-A10 有價證券借貸後檯電腦作業手冊 | Securities lending back-office administration, settlement, and reconciliation. | Front-office lending or tender borrowing. | `financing-lending-and-shortfall.md` |
| 9 | O-027-A10 證券業務借貸款項電腦作業手冊 | Broker money-lending business operations. | Securities lending, margin financing, or tender borrow. | `financing-lending-and-shortfall.md` |
| 10 | O-007-A10 信用交易電腦作業手冊 | Margin purchase, short sale, credit trading controls, credit files/reports. | Securities lending or day-trade shortfall repair. | `financing-lending-and-shortfall.md` |
| 11 | O-026-A10 權證暨ETF流動量提供者專用電腦作業手冊 | Warrant/ETF liquidity-provider dedicated line declaration/query and related operational errors. | Market-maker quoting rules or normal ETF order flow. | `products-liquidity-and-issuance.md` |
| 12 | O-125-A10 TWSE FIX 4.4 Specification (FIX 4.4電文規範作業手冊英文版) | English FIX 4.4 tags/session/order routing cross-check. | Market-data multicast or TMP files. | `broker-exchange-integration.md`, `protocols-and-market-data.md` |
| 13 | O-128-A10 證券商備用競價設備系統-證券商使用手冊 | Broker spare auction-equipment system usage and continuity operations. | Main IP trading network failover or full-day backup checks. | `broker-exchange-integration.md` |
| 14 | O-008-A10 投資人開戶電腦作業手冊 | Investor account-opening computer workflows, broker account data exchange, validation, and files. | KYC/legal advice or trading account permissions without current compliance checks. | `accounts-settlement-and-exceptions.md` |
| 15 | O-124-A10 FIX4.4電文規範作業手冊 | Chinese FIX 4.4 specification: FIX session/message semantics, CompID/SubID, board routing. | Host TMP socket wrapper or market-data feed. | `broker-exchange-integration.md`, `protocols-and-market-data.md` |
| 16 | O-037-A10 TWSE盤中零股交易電腦作業手冊 | Intraday odd-lot order/report/query workflow and related files. | After-hours odd-lot or regular trading with smaller quantity. | `trading-markets.md` |
| 17 | O-002-A10 零股交易電腦作業手冊 | After-hours odd-lot trading workflow. | Intraday odd-lot. | `trading-markets.md` |
| 18 | O-019-A10 盤後定價交易電腦作業手冊 | After-hours fixed-price trading connection, order, query, reduction/cancel, and execution-report workflow. | After-hours odd-lot or regular continuous trading. | `trading-markets.md` |
| 19 | O-031-A10 投信ETF電腦作業手冊 | ETF investment-trust/issuer-side workflows. | Broker-side ETF workflows or ETN issuer workflows. | `products-liquidity-and-issuance.md` |
| 20 | O-030-A10 證券商ETF電腦作業手冊 | Broker-side ETF creation/redemption/trading-related operational files. | Investment-trust ETF workflows or ETN workflows. | `products-liquidity-and-issuance.md` |
| 21 | O-020-A10 有價證券借貸前檯電腦作業手冊 | Securities lending front-office participant workflows. | Lending back office or tender borrowing. | `financing-lending-and-shortfall.md` |
| 22 | O-022-A10 證券商有價證券借貸制度電腦作業手冊 | Broker securities-lending system operations. | General SBL front/back office or money lending. | `financing-lending-and-shortfall.md` |
| 23 | O-011-A10 補正借券電腦作業手冊 | Borrowing to correct/repair securities shortfall. | Ordinary securities lending or tender borrowing. | `financing-lending-and-shortfall.md` |
| 24 | O-006-A10 公開申購配售電腦作業手冊 | Public subscription/allocation workflows and broker files. | Auction, ordinary order book, or ETF subscription/redemption. | `trading-markets.md` |
| 25 | O-034-A10 ETN申購賣回平台--發行人端電腦作業手冊 | ETN issuer-side subscription/redemption platform operations. | ETN broker-side or ETF issuer workflows. | `products-liquidity-and-issuance.md` |
| 26 | O-033-A10 ETN申購賣回平台--證券商端電腦作業手冊 | ETN broker-side subscription/redemption platform operations. | ETN issuer-side or ETF broker workflows. | `products-liquidity-and-issuance.md` |
| 27 | O-038-A10 股票造市者及交易獎勵參與者電腦作業手冊 | Stock market maker/trading incentive participant reporting, performance, and rebate files. | Liquidity-provider quote-rule manual or ordinary market making theory. | `products-liquidity-and-issuance.md` |
| 28 | O-035-A10 流動量提供者報價規則電腦作業手冊 | Liquidity-provider quote-rule operational constraints. | Liquidity-provider line declaration in O-026. | `products-liquidity-and-issuance.md` |
| 29 | O-029-A10 現股當日沖銷交易電腦作業手冊 | Day-trading detail declaration, query, buy-first/sell-first handling, and shortfall repair routing. | A simple order flag or ordinary securities lending. | `financing-lending-and-shortfall.md` |
| 30 | O-036-A10 聯徵中心負面資料查詢電腦作業手冊 | Negative-data query workflow for broker risk controls. | Account opening or trading eligibility law. | `accounts-settlement-and-exceptions.md` |
| 31 | O-121-A10資訊交換平台有價證券借貸相關資料查詢作業手冊 | Information-exchange platform queries for securities lending data. | SBL transaction workflow itself. | `financing-lending-and-shortfall.md`, `protocols-and-market-data.md` |
| 32 | O-024-A10 證金標購電腦作業手冊 | Securities-finance tender purchase workflow. | Exchange tender purchase or securities lending. | `financing-lending-and-shortfall.md` |
| 33 | O-004-A10 標借電腦作業手冊 | Tender borrowing workflow used for securities procurement/settlement repair. | Securities lending front office, 補正借券, or 標購. | `financing-lending-and-shortfall.md` |
| 34 | O-018-A10 標購電腦作業手冊 | Tender purchase workflow. | Tender borrowing or securities-finance tender purchase. | `financing-lending-and-shortfall.md` |
| 35 | O-005-A10 上市證券拍賣電腦作業手冊 | Listed securities auction workflow. | Public subscription or block trading. | `trading-markets.md` |
| 36 | O-012-A10 借戶賣出股票申報電腦作業手冊 | Borrower selling stock declaration workflow. | Ordinary short sale, securities lending contract, or day-trade shortfall. | `financing-lending-and-shortfall.md` |
| 37 | O-025-A10 綜合交易帳號電腦作業手冊 | Comprehensive trading account operations and restrictions. | Ordinary investor account or omnibus concept without manual constraints. | `accounts-settlement-and-exceptions.md` |
| 38 | O-032-A10 證券商受託辦理定期定額買賣有價證券業務 | Broker periodic fixed-amount/DCA trading operations. | Ordinary single order or public subscription. | `trading-markets.md` |
| 39 | O-009-A10 錯帳及更正帳號電腦作業手冊 | Error-account declaration, account correction, delayed settlement, and block/spread error repair. | Default handling or order modification. | `accounts-settlement-and-exceptions.md` |
| 40 | O-003-A10 鉅額逐筆交易電腦作業手冊 | Block trading by sequential/逐筆 method. | Paired/matched block trading or regular trading. | `trading-markets.md` |
| 41 | O-003-A10 鉅額配對交易電腦作業手冊 | Block trading by paired/matched method. | Sequential block trading. | `trading-markets.md` |
| 42 | O-013-A10 證券商聯合徵信電腦作業手冊 | Joint credit information workflow for broker risk controls. | Negative-data center query or investor account opening. | `accounts-settlement-and-exceptions.md` |
| 43 | O-108-A10 第二路檔案傳輸電腦作業手冊 | Second file-transfer route, send/receive pairing, primary receive path, and route resilience. | Second execution-report channel. | `broker-exchange-integration.md` |
| 44 | O-107-A10 證券商申請第二成交回報通道及TCPIP網路擴充版成交回報電腦作業手冊 | Second execution-report channel and expanded execution-report format. | File-transfer route 2 or market-data duplicate multicast groups. | `broker-exchange-integration.md` |
| 45 | O-106-A10 資訊交換平台主機連線電腦作業手冊 | Information-exchange platform host connection. | Main broker host connection or market-data feed. | `protocols-and-market-data.md` |
| 46 | O-105-A10 TCPIP網路主機連線電腦作業手冊 | IP trading network, broker router/firewall, socket layer, heartbeat, failover, and source IP/port session identity. | Market-data multicast or business trading rules. | `broker-exchange-integration.md` |
| 47 | O-023-A10 證金議借交易電腦作業手冊 | Securities-finance negotiated lending workflow. | Tender borrowing, tender purchase, or ordinary SBL. | `financing-lending-and-shortfall.md` |
| 48 | O-028-A10-「證券商辦理客戶委託保管及運用其款項操作辦法」之電腦作業手冊 | Customer entrusted fund custody/use operations. | Trading settlement, margin financing, or money lending. | `accounts-settlement-and-exceptions.md` |

## Routing Heuristics For Ambiguous Chinese Terms

| User term | First interpretation check |
| --- | --- |
| 違約 | Ordinary/credit default in `O-010`; not an order reject. |
| 借券 | Could mean SBL front office/back office, broker SBL system, 補正借券, 標借, borrower sell declaration, or day-trade shortfall. Ask/route by lifecycle. |
| 開戶 | Investor account-opening files in `O-008`; do not answer compliance/KYC from this alone. |
| 標借 | Tender borrowing `O-004`; do not confuse with 標購 `O-018` or 證金標購 `O-024`. |
| 信用 | Margin/short sale `O-007` unless the context is credit default `O-010` or joint credit data `O-013`. |
| 造市/流動量 | Market maker/incentive reports `O-038`, quote rules `O-035`, or LP dedicated-line declaration `O-026` depending on actor/action. |
| 備援 | IP trading network failover `O-105`, full-day backup `O-104`, spare auction system `O-128`, second report channel `O-107`, or second FT route `O-108`. |
