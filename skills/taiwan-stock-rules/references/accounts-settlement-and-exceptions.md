# Accounts, Settlement, Defaults, And Exception Handling

This file synthesizes the account and post-trade exception manuals.

## Investor Account Opening

`O-008-A10 投資人開戶電腦作業手冊` is the source for broker computer workflows around investor account opening. Use it for account data exchange, reporting, validation, and operational file questions.

Do not use it as the only source for suitability, KYC, or current account-opening law. For production onboarding, verify against current TWSE, FSC, TDCC, and broker compliance rules.

Source: `O-008-A10 投資人開戶電腦作業手冊`, updated `114.08.11`.

## Comprehensive Trading Account

`O-025-A10 綜合交易帳號電腦作業手冊` covers comprehensive trading account operations. It is relevant whenever the user asks whether a workflow can use a comprehensive account.

Important cross-rule:

- The day-trading manual states that clients may not use comprehensive trading accounts for securities day trading in the relevant operational section. Treat comprehensive accounts as special-context accounts requiring explicit manual checks before enabling trading features.

Source: `O-025-A10 綜合交易帳號電腦作業手冊`, updated `108.05.22`; day-trading cross-reference `O-029`, updated `109.10.12`.

## Error Account And Account Correction

`O-009-A10 錯帳及更正帳號電腦作業手冊` separates error-account reporting from account correction.

Synthesized rules:

- Error-account reporting and account correction are post-trade repair workflows, not normal trade amendments.
- Error-account workflows can include error quantity, offset quantity, proprietary securities used for settlement, and recovery/cover processing.
- Account correction is not treated as error account reporting in the manual logic; it requires reason/relationship data and is handled at the order/account correction level.
- The manual distinguishes ordinary and delayed-settlement cases and includes T/T+1/T+2/T+3 timing references.
- Block-trade error workflows and spread error workflows have their own file codes and should be handled separately from ordinary error-account records.

System design:

- Use a separate exception domain model: `trade_error`, `account_correction`, `delayed_settlement_error`, `block_trade_error`, `spread_error`.
- Keep original trade identity, original account, corrected account, quantity split, offset quantity, and proprietary-settlement fields.
- Require return files before treating an exception submission as accepted.

Source: `O-009-A10 錯帳及更正帳號電腦作業手冊`, updated `108.05.21`.

## Default Handling

`O-010-A10 普通違約及信用違約電腦作業手冊` covers ordinary and credit-default operational workflows. It includes default declarations, default offset data, default handling declarations, query/report files, and historically block default handling.

Use it when:

- A customer or credit account fails settlement.
- The workflow asks about ordinary default versus credit default.
- Broker systems need to declare, query, offset, or process default-related data.

Do not treat default handling as just another failed order. It is a settlement/legal exception workflow with its own reporting and repair lifecycle.

Source: `O-010-A10 普通違約及信用違約電腦作業手冊`, updated `115.06.01`.

## Joint Credit / Negative Data

Use:

- `O-013-A10 證券商聯合徵信電腦作業手冊`
- `O-036-A10 聯徵中心負面資料查詢電腦作業手冊`

These are data-query/reporting workflows for credit/negative-data operations, not trading rules. Treat them as broker risk-control support systems.

Sources: `O-013` updated `105.03.15`; `O-036` updated `109.03.02`.

## Customer Fund Custody And Use

`O-028-A10-「證券商辦理客戶委託保管及運用其款項操作辦法」之電腦作業手冊` covers broker operations around customer fund custody/use workflows. Use it when the question is about entrusted cash custody/use rather than market trading.

Source: `O-028-A10`, updated `99.12.20`.

## Exception Handling Checklist

Before answering or implementing:

1. Identify whether the event is pre-trade validation, order rejection, trade error, account correction, settlement shortfall, default, or reporting query.
2. Identify ordinary, credit, day-trade, block-trade, or special-product context.
3. Keep T/T+1/T+2/T+3 explicit.
4. Use the exact file/message family from the relevant manual.
5. Require correct/error reply handling.
6. Preserve audit trail: original trade, submitted repair, TWSE reply, final status.
