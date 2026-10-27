# Ledger

The ledger records the deposits and withdrawals on an organization's prepaid
credit accounts. An organization can have more than one account; `account_id`
identifies each one (for example, `"seer"`).

The ledger is not a separate service. Its endpoints are methods on the contract
service, which also owns invoices. The balance depends on the state of each
deposit's invoice, and the platform has no other reliable way to keep a separate
ledger in step with invoices.

## Messages

| Message | Purpose |
| --- | --- |
| `LedgerEntry` | One deposit or withdrawal. Amounts are signed. |
| `LedgerDeposit` | The credit that an off-cycle invoice buys. |
| `RecordLedgerWithdrawal` | Takes credit out of an account. |
| `GetLedgerBalance` | The balance, and the deposits that are still unpaid. |
| `ListLedgerEntries` | An account's entries, newest first. |

## Every entry has an invoice

- A deposit refers to the off-cycle invoice that pays for it.
- A withdrawal refers to the invoice that shows the credit-only usage it pays
  for. An invoice has at most one withdrawal per account.

## Deposits

There is no endpoint that records a deposit. To buy credit, set
`ledger_deposit` on `BillOffCycleInvoiceRequest` or
`CreateOffCycleInvoiceRequest`. The deposit is written in the same transaction
as the invoice. If the deposit were a separate call, a caller that crashed
between the two calls could leave a customer charged without credit.

## The balance is pessimistic

A deposit counts toward `balance_cents` only after its invoice is paid. Until
then, it is in `pending_deposit_cents`. The ledger reads the paid state from
each deposit's invoice. It does not record payments itself.

The ledger does not credit a deposit first and reverse it if the payment fails.
Usage that the customer does not pay for is a full loss, because AI usage has no
margin. Thus, credit must never be available before the money is received.

A withdrawal always takes its full amount, even if the balance becomes
negative.

## The ledger balance is not the wallet balance

Usage is not withdrawn as it occurs. It is counted in ClickHouse and withdrawn
periodically, for example at contract rollover. A withdrawal for each LLM call
would cause too many Postgres writes, and would couple usage tracking to
billing.

Thus, the current balance of a wallet (for example, the Seer wallet) is:

```
GetLedgerBalance.balance_cents - (usage cost not yet withdrawn, from the usage pricer)
```

`GetLedgerBalance` alone does not include usage that is not withdrawn yet.
