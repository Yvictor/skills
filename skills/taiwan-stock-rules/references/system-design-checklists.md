# System Design Checklists For Taiwan Stock Rules

Use these checklists when building or reviewing code that implements Taiwan stock market workflows.

## Order Entry Checklist

- Market segment is explicit: regular, intraday odd lot, after-hours odd lot, after-hours fixed price, block, auction, subscription, ETF/ETN platform, or other.
- Actor is explicit: investor, broker, dealer/proprietary, comprehensive account, issuer, liquidity provider, market maker.
- Account permissions are checked before order construction.
- Product eligibility is checked before order construction.
- Quantity unit and price unit are taken from the relevant manual.
- Price type and time-in-force are validated for the segment.
- Order source/channel indicator is preserved when required.
- Broker order number / request id uniqueness is enforced.
- Cancellation, reduction, query, and new order are separate operations.
- Return/error acknowledgements are stored and interpreted.
- Execution reports are reconciled against accepted orders.

## Post-Trade And Settlement Checklist

- Trade date and settlement date are explicit.
- T/T+1/T+2/T+3 references are not collapsed.
- Error-account, account-correction, delayed-settlement, day-trade shortfall, and default workflows are separate state machines.
- Repair declarations have their own message/file codes.
- Correct/error replies are required before downstream processing.
- Offsets, proprietary securities used for settlement, and buy-in/borrow paths are represented explicitly.
- Audit trail includes original trade, repair action, TWSE response, and final status.

## Credit, Day Trading, And Lending Checklist

- Cash, margin purchase, short sale, securities borrowing, securities lending, and money lending are distinct concepts.
- Day trading is not just an order flag; it has detail reporting and shortfall workflows.
- Buy-first-sell-later and sell-first-buy-later are distinct for day trading.
- Securities shortfall workflows distinguish broker internal lending, investor lending, securities finance company borrowing, tender borrow, tender purchase, and negotiated lending.
- Comprehensive trading account restrictions are checked.
- Source manual is cited for each rule.

## Product-Specific Checklist

- ETF broker workflows and investment-trust/issuer workflows are separate.
- ETN broker-side and issuer-side workflows are separate.
- Liquidity-provider line declarations are separate from quote/pricing rules.
- Market maker performance/rebate files are reporting workflows.
- Warrant, ETF, ETN, market maker, and liquidity-provider terms are not used interchangeably.

## Protocol Checklist

- Protocol family is identified: broker operation files/messages, host connection, FIX, market data, second report channel, backup system.
- Version is pinned.
- Transport model is explicit: host/order/report/FIX connectivity uses TCP/IP socket/session manuals; centralized-market real-time market data uses IP multicast per `O-126/O-127`.
- Market-data receiver design includes IGMP-capable network equipment, multicast group/port configuration, duplicate multicast groups per channel, sequence-gap detection, and recovery/reconciliation behavior.
- Field names and code values are copied from source text, not paraphrased.
- Message/file layout tests include length, padding, date/time format, numeric units, and encoding.
- Reconnect/replay behavior is explicit and idempotent.
- Production implementation links to exact manual title and update date.

## Answer Review Checklist

Before responding to a user:

- Did you use synthesized references first?
- Did you open extracted text for exact numbers, fields, or edge cases?
- Did you cite manual title and update date?
- Did you distinguish legal/current-rule uncertainty from broker-operation evidence?
- Did you avoid presenting operational file rules as investor-facing legal rules?
