# Taiwan Stock Rule Cards

Use these cards as the first answer surface for common Taiwan stock market and broker-system questions. Each card is synthesized from the TWSE broker manuals and points to the source manual for verification.

## Card 1: Classify The Question Before Answering

Every question should be classified across five axes:

| Axis | Values to identify | Why it matters |
|---|---|---|
| Market segment | regular, intraday odd lot, after-hours odd lot, after-hours fixed price, block, auction, subscription, ETF/ETN platform, securities lending, default/error workflow | Determines accepted operations, price/quantity rules, report files, and session. |
| Actor/account | investor, broker, dealer, comprehensive account, margin/short account, SBL account, issuer, liquidity provider, market maker | Account restrictions and file responsibilities differ. |
| Lifecycle stage | order input, acknowledgement, reduction, cancellation, query, execution report, file declaration, reconciliation, repair | Do not treat post-trade declarations as orders. |
| Protocol | broker operation file/message, FIX, TCP/IP, market data, backup system | Exact field names and sessions come from different manuals. |
| Risk/exception | price/quantity validation, credit/short sale, total order cap, day-trade shortfall, error account, default | Controls often span multiple manuals. |

Rule of thumb: If the user asks "can I trade/order X?", answer with market segment + account + product + lifecycle. If the user asks "what do I send?", answer with protocol + message/file + source manual.

Source model: `O-001`, `O-002`, `O-003`, `O-007`, `O-009`, `O-010`, `O-019`, `O-029`, `O-037`, `O-124`, `O-125`, `O-126`, `O-127`.

## Card 2: Intraday Odd Lot Is Its Own Market Segment

Do not implement intraday odd-lot trading as "regular trading with small quantity."

Synthesized rule:

- Intraday odd lot has a dedicated operation context and includes order input/reporting, single-message/report-file receiving, and execution report handling.
- Supported order workflow includes buy, sell, reduction, cancellation, query, and acknowledgement.
- Intraday odd-lot tradable-security price data and same-day volume/value reports are actively sent by TWSE.
- Intraday odd-lot execution reports are merged into the ordinary same-day execution-report flow.
- Broker order numbers must be sequential/unique in context, with a corresponding order ticket.
- If broker total order/self-trade application amount exceeds 20x available net funds across regular, after-hours fixed-price, intraday odd lot, and after-hours odd lot, TWSE may stop buy/sell input and allow only cancellation, reduction, and query.

Implementation implication:

- Use a separate `INTRADAY_ODD_LOT` segment.
- Reconcile special odd-lot reports plus ordinary execution reports.
- Include total order amount controls across multiple segments.

Source: `O-037-A10 TWSE盤中零股交易電腦作業手冊`, updated `114.05.05`.

## Card 3: After-Hours Fixed-Price Trading Has Special Order Semantics

After-hours fixed-price trading is a separate subsystem, not regular trading after 13:30.

Synthesized rule:

- Broker systems connect to the after-hours fixed-price subsystem through connection subsystem function `AP-CODE = 7`.
- After close, input buy/sell declarations are matched immediately by the after-hours fixed-price process and execution reports are merged into the general execution-report protocol.
- Supported functions include buy, sell, query, reduction, cancellation, acknowledgement, connection confirmation, reconnect query, and aggregate order-quantity query.
- In the cited input message, `PRICE` must be `0`, while `PRICE-TYPE` is limit (`2`) and `TIME-IN-FORCE` is ROD (`0`).
- Quantity must be greater than 0 and at most 499 in the cited message; reduction quantity is the quantity to reduce.
- `ORDER-TYPE` distinguishes ordinary, margin purchase, short sale, and securities borrowing/short-sale categories.
- Errors include duplicate order number, quantity limit, total order amount cap, short/borrow restrictions when after-hours price is below reference price, and dealer trading restriction when after-hours price is limit-up/limit-down.

Implementation implication:

- Use a separate `AFTER_HOURS_FIXED_PRICE` segment.
- Do not expose user-entered arbitrary price unless the current rule and API path support it; the broker message may use `PRICE = 0`.
- Keep order-source markers: ordinary, automated device, DMA, internet, voice, API.
- Treat after-hours fixed-price short sale / borrowing rules as separate validations.

Source: `O-019-A10 盤後定價交易電腦作業手冊`, updated `114.05.05`.

## Card 4: Day Trading Is A Reporting And Repair Workflow, Not Just An Order Flag

Day trading should be modeled beyond a front-end "day trade" checkbox.

Synthesized rule:

- The day-trade detail declaration workflow (`BC8`) is used for T/T+1/T+2 day-trade detail reporting.
- Brokers must declare same-day buy/sell day-trade amounts by 18:00 on trade day; the system closes automatically at 18:00.
- Brokers may adjust by adding/deleting through 18:00 on T+1 and until 10:00 on T+2.
- Day-trade detail packages are grouped by day-trade start/end classification, investor account, security, buy/sell day-trade details and amounts; each package has a transaction sequence count limit of 8000.
- Within each package, buy/sell day-trade quantities must match.
- Day trading applies to ordinary trading and after-hours fixed-price trading. If the security is only eligible for buy-first-sell-later day trading, after-hours fixed-price trading is sell-only for that day-trade purpose.
- If a day-trade account/security has no declared day-trade amount, it is treated as no day-trade amount to declare.
- If a broker needs to report an error account or account correction for a day-trade position, it must cancel the relevant day-trade declaration first, except default handling uses post-offset amounts.
- After T+2 10:00, brokers can report error account only for the post-offset day-trade difference and cannot report account correction for already-declared day-trade data.
- Comprehensive trading accounts cannot be used for securities day trading, including allocated trades and account-corrected allocated trades.

Implementation implication:

- Separate order intent from `BC8` day-trade detail declaration.
- Track T/T+1/T+2 cutoffs.
- Add package-size checks and buy/sell quantity balancing.
- Model day-trade repair paths separately from normal order correction.

Source: `O-029-A10 現股當日沖銷交易電腦作業手冊`, updated `109.10.12`.

## Card 5: Sell-First Day Trade Shortfall Becomes A Securities Repair Workflow

If a sell-first day trade is not bought back, it enters a securities delivery repair domain.

Synthesized rule:

- If an investor sells first but does not buy in during the day, does not change transaction category to margin short/securities borrowing sale, and has no inventory for settlement, the broker must use a T+1 trading-time buyback through broker head-office account for T+3 return declaration.
- The broker must declare the shortfall occurrence by 18:00 on trade day.
- If the T-day shortfall remains unresolved and T+2 settlement cannot be completed, the "應付當沖交割券差申報平台" is used to support T+2 settlement.
- The broker is the lending contract subject in this platform and must establish a special account for securities transfer.
- Investor-lent securities must be moved into the broker special account before being transferred to the borrower.
- If lender and borrower are at different brokers, both brokers must declare matching special-account securities information.
- Follow-up transfer/return declaration can proceed only after TWSE correct notification, with error code `"00"` in the cited text.
- Other than dealers, all securities firms can borrow from investors and lend to investors without qualification restrictions in this platform.
- When using this platform for day-trade settlement shortfall, transaction category remains cash/spot (`委託類別 0`); T+1 buyback through the special account and later processing declarations still apply.

Implementation implication:

- Represent sell-first day-trade shortfall as a state machine: occurrence -> declaration -> borrow/transfer matching -> TWSE/TDCC reply -> buyback/return.
- Do not automatically convert the order to margin short or securities borrowing sale unless the required category-change workflow happened.

Source: `O-029-A10 現股當日沖銷交易電腦作業手冊`, updated `109.10.12`.

## Card 6: Error Account And Account Correction Are Different Workflows

Do not merge error-account processing with account correction.

Synthesized rule:

- Error account (`錯帳`) requires an error category and must leave account-correction reason blank.
- Error categories distinguish broker-attributable errors (`1` stock code, `2` quantity, `3` price, `4` buy/sell reversal, `5` other) and investor-attributable errors (`A` stock code, `B` quantity, `C` price, `D` buy/sell reversal, `E` other).
- Error-account reporting can be partial or can cover all executions under an order number.
- If total execution sequence is `0`, it means the whole order number's execution data is reported as error account.
- Error-account quantity plus offset quantity must not exceed original executed quantity.
- Proprietary securities used for settlement must not exceed error-account quantity.
- Account correction (`更正帳號`) requires error category blank and account-correction reason nonblank.
- Account correction is not error account; do not enter error quantity, offset quantity, error category, proprietary settlement fields, order type, or execution price.
- Account correction must be reported by order number for all execution data under that order number using total execution sequence `0`.
- Declaration dates can be T, T+1, or T+2 for ordinary cases; delayed settlement uses T+2 or T+3.
- For same securities group trades in the same stock, error buys and sells can offset; offset portion is declaration-only and does not require cover processing, while the remainder still requires declaration and cover handling.
- Error/account-correction file transmissions have a 10-send limit for the declaration and processing files in the cited text; normal processing must wait for TWSE error reply before sending another batch and repeat until the reply indicates all correct.

Implementation implication:

- Use separate models: `ErrorTradeReport` and `AccountCorrectionReport`.
- Validate mutually exclusive fields.
- Implement retry based on TWSE error reply files, not blind resubmission.

Source: `O-009-A10 錯帳及更正帳號電腦作業手冊`, updated `108.05.21`.

## Card 7: Default Handling Is A Settlement Exception Workflow

Default handling is separate from order rejection and error-account correction.

Synthesized rule:

- The ordinary/credit default manual covers ordinary default, credit default, default offset data, default handling declaration, declaration detail queries, and default announcement/receiving files.
- Treat default handling as a post-trade settlement/legal exception flow.
- Block-trade and agency/default announcement workflows may have separate file families.
- Return/error files must be checked after default file send/receive operations.

Implementation implication:

- Use a dedicated `DefaultCase` workflow with ordinary/credit/default-type classification.
- Do not represent default as a failed order status.
- Keep default declarations, offsets, handling declarations, and announcement receiving as separate events.

Source: `O-010-A10 普通違約及信用違約電腦作業手冊`, updated `115.06.01`.

## Card 8: ETF, ETN, Liquidity Provider, And Market Maker Are Different Actor Workflows

Do not answer product questions without identifying the actor.

Synthesized rule:

- ETF has broker-side and investment-trust/issuer-side manuals.
- ETN has broker-side and issuer-side manuals.
- ETN issuer workflows include basic subscription/redemption data declaration/query, lock-position query, detail summary query, actual T-day amount declaration/query, confirmation files, receivable/payable files, inventory units for market making, and quote-exemption date declaration/query.
- Warrant/ETF liquidity-provider dedicated line workflows include declaration and query, not quote-pricing logic.
- ETF liquidity-provider dedicated lines are constrained to FIX lines in the cited error rules.
- Stock market maker / trading incentive participant manuals cover performance file and monthly fee-rebate file queries, including innovation-board market maker files; they are not general market-making order-entry manuals.

Implementation implication:

- Classify by actor first: broker, issuer/investment trust, liquidity provider, market maker, investor.
- Classify by workflow second: trading, subscription/redemption, line declaration, quote-exemption, performance/rebate reporting.

Sources: `O-030` and `O-031` updated `114.01.17`; `O-033` and `O-034` updated `112.12.20`; `O-026` updated `114.12.15`; `O-038` updated `111.08.12`.

## Card 9: FIX And Market Data Are Protocol Layers, Not Trading Rules

Do not treat FIX manuals or market-data specs as substitutes for market-segment rules.

Synthesized rule:

- FIX 4.4 describes protocol tags, values, sessions, acknowledgements, and rejects for order/routing workflows.
- Market information specs describe versioned market-data message contracts, not order entry.
- Host connection manuals describe infrastructure state and file/message connectivity, not product eligibility.
- Backup and second-channel manuals describe continuity/recovery paths, not primary trading semantics.
- Common market-data lookup: 集中市場普通股競價交易即時行情資訊 is 格式六; its packet transmission format code is PACK BCD `06`.

Implementation implication:

- Validate market segment, account/product eligibility, price type, and time-in-force before building FIX messages.
- Pin market-data parser implementation to the spec version, e.g. B.12.13 in the current `O-126/O-127` specs.
- Keep connection/session state separate from order state.
- Make reconnect/recovery idempotent.

Sources: `O-124` updated `114.05.05`; `O-125` updated `114.09.03`; `O-126/O-127` updated `115.05.15`; `O-101` updated `115.03.16`.

## Card 10: Always Distinguish Operational Evidence From Current Legal Rule

These manuals are strong evidence for broker system operations and message/file handling. They are not always enough for a current legal/compliance answer.

Use this response pattern for high-stakes questions:

> Based on the TWSE broker operation manual, broker systems should treat this as ... Source: `<manual>`, updated `<date>`. For production or legal compliance, verify against current TWSE rules/circulars because the manual is an operational snapshot.

Implementation implication:

- Include `source_manual`, `source_updated`, and `verified_at` fields in internal rule objects.
- Do not hard-code rules without source and update date.
