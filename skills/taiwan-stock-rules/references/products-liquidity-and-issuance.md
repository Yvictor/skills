# ETFs, ETNs, Warrants, Liquidity Providers, And Market Makers

This file synthesizes product-specific and liquidity-provider manuals.

## ETF Operations

The bundle distinguishes ETF operations by participant:

- `O-030-A10 證券商ETF電腦作業手冊`: broker-side ETF operations.
- `O-031-A10 投信ETF電腦作業手冊`: investment trust / issuer-side ETF operations.

Do not answer ETF creation/redemption, basket, cash component, broker query, or issuer declaration questions from only one side. Determine whether the user is asking as a broker, issuer/investment trust, liquidity provider, or trading-system implementer.

Sources: `O-030` and `O-031`, both updated `114.01.17`.

## ETN Subscription And Redemption Platform

ETN workflows are split by participant:

- `O-033-A10 ETN申購賣回平台--證券商端電腦作業手冊`
- `O-034-A10 ETN申購賣回平台--發行人端電腦作業手冊`

The issuer manual includes workflows such as basic subscription/redemption data declaration/query, position lock query, detail summary query, actual T-day amount declaration/query, confirmation files, receivable/payable files, inventory units for market making, and quote-exemption date declaration/query.

System implications:

- Model issuer-side and broker-side ETN processes separately.
- Treat subscription/redemption as a platform workflow with declarations, confirmations, amount calculations, and post-processing, not as ordinary order-book trading.
- Keep inventory-for-market-making and quote-exemption workflows separate from investor subscription/redemption.

Broker-side source-derived operation codes:

| Workflow | Code |
| --- | --- |
| PRF basic subscription/redemption data query | `ME3` |
| Remaining application units query | `MEN` |
| Application subscription/redemption file declaration | `ME4` |
| Application subscription/redemption file query | `ME5` |
| Redemption position lock query | `ME6` |
| Preliminary review reply query | `MEC` |
| T-day actual subscription/redemption amount query | `MEF` |
| Full subscription detail confirmation query | `MEG` |
| Full subscription detail confirmation declaration | `MEH` |
| Full subscription/redemption detail confirmation re-review query | `MEK` |
| Subscription/redemption receivable/payable query | `MEO` |
| Investor roster query | `MEP` |
| Delisting receivable/payable query | `MES` |

Broker-side source-derived rules:

- Declaration sends must wait for TWSE error-message reply before sending another declaration.
- Chinese fields use BIG5 encoding.
- More than 30 accumulated field errors stops further processing.
- PRF basic-data query is open `0800-1530`, and TWSE actively sends at `0800`.

Issuer-side source-derived timing:

| Workflow | Timing |
| --- | --- |
| PRF `ME1` declaration | `T-1 16:30-19:00` |
| T-day redemption lock result query | `T 15:30-18:00` |
| T-day actual amount declaration | Before `T+1 09:00` |
| Re-review amount confirmation | `T+1 09:30-12:00` |
| Receivable/payable query | `T+1 12:30-15:30` |
| Inventory units for market making | `T 09:00-15:30` |
| Quote-exemption date check | Query with `MEV` after declaration |
| Investor roster production on delisting day | `13:30` |
| Delisting receivable/payable query | After `2:00` on delisting day |

Issuer-side constraints:

- For redemption, regardless of issuer note character, the confirmation is treated as `Y`.
- Issuers may not apply for subscription/redemption of self-issued ETNs.
- Issuer administrator user ID is fixed as dealer code plus `IR01`.

Sources: `O-033` and `O-034`, both updated `112.12.20`.

## Warrants And ETF Liquidity Provider Lines

`O-026-A10 權證暨ETF流動量提供者專用電腦作業手冊` covers dedicated line/PVC declaration and query for warrant and ETF liquidity providers.

Synthesized rules:

- The relevant operations include declaration and query workflows, not general quote pricing rules.
- The manual includes dedicated codes for adding/deleting warrant liquidity lines and ETF liquidity lines.
- ETF liquidity-provider dedicated lines are constrained to FIX lines in the cited error rules.
- A successful declaration should be followed by a query confirmation.
- Correct/error replies must be checked before resubmitting or continuing.

Source-derived lookup:

| Item | Value |
| --- | --- |
| PVC declaration operation | `B97`, available `08:00 ~ 18:00` |
| PVC query operation | `B98`, available `08:00 ~ 18:00` |
| Field error cutoff | More than 50 accumulated field errors stops further processing |
| `WK-CODE 01` | Warrant liquidity dedicated line add |
| `WK-CODE 02` | Warrant liquidity dedicated line delete |
| `WK-CODE 03` | ETF liquidity dedicated line add |
| `WK-CODE 04` | ETF liquidity dedicated line delete |
| Query all branches | `RQST-BRKID = "****"` |

Source: `O-026-A10 權證暨ETF流動量提供者專用電腦作業手冊`, updated `114.12.15`.

## Liquidity Provider Quote Rules

`O-035-A10 流動量提供者報價規則電腦作業手冊` is short in extracted text. Use it as a pointer to quote-rule operations, but verify against current TWSE product and liquidity-provider rules before production decisions.

Source: `O-035-A10 流動量提供者報價規則電腦作業手冊`, updated `111.08.12`.

## Stock Market Makers And Trading Incentive Participants

`O-038-A10 股票造市者及交易獎勵參與者電腦作業手冊` covers performance and monthly fee-rebate query workflows for stock market makers, trading incentive participants, and innovation-board market makers.

Key workflow families:

- Performance file query for stock market makers and trading incentive participants.
- Monthly fee-rebate file query.
- Innovation-board market-maker performance file query.
- Innovation-board market-maker monthly fee-rebate file query.

System implications:

- This manual is about measurement and fee/rebate/reporting files, not order-entry rules for market making.
- Keep performance data type parsing explicit.
- Treat "whether market-making obligation is achieved" as a reported field, not as a value to infer from raw trades unless building a separate analytics system.

Source: `O-038-A10 股票造市者及交易獎勵參與者電腦作業手冊`, updated `111.08.12`.

## Product Routing Rule

When a question includes ETF, ETN, warrant, liquidity provider, or market maker:

1. Identify product.
2. Identify actor: broker, issuer, investment trust, liquidity provider, market maker, investor.
3. Identify workflow: order-book trading, subscription/redemption, line declaration, quote rule, performance/rebate query.
4. Use the matching manual family.
5. Do not infer one actor's workflow from another actor's manual.
