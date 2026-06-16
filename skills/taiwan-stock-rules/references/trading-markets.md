# Trading Markets And Order Workflows

This file synthesizes the trading-market manuals into a usable rule model. Use full extracted text for exact field names, error codes, or cutoff times.

## Market Segments

### Regular Trading

Regular trading is the base market workflow. The `O-001-A10 一般交易電腦作業手冊` describes order input, order acknowledgement, execution report handling, market-data support files, and operational notes for broker host connections.

System implications:

- Treat regular trading as the default segment only after checking whether the product/order belongs to a special segment.
- Implement order input, acknowledgement, execution report, cancellation/reduction/query, and reconciliation as separate states.
- Preserve channel/source markers such as ordinary, automated service equipment, DMA, internet, voice, or API order indicators where applicable.
- Validate price type, time-in-force, quantity, account, and order classification before sending the order.

Source: `O-001-A10 一般交易電腦作業手冊`, updated `115.03.13`.

### Intraday Odd Lot

Intraday odd-lot trading is not just regular trading with smaller quantity. It has a dedicated operation code and its own input/report workflow. The manual describes intraday odd-lot buy/sell, reduction, cancellation, query, acknowledgement, tradable-security price data, day volume/value data, and execution reports that are merged into ordinary execution reporting.

Important distinctions:

- It uses its own operation context (`盤中零股交易作業`) and dedicated files such as intraday odd-lot tradable securities/price data and day volume/value data.
- Broker systems should still reconcile executions with ordinary execution-report infrastructure when the manual says execution reports are merged.
- Total order amount controls can aggregate regular trading, after-hours fixed-price trading, intraday odd lot, and after-hours odd lot.

Source: `O-037-A10 TWSE盤中零股交易電腦作業手冊`, updated `114.05.05`.

### After-Hours Odd Lot

After-hours odd-lot trading is a separate odd-lot segment from intraday odd lot. Do not infer the workflow from intraday odd lot. Use `O-002` for order/report details, file names, quantities, and constraints.

System implications:

- Keep intraday odd-lot and after-hours odd-lot order validations separate.
- Check whether the user means "盤中零股" or older/after-hours "零股交易".

Source: `O-002-A10 零股交易電腦作業手冊`, updated `114.05.05`.

### After-Hours Fixed-Price Trading

After-hours fixed-price trading has its own connection context and order/report workflow. Broker systems establish the after-hours fixed-price subsystem connection, input orders after close, and receive executions via the general execution-report mechanism.

Key behavior:

- The after-hours fixed-price price field can be special; in the extracted operation text, `PRICE` is required to be zero for the relevant input message while price type is still identified as limit in the message schema. Verify the exact field rule before implementation.
- Connection subsystem function is `AP-CODE = 7`.
- In the cited buy/sell/reduction input message, `PRICE` must be `0` and `QUANTITY` must be greater than 0 and at most 499.
- Execution reports are merged into the general execution-report protocol; missing execution reports are handled by the execution-report resend subsystem.
- The workflow supports buy/sell input, query, reduction, cancellation, acknowledgement, and aggregate order quantity query.
- Certain error conditions are segment-specific: order time not reached/expired, quantity limit, price-type or time-in-force errors, restricted security, securities borrowing/short-selling restrictions, and total order amount controls.

Source: `O-019-A10 盤後定價交易電腦作業手冊`, updated `114.05.05`.

### Block Trading

The bundle contains separate manuals for block trading by matching method:

- `O-003-A10 鉅額逐筆交易電腦作業手冊`
- `O-003-A10 鉅額配對交易電腦作業手冊`

Use the correct manual according to whether the question is about negotiated/matched block trading or sequential block trading. Do not collapse these into ordinary trading; block trading has different message/file flows and historically interacts with error/default handling through block-specific files.

Sources: both `O-003-A10` block trading manuals, updated `107.10.23`.

### Auction And Public Subscription

Auction and public subscription are specialized workflows:

- `O-005-A10 上市證券拍賣電腦作業手冊`
- `O-006-A10 公開申購配售電腦作業手冊`

Use these when the user asks about bidding, subscription, allocation, broker files, or post-processing rather than ordinary order-book trading.

Sources: `O-005-A10`, updated `108.07.03`; `O-006-A10`, updated `113.08.07`.

### Dollar-Cost Averaging / Periodic Fixed-Amount Trading

`O-032-A10 證券商受託辦理定期定額買賣有價證券業務` covers broker periodic fixed-amount trading operations.

Source-derived facts:

- Each transmitted file can contain at most 8000 records in the cited source.
- For ordinary trading, `CAJ-MTHQTY` is entered in trading units and is capped at 499 trading units.

Source: `O-032-A10 證券商受託辦理定期定額買賣有價證券業務`, updated `108.05.21`.

## Order Lifecycle Pattern

Across trading manuals, model the lifecycle as:

1. Broker establishes the correct connection/session.
2. Broker sends input or query messages/files for the correct market segment.
3. TWSE returns acknowledgement or correct/error reply.
4. Broker reconciles remaining quantity, executions, and status.
5. Broker handles reductions/cancellations only through supported operation types.
6. Execution reports and post-trade files feed downstream accounting, risk, and settlement.

Never assume a market segment supports the same order operations as regular trading. Query the segment manual first.

## Practical Coding Rules

- Encode market segment explicitly in order models.
- Do not use a single enum like `REGULAR | ODD_LOT | AFTER_HOURS` unless it distinguishes intraday odd lot from after-hours odd lot and block-trading modes.
- Validate operation windows per segment and per operation type.
- Store original TWSE message/file code with every inbound/outbound record.
- Make return/error files first-class state changes.
- Require manual lookup before implementing a field layout.
