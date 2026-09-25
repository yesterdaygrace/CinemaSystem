# Cinema Cancellation and Refund Flow

```mermaid
flowchart TD
    A[Bioskop membatalkan schedule] --> B[Schedule = CANCELLED]
    B --> C[Cari order PAID]
    C --> D[Buat refund record]
    D --> E[Kirim / proses refund]
    E --> F{Refund berhasil?}

    F -->|Ya| G[Refund = COMPLETED]
    G --> H[Ticket = REFUNDED]
    H --> I[Release seat sesuai aturan bisnis]

    F -->|Tidak| J[Refund = FAILED / PENDING]
    J --> K[Retry / Manual handling]
```

## Data preservation

Pembatalan tidak menghapus:

```text
order
payment
ticket
```

Sebaliknya:

```text
schedule → CANCELLED
refund   → created
ticket   → REFUNDED
```

Dengan demikian histori transaksi tetap tersedia.
