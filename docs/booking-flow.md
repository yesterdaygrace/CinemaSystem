# Booking Flow and Concurrency

## Normal booking

```mermaid
flowchart TD
    A[Customer memilih seat] --> B[Backend menerima request]
    B --> C[Start transaction]
    C --> D[Lock show_seat row]
    D --> E{Status AVAILABLE?}

    E -->|No| F[Reject request]
    E -->|Yes| G[Set HELD]
    G --> H[Set held_until]
    H --> I[Commit]
    I --> J[Payment]
    J --> K{Payment success?}

    K -->|Yes| L[Set SOLD]
    K -->|No / Timeout| M[Set AVAILABLE]
```

## Concurrent requests

```mermaid
sequenceDiagram
    participant A as Customer A
    participant API as Go API
    participant DB as PostgreSQL
    participant B as Customer B

    A->>API: Hold A10
    API->>DB: BEGIN + SELECT FOR UPDATE A10
    DB-->>API: A10 AVAILABLE
    API->>DB: UPDATE A10 = HELD

    B->>API: Hold A10
    API->>DB: SELECT FOR UPDATE A10
    Note over DB: Request B waits for the row lock

    API->>DB: COMMIT
    DB-->>API: Row lock released

    DB-->>API: A10 = HELD
    API-->>B: 409 Seat unavailable
```

## Important rule

`FOR UPDATE` protects the critical section.

Idempotency is a separate mechanism for duplicate requests.
