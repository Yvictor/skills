# Financing, Securities Lending, Day Trading, And Shortfall Workflows

Use this file to understand how margin, lending, day trading, and securities shortfalls connect. Open the source text for exact fields and file/message layouts.

## Credit And Margin Trading

`O-007-A10 信用交易電腦作業手冊` covers broker workflows around margin purchase, short sale, credit account/report operations, and related files. Treat it as a post-order and credit-control corpus, not a general explanation of all legal eligibility rules.

System implications:

- Credit trading status belongs to the account/product/order context, not only to an order side.
- Separate cash, margin purchase, short sale, and other order conditions in the order model.
- Validate product eligibility and account permissions before order submission.
- Reconcile credit reports and error replies as part of daily operations.

Source: `O-007-A10 信用交易電腦作業手冊`, updated `115.01.13`.

## Day Trading

`O-029-A10 現股當日沖銷交易電腦作業手冊` describes day-trading detail reporting and query workflows. It includes both buy-first-sell-later and sell-first-buy-later evolution in its revision history and operational sections.

Key synthesized rules:

- Day-trade detail reporting is an operational/reporting workflow, not simply an order flag.
- The `BC8` detail declaration has packaging constraints; the extracted text states a per package transaction sequence count limit of 8000 and requires buy/sell day-trade quantities to match within the package.
- Day trading applies to ordinary trading and after-hours fixed-price trading contexts; for securities marked as only buy-first-sell-later day trading, after-hours fixed-price trading is sell-only for that day-trade purpose.
- Comprehensive trading accounts are restricted from day trading in the cited operational text.
- If sell-first-buy-later day trading cannot be covered by intraday buyback and settlement securities are missing, the workflow moves into T+1/T+2/T+3 shortfall, buy-in, borrowing, and declaration processes.

Source: `O-029-A10 現股當日沖銷交易電腦作業手冊`, updated `109.10.12`.

## Securities Lending Front Office And Back Office

The securities lending manuals split front-office and back-office responsibilities:

- `O-020-A10 有價證券借貸前檯電腦作業手冊`
- `O-021-A10 有價證券借貸後檯電腦作業手冊`
- `O-022-A10 證券商有價證券借貸制度電腦作業手冊`
- `O-121-A10資訊交換平台有價證券借貸相關資料查詢作業手冊`

Use front-office material for participant-facing lending operations and back-office material for settlement/administrative reconciliation. Do not merge them in implementation; the operational controls and file flows differ.

System implications:

- Lending contracts, lending account identities, broker proprietary/special accounts, and delivery/return events should be modeled separately from ordinary sell orders.
- A securities lending workflow can be a planned borrowing/lending workflow or a repair path for day-trade securities shortfall.
- For information exchange queries, use `O-121` rather than general SBL manuals.

Sources: `O-020` updated `114.01.06`; `O-021` updated `115.02.06`; `O-022` updated `113.11.28`; `O-121` updated `108.09.02`.

## Borrowing, Tender, And Securities Finance Workflows

The bundle includes multiple repair/procurement channels:

- `O-004-A10 標借電腦作業手冊`
- `O-011-A10 補正借券電腦作業手冊`
- `O-018-A10 標購電腦作業手冊`
- `O-023-A10 證金議借交易電腦作業手冊`
- `O-024-A10 證金標購電腦作業手冊`
- `O-027-A10 證券業務借貸款項電腦作業手冊`

These are not interchangeable:

- **標借 / 補正借券 / 標購** are operational channels used when securities need to be borrowed or procured under exchange/broker processes.
- **證金標購 / 證金議借** involve securities finance company workflows.
- **證券業務借貸款項** is about broker lending-money business operations, not securities lending.

When a question says "借", determine whether it means margin financing, securities lending, tender borrowing, money lending, or day-trade settlement shortfall.

## Shortfall Handling Model

When a trade creates a securities delivery problem:

1. Determine whether the problem originates in day trading, ordinary settlement, error account, default, or lending return.
2. Determine who owns the repair workflow: investor, broker, securities finance company, or exchange platform.
3. Use the specific manual for the repair path.
4. Track dates explicitly: T, T+1, T+2, T+3 appear in several workflows and are not interchangeable.
5. Treat declarations and correct/error replies as auditable settlement evidence.
