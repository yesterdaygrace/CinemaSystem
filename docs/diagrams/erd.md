# Entity Relationship Diagram (ERD)

Relational model schema representing the full cinema ticketing domain across **14 relational tables** in PostgreSQL (Third Normal Form / 3NF), synchronized with [`database.sql`](../database.sql):

```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS ||--o{ SHOW_SEATS : holds
    USERS ||--o{ AUDIT_LOGS : performs

    CINEMAS ||--o{ STUDIOS : contains
    STUDIOS ||--o{ SEATS : contains
    STUDIOS ||--o{ SCHEDULES : hosts

    MOVIES ||--o{ SCHEDULES : has

    SCHEDULES ||--o{ SHOW_SEATS : creates
    SEATS ||--o{ SHOW_SEATS : assigned_to

    ORDERS ||--o{ ORDER_ITEMS : contains
    SHOW_SEATS ||--o{ ORDER_ITEMS : booked_by

    ORDERS ||--o{ PAYMENTS : has
    ORDERS ||--o{ REFUNDS : may_have

    ORDER_ITEMS ||--|| TICKETS : generates
    PAYMENTS ||--o{ REFUNDS : refunded_by
    PAYMENTS ||--o{ PAYMENT_EVENTS : receives

    USERS {
        bigint id PK "pengguna.id"
        varchar name "nama"
        varchar email UK "email"
        varchar password_hash "hash_kata_sandi"
        varchar role "peran (ADMIN, CUSTOMER)"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    CINEMAS {
        bigint id PK "bioskop.id"
        varchar name "nama"
        varchar city "kota"
        varchar timezone "zona_waktu (e.g. Asia/Jakarta)"
        text address "alamat"
        varchar status "status"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    STUDIOS {
        bigint id PK "studio.id"
        bigint cinema_id FK "bioskop_id"
        varchar name "nama"
        int capacity "kapasitas"
        varchar type "tipe (REGULAR, IMAX, PREMIERE)"
        varchar status "status"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    SEATS {
        bigint id PK "kursi.id"
        bigint studio_id FK "studio_id"
        varchar row_label "label_baris"
        int seat_number "nomor_kursi"
        varchar seat_type "tipe_kursi (REGULAR, VIP, SWEETBOX)"
    }

    MOVIES {
        bigint id PK "film.id"
        varchar title "judul"
        int duration_minutes "durasi_menit"
        text description "deskripsi"
        varchar age_rating "rating_usia (SU, 13+, 17+, 21+)"
        varchar status "status (ACTIVE, ARCHIVED)"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    SCHEDULES {
        bigint id PK "jadwal.id"
        bigint movie_id FK "film_id"
        bigint studio_id FK "studio_id"
        timestamp start_time "waktu_mulai"
        timestamp end_time "waktu_selesai"
        varchar status "status (SCHEDULED, COMPLETED, CANCELLED)"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    SHOW_SEATS {
        bigint id PK "kursi_jadwal.id"
        bigint schedule_id FK "jadwal_id"
        bigint seat_id FK "kursi_id"
        numeric price "harga"
        varchar status "status (AVAILABLE, HELD, SOLD, INACTIVE)"
        bigint held_by FK "ditahan_oleh"
        timestamp held_until "ditahan_sampai"
        timestamp sold_at "terjual_pada"
        timestamp updated_at "diperbarui_pada"
    }

    ORDERS {
        bigint id PK "pesanan.id"
        varchar order_number UK "nomor_pesanan"
        bigint user_id FK "pengguna_id"
        numeric total_amount "total_harga"
        varchar status "status (PENDING, PAID, EXPIRED, CANCELLED)"
        timestamp expires_at "kedaluwarsa_pada"
        timestamp created_at "dibuat_pada"
        timestamp updated_at "diperbarui_pada"
    }

    ORDER_ITEMS {
        bigint id PK "item_pesanan.id"
        bigint order_id FK "pesanan_id"
        bigint show_seat_id FK "kursi_jadwal_id"
        numeric price "harga"
    }

    PAYMENTS {
        bigint id PK "pembayaran.id"
        bigint order_id FK "pesanan_id"
        varchar payment_reference UK "referensi_pembayaran"
        varchar payment_method "metode_pembayaran"
        numeric amount "total_bayar"
        varchar status "status (PENDING, SUCCESS, FAILED, REFUNDED)"
        timestamp paid_at "dibayar_pada"
        timestamp created_at "dibuat_pada"
    }

    TICKETS {
        bigint id PK "tiket.id"
        bigint order_item_id FK "item_pesanan_id"
        varchar ticket_code UK "kode_tiket"
        varchar status "status (ISSUED, USED, REFUNDED, CANCELLED)"
        timestamp issued_at "diterbitkan_pada"
        timestamp cancelled_at "dibatalkan_pada"
    }

    REFUNDS {
        bigint id PK "pengembalian_dana.id"
        bigint payment_id FK "pembayaran_id"
        varchar refund_reference UK "referensi_pengembalian"
        numeric amount "total_kembali"
        text reason "alasan"
        varchar status "status (PENDING, SUCCESS, FAILED)"
        timestamp processed_at "diproses_pada"
        timestamp created_at "dibuat_pada"
    }

    AUDIT_LOGS {
        bigint id PK "log_audit.id"
        bigint user_id FK "pengguna_id"
        varchar action "aksi"
        varchar entity_type "tipe_entitas"
        bigint entity_id "entitas_id"
        jsonb old_values "nilai_lama"
        jsonb new_values "nilai_baru"
        timestamp created_at "dibuat_pada"
    }

    PAYMENT_EVENTS {
        bigint id PK "event_pembayaran.id"
        varchar provider_event_id UK "id_event_provider"
        bigint payment_id FK "pembayaran_id"
        varchar event_type "tipe_event"
        jsonb payload "payload"
        timestamp received_at "diterima_pada"
        timestamp processed_at "diproses_pada"
    }
```

---

## Key Constraints & Guarantees

1. **Anti Double-Booking**:
   - Unique constraint `uq_jadwal_kursi UNIQUE (jadwal_id, kursi_id)` on `kursi_jadwal`.
   - Seat lifecycle state machine: `AVAILABLE` → `HELD` (10-minute hold window) → `SOLD`.
2. **Dual-Layer Overlap Prevention**:
   - Application layer: Interval intersection validation returning HTTP 409 Conflict.
   - Database engine level: PostgreSQL `btree_gist` exclusion constraint:
     ```sql
     CONSTRAINT no_overlapping_schedule EXCLUDE USING gist (
         studio_id WITH =,
         tstzrange(waktu_mulai, waktu_selesai, '[)') WITH &&
     ) WHERE (status = 'SCHEDULED')
     ```
3. **Webhook Idempotency Protection**:
   - `event_pembayaran` with `id_event_provider VARCHAR(100) NOT NULL UNIQUE` prevents duplicate webhook processing from external payment gateways.
4. **National Multi-City Support**:
   - `bioskop.zona_waktu` (`Asia/Jakarta`, `Asia/Makassar`, `Asia/Jayapura`) combined with PostgreSQL `TIMESTAMPTZ` ensures unambiguous screening timestamps across Indonesian time zones.
5. **Full Financial Auditability**:
   - Physical records in `pesanan`, `pembayaran`, `tiket`, `pengembalian_dana`, and `log_audit` are never hard-deleted.
