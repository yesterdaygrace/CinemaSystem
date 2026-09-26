# End-to-End System Flow

This flowchart illustrates the comprehensive customer journey across movie discovery, multi-city branch selection, real-time seat reservation, distributed locking, simulated payment, ticket issuance, and auto-restock mechanisms.

```mermaid
flowchart TD
    Start([Customer opens Mobile App / Web]) --> SelectCinema[Select City & Cinema Branch<br>e.g. Jakarta, Surabaya, Medan]
    SelectCinema --> SelectMovie[Browse Now Showing Films]
    SelectMovie --> SelectSchedule[Pick Screening Date & Time<br>Times displayed in Local Timezone]
    SelectSchedule --> ViewSeatmap[View Real-Time Studio Seatmap]

    ViewSeatmap --> ChooseSeat{Are seats available?}

    ChooseSeat -- No / Occupied --> AltSeat[Select Alternative Seats]
    AltSeat --> ViewSeatmap

    ChooseSeat -- Yes --> AcquireLock[🔒 System Locks Seats for 10 Minutes<br>Redis Redlock + PostgreSQL Row Lock<br>Status: AVAILABLE → HELD]

    AcquireLock --> PaymentStep[Customer proceeds to Checkout<br>Simulate Successful Payment]

    PaymentStep --> PayCheck{Payment Succeeded<br>Within 10 Minutes?}

    PayCheck -- Yes --> IssueTicket[🎟️ Tickets Officially Issued<br>Unique Ticket Code + QR Code<br>Status: HELD → SOLD<br>Confirmation sent via WhatsApp/Email]
    IssueTicket --> CinemaEntrance([🍿 Scan QR Code at Studio Entrance])

    PayCheck -- No / Expired --> AutoRestock[🔓 Automatic Restock Worker Executes<br>Redis key deleted, status reverts to AVAILABLE<br>Pending Order marked EXPIRED]
    AutoRestock --> Cancelled([Order Cancelled - Seats Available to Others])
```

---

## Key Operational Stages

1. **Discovery & Timezone Adaptation**: Customers browse cinema branches nationwide. Timestamps are stored in PostgreSQL as `TIMESTAMPTZ` and rendered dynamically in the cinema branch's local timezone (`bioskop.zona_waktu`).
2. **Instant Hold (Zero Double-Booking)**: Clicking a seat triggers an atomic 10-minute hold (`HELD`) enforced by Redis distributed lock and PostgreSQL row-level locks.
3. **Simulated Payment Gateway**: Integration with payment gateways (Midtrans / Xendit). Successful payment transitions seats to `SOLD`.
4. **Automated Inventory Restocking**: If payment is not finalized before the 10-minute countdown expires, an automated consumer releases the seat lock, instantly returning the seat to `AVAILABLE` without human intervention.
