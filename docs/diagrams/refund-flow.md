# Cinema Cancellation and Refund Flow

This document details the difference between **Cinema-Initiated Cancellation** and **Customer-Initiated Return**, highlighting automated 100% refund disbursement and immutable audit preservation.

---

## 1. Cinema-Initiated Screening Cancellation Flow (100% Refund)

When a cinema branch experiences unforeseen operational issues (projector lamp malfunction, power outage, technical issues):

```mermaid
flowchart TD
    A[Cinema Manager cancels schedule in Admin Portal] --> B[API marks jadwal status = CANCELLED]
    B --> C[All seats in studio for this schedule marked INACTIVE<br>Cannot be booked by any user]

    C --> D[Identify all affected orders where status = PAID]
    D --> E[Kafka Event Dispatched: schedule.cancelled]

    subgraph RefundWorker ["Automated Refund & Notification Engine"]
        E --> F[Create pengembalian_dana record with status = PENDING]
        F --> G[Dispatch 100% refund transaction to Payment Gateway API]
        G --> H{Disbursement Successful?}

        H -->|Yes| I[UPDATE pengembalian_dana SET status = 'SUCCESS', diproses_pada = NOW()]
        I --> J[UPDATE tiket SET status = 'REFUNDED', dibatalkan_pada = NOW()]
        J --> K[UPDATE pembayaran SET status = 'REFUNDED']
        K --> L[Dispatch WhatsApp & Email notification to customer with refund proof]

        H -->|No| M[UPDATE pengembalian_dana SET status = 'FAILED']
        M --> N[Push to Dead Letter Queue & Alert Finance Operations]
    end
```

---

## 2. Business Rules: Cinema Cancellation vs Customer Cancellation

| Attribute | Cinema-Initiated Cancellation | Customer Cancellation (Voluntary) |
|---|---|---|
| **Trigger** | Studio failure, projector outage, force majeure. | Customer changes their mind or schedule. |
| **Schedule Status** | Changes to `CANCELLED`. | Remains `SCHEDULED`. |
| **Seat Inventory Effect** | `kursi_jadwal` marked **`INACTIVE`** (seats are NOT restocked for this cancelled screening). | `kursi_jadwal` returns to **`AVAILABLE`** (seats can be bought by others). |
| **Refund Amount** | **100% full refund** without deduction or administrative fees. | Depends on cinema policy (e.g. 80% refund or non-refundable). |
| **Customer Notification** | Priority push notification + WhatsApp apology & refund receipt. | Standard cancellation confirmation. |

---

## 3. Data Preservation & Financial Auditability

Operational cancellations **never execute hard-deletes (`DELETE`)** on financial tables:

```text
Do NOT execute:
DELETE FROM pesanan WHERE jadwal_id = 1;
DELETE FROM pembayaran WHERE ...;
DELETE FROM tiket WHERE ...;
```

Instead, immutable state transitions are applied:

```text
jadwal            : SCHEDULED → CANCELLED
kursi_jadwal      : SOLD      → INACTIVE
pesanan           : PAID      (Retained for transaction history)
pembayaran        : SUCCESS   → REFUNDED
tiket             : ISSUED    → REFUNDED
pengembalian_dana : PENDING   → SUCCESS
log_audit         : INSERT record of Admin cancellation action
```

This guarantees an unbroken financial audit trail for internal accounting, tax compliance, and payment gateway reconciliation.
