# TWSE Broker Manual Mind Map

Use this file when a user wants the whole skill as a mental map, or when a broad question needs orientation before opening detailed references.

This is a navigation artifact. For exact fields, file layouts, codes, and time windows, route from this map to the relevant reference and then to the extracted source manual.

## Expert Mental Model

```mermaid
mindmap
  root((TWSE Broker Operations))
    Market and Order Domains
      Regular trading
        O-001
        Order input
        Acknowledgement
        Execution report
        Cancel reduce query
      Odd lot
        Intraday odd lot O-037
        After-hours odd lot O-002
      After-hours fixed price
        O-019
        AP-CODE 7
        General execution report
      Block trading
        Sequential block O-003
        Paired block O-003
      Auction and subscription
        Auction O-005
        Public subscription O-006
      Periodic fixed amount
        DCA O-032
    Account and Risk Domains
      Investor account opening
        O-008
        B50 ordinary account
        B40 discretionary investment account
        B26 credit account
      Comprehensive account
        O-025
        Special restrictions
      Credit and margin
        O-007
        Margin purchase
        Short sale
      Default and exceptions
        Default O-010
        Error account O-009
        Account correction O-009
      Credit information
        Joint credit O-013
        Negative data O-036
      Customer funds
        Custody and use O-028
    Lending and Shortfall Domains
      Securities lending
        Front office O-020
        Back office O-021
        Broker SBL system O-022
        SBL query platform O-121
      Day trading
        O-029
        Detail declaration
        Sell-first shortfall
      Borrow and procurement
        Tender borrow O-004
        Corrective borrow O-011
        Tender purchase O-018
        Securities finance tender purchase O-024
        Securities finance negotiated lending O-023
      Borrower selling declaration
        O-012
      Money lending
        O-027
    Products and Participant Domains
      ETF
        Broker side O-030
        Investment trust side O-031
      ETN
        Broker side O-033
        Issuer side O-034
      Warrant and ETF liquidity provider
        Dedicated line O-026
        Quote rules O-035
      Stock market maker
        Incentive and reporting O-038
    Protocol and Transport Domains
      Host connection
        O-101
        Connection subsystem
        Single-message and file transfer
        AP startup login startup
      TCP IP trading network
        O-105
        Dedicated router
        Dedicated firewall
        Source IP plus Source Port
        Socket layer
        Heartbeat
        Main backup test sites
      FIX
        Chinese spec O-124
        English spec O-125
        CompID
        TargetSubID
      Market data
        Chinese spec O-126
        English spec O-127
        IP multicast
        IGMP
        PACK BCD
        Sequence gaps
      Information exchange platform
        O-106
      Second channels
        Second execution report O-107
        Second file transfer O-108
      Backup systems
        Full-day backup O-104
        Spare auction equipment O-128
    Report and Evidence Domains
      Statistics files
        O-016
      Correct error replies
        Required before next batch
      Query files
        Reconciliation evidence
      Market data heartbeat
        Format 16
      Audit trail
        Original event
        Submission
        TWSE reply
        Final state
```

## Manual Routing Map

```mermaid
mindmap
  root((48 TWSE Source Manuals))
    Trading Markets
      O-001 regular trading
      O-037 intraday odd lot
      O-002 after-hours odd lot
      O-019 after-hours fixed price
      O-003 sequential block trading
      O-003 paired block trading
      O-005 listed securities auction
      O-006 public subscription
      O-032 periodic fixed amount trading
    Accounts Settlement Exceptions
      O-008 investor account opening
      O-025 comprehensive trading account
      O-009 error account and account correction
      O-010 ordinary and credit default
      O-013 joint credit information
      O-036 negative data query
      O-028 customer fund custody and use
    Financing Lending Shortfall
      O-007 credit trading
      O-029 day trading
      O-020 securities lending front office
      O-021 securities lending back office
      O-022 broker SBL system
      O-121 SBL information exchange query
      O-004 tender borrowing
      O-011 corrective borrowing
      O-018 tender purchase
      O-024 securities finance tender purchase
      O-023 securities finance negotiated lending
      O-012 borrower selling stock declaration
      O-027 money lending business
    Products Issuance Liquidity
      O-030 broker ETF
      O-031 investment trust ETF
      O-033 ETN broker side
      O-034 ETN issuer side
      O-026 warrant ETF LP dedicated line
      O-035 LP quote rules
      O-038 stock market maker incentive
    Connectivity Protocol Data
      O-101 host connection
      O-105 TCP IP host connection
      O-106 information exchange host connection
      O-107 second execution report
      O-108 second file transfer
      O-124 FIX Chinese
      O-125 FIX English
      O-126 market data Chinese
      O-127 market data English
      O-016 statistical report files
      O-104 full-day backup
      O-128 spare auction equipment
```

## Ambiguity Map

| User phrase | Route first | Avoid confusing with |
| --- | --- | --- |
| 開戶 | `O-008` investor/account-opening workflows | KYC law, comprehensive account, credit account unless specified |
| 全權委託開戶 | `O-008` B40/B41/BC5 | Ordinary B50 account only |
| 錯帳 | `O-009` B02/B08/B54/B55/B57 | Default, account correction, order modification |
| 更正帳號 | `O-009` but separate from錯帳 | Error account quantity repair |
| 違約 | `O-010` ordinary/credit default | Order reject,錯帳, day-trade shortfall |
| 借券 | First classify lifecycle | SBL, tender borrow, corrective borrow, borrower sell, shortfall repair |
| 標借 | `O-004` tender borrowing | 標購, 證金標購, ordinary SBL |
| 標購 | `O-018` tender purchase | 標借, 證金標購 |
| 證金標購 | `O-024` | Exchange tender purchase |
| 證金議借 | `O-023` | Tender borrow or ordinary SBL |
| 當沖券差 | `O-029` then repair manuals | Ordinary SBL only |
| 行情 | `O-126/O-127` | Host TCP socket or FIX |
| 下單 FIX | `O-124/O-125` plus market manual | Market-data feed |
| Source IP Port socket | `O-105` | FIX CompID or multicast group |
| 第二路 | Need object: execution report or file transfer | Market-data duplicate multicast groups |
| 備援 | Need object: line/site/full-day/spare equipment | Active-active business semantics |

## How To Use This Map

1. Start with the user phrase and choose a domain.
2. If the phrase is ambiguous, use the ambiguity map before answering.
3. Open the domain reference:
   - Trading: `trading-markets.md`
   - Accounts/exceptions: `accounts-settlement-and-exceptions.md`
   - Financing/lending/shortfall: `financing-lending-and-shortfall.md`
   - Products/liquidity: `products-liquidity-and-issuance.md`
   - Connectivity/protocol: `broker-exchange-integration.md`, then `protocols-and-market-data.md`
4. For exact fields or file formats, open the extracted source text listed in `manual-index.md`.
5. Cite the manual title and update date in the answer.

