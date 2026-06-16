# Integrated TWSE Rule Model

This is the synthesized model for using the TWSE broker operation manuals. Treat the extracted manuals as source evidence and this file as the decision framework.

## What These Manuals Are

The TWSE `證券商作業手冊` set is primarily a broker-system operation corpus. It describes how securities firms connect to TWSE systems, submit orders or files, receive reports, handle exceptional events, and implement product-specific workflows. It is not a complete substitute for statutes, exchange rules, investor-facing announcements, or real-time TWSE circulars.

Use it for:

- Trading workflow behavior as seen by broker systems.
- Message IDs, file codes, field semantics, return/error handling, and operational cutoffs.
- How special markets or products interact with ordinary trading, settlement, credit, securities lending, market data, or reporting.
- How to build checks into broker-side or trading-system code.

Do not use it alone for:

- Legal advice.
- Current investor eligibility, fee/tax, disclosure, or suitability decisions.
- A production rule that may have changed after the manual update date.

## Mental Model

Think of TWSE market operations as five layers:

1. **Market segment**: regular trading, intraday odd lot, after-hours odd lot, after-hours fixed price, block trading, auction, public subscription, ETF/ETN platforms, securities lending, margin, or default/error-correction workflows.
2. **Participant and account context**: investor account, broker proprietary account, comprehensive trading account, margin/short account, securities lending account, issuer, liquidity provider, market maker, or clearing/settlement actor.
3. **Order/report lifecycle**: input, acknowledgement, modification/reduction, cancellation, query, execution report, file transfer, reconciliation, exception repair.
4. **Protocol surface**: order-entry messages, single-message queries, batch files, FIX, TCP/IP host connection, market-data feeds, or dashboard/backup systems.
5. **Risk and exception control**: price/quantity/eligibility checks, order book/session restrictions, total order amount limits, credit controls, securities shortfall handling, error account correction, default declaration, and settlement repair.

When answering a question, first locate the layer. A question about "can this order be sent?" usually crosses layers 1, 2, 3, and 5. A question about "what field should I send?" is layer 4 but still depends on the market segment.

## Source Families

Use these source families before opening full text:

- Core trading: `O-001`, `O-002`, `O-003`, `O-005`, `O-006`, `O-019`, `O-037`
- Margin, day trading, and securities lending: `O-007`, `O-020`, `O-021`, `O-022`, `O-027`, `O-029`, `O-004`, `O-011`, `O-018`, `O-023`, `O-024`
- Account, settlement, and exceptions: `O-008`, `O-009`, `O-010`, `O-013`, `O-025`, `O-028`, `O-032`, `O-036`
- ETF/ETN/warrants/liquidity/market making: `O-026`, `O-030`, `O-031`, `O-033`, `O-034`, `O-035`, `O-038`
- Connectivity, protocols, and data: `O-016`, `O-101`, `O-104`, `O-105`, `O-106`, `O-107`, `O-108`, `O-121`, `O-124`, `O-125`, `O-126`, `O-127`, `O-128`

For complete per-manual routing, read `manual-domain-matrix.md`. It maps every downloaded manual to its expert role and common confusion boundaries.

## Answer Pattern

For factual answers:

1. State the rule in plain language.
2. State scope: market segment, product, account type, and whether it is order entry, post-trade reporting, file transfer, or exception handling.
3. State the implementation implication for systems.
4. Cite source manual title and update date.
5. Mention if a current TWSE circular or rule page should be checked.

For system design:

1. Split validation into pre-order, order-entry, acknowledgement, execution, post-trade reconciliation, and exception workflows.
2. Preserve source message/file names exactly.
3. Treat "query" files/messages as reconciliation controls, not as the primary source of order truth.
4. Add idempotency checks for order numbers, file sequence numbers, and repeated uploads.
5. Treat TWSE return/error files as required state transitions.

## Cross-Cutting Controls

- **Order identifiers**: many workflows require broker-side order or sequence identifiers to be unique in their context. Duplicate handling is a recurring rejection class.
- **Reduction/cancel/query separation**: a "change" operation is often specifically reduction, cancellation, or query. Do not assume price modification exists unless the manual says so for that segment.
- **Session gates**: many files/messages are accepted only in specific time windows. A system should encode market segment and operation windows separately.
- **Quantity units**: manuals may express quantities as trading units, shares, beneficial units, or product units. Never normalize without checking the specific manual.
- **Account restrictions**: comprehensive accounts, proprietary accounts, borrowing/lending accounts, and margin/short accounts often have special restrictions.
- **Post-trade repair**: error correction, default handling, day-trade securities shortfall, and lending workflows are operational repair paths. They should not be modeled as normal trading.
- **Return files are authoritative for batch operations**: file upload workflows usually require reading TWSE correct/error replies before continuing.

## Reasoning Heuristics

Use these heuristics to synthesize answers rather than quoting one manual in isolation.

### If a question mentions order placement

Ask:

1. Which market segment?
2. Which account/order condition?
3. Is the action new, reduce, cancel, query, or post-trade declaration?
4. Which channel/protocol?
5. Which post-trade reports prove the final state?

Then answer from the segment manual and only open protocol manuals for exact fields.

### If a question mentions "can I use X?"

Translate "X" into an account/product/workflow constraint. Examples:

- "Can a comprehensive account day trade?" means account restriction + day-trade reporting, not only trading session.
- "Can I borrow for day-trade shortfall?" means sell-first day-trade repair workflow, not ordinary securities lending.
- "Can I quote as liquidity provider?" means actor qualification/line declaration/quote-rule workflow, not regular order entry.

### If a question mentions dates or deadlines

Keep trade date labels exact:

- `T`: trade date.
- `T+1`, `T+2`, `T+3`: subsequent business/settlement workflow dates as defined by the specific manual.

Do not generalize a cutoff from one workflow to another. For example, day-trade `BC8` declaration cutoff and error-account declaration cutoff are separate controls.

### If a question mentions protocol fields

Do not paraphrase field names. Open the extracted text and copy field names exactly. State the manual title and update date. If the field belongs to a market segment message, read the segment manual before reading FIX/TCPIP docs.

### If a question mentions a failure

Classify the failure:

- Order reject: segment/order validation.
- Missing or disputed acknowledgement: query/reconnect/reconciliation.
- Execution/report mismatch: execution-report reconciliation.
- Error trade or account correction: `O-009`.
- Day-trade shortfall: `O-029`.
- Ordinary/credit default: `O-010`.
- Lending/borrow return problem: securities lending manuals.

This classification determines which state machine and source manual apply.

## Currentness Rule

Each answer must include the manual update date from `manual-index.md`. If the user is making production trading, compliance, or legal decisions, instruct them to verify against the live TWSE page and any later circulars. The downloaded bundle is a snapshot of the source page at build time.
