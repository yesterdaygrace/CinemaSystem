# Cinema Ticket System

Sistem pembelian tiket bioskop online yang dirancang untuk skala nasional dengan banyak cabang dan akses pengguna secara bersamaan.

Repository ini berisi jawaban untuk:

- **A. System Design Test**
- **B. Database Design Test**
- **C. Skill Test**

## 1. Scope

### A. System Design

Sistem dirancang untuk menangani:

- Customer melihat jadwal tayang.
- Customer memilih kursi.
- Kursi tidak boleh terjual kepada dua customer untuk jadwal yang sama.
- Banyak customer dapat mengakses sistem secara bersamaan.
- Kursi yang sedang dalam proses pembayaran dapat ditahan sementara.
- Kursi kembali tersedia jika pembayaran gagal atau hold berakhir.
- Tiket yang sudah terjual dapat dicatat dan ditelusuri.
- Pembatalan oleh pihak bioskop dapat memicu proses refund.
- Riwayat order, pembayaran, tiket, dan refund tetap disimpan.

### B. Database Design

Database dirancang dengan entitas utama:

```text
users
cinemas
studios
seats
movies
schedules
show_seats
orders
order_items
payments
tickets
refunds
audit_logs
```

Tidak semua tabel pada desain B harus mempunyai API pada bagian C. Desain database menjelaskan kebutuhan sistem secara menyeluruh, sedangkan implementasi C hanya mengerjakan endpoint yang diminta.

### C. Skill Test

Implementasi Golang difokuskan pada:

```text
POST   /api/v1/auth/login

GET    /api/v1/schedules
GET    /api/v1/schedules/:id
POST   /api/v1/schedules
PUT    /api/v1/schedules/:id
DELETE /api/v1/schedules/:id
```

Authorization menggunakan JWT dari proses login.

## 2. Architecture

Project menggunakan **modular monolith**.

```text
Client
   |
   v
Gin Router
   |
   +------------------+
   |                  |
   v                  v
Auth Module      Schedule Module
   |                  |
   v                  v
Service            Service
   |                  |
   v                  v
Repository        Repository
   |                  |
   +--------+---------+
            |
            v
        PostgreSQL
          (GORM)
```

Migration schema dikelola oleh `golang-migrate`.

Swagger digunakan untuk dokumentasi API.

Mermaid digunakan untuk diagram desain.

## 3. Technology Stack

| Area | Technology |
|---|---|
| Language | Go |
| HTTP Framework | Gin |
| ORM | GORM |
| Database | PostgreSQL |
| Authentication | JWT |
| Password Hashing | bcrypt |
| Migration | golang-migrate |
| API Documentation | Swagger / OpenAPI |
| Diagram | Mermaid |
| Container | Docker Compose |
| Testing | Go testing + httptest |

## 4. Project Structure

```text
cinema-ticket-system/
├── cmd/
│   └── api/
│       └── main.go
│
├── internal/
│   ├── auth/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   ├── model.go
│   │   └── jwt.go
│   │
│   ├── schedule/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   ├── model.go
│   │   └── dto.go
│   │
│   ├── middleware/
│   │   └── auth.go
│   │
│   ├── database/
│   │   └── postgres.go
│   │
│   └── config/
│       └── config.go
│
├── migrations/
├── docs/
│   ├── A-system-design.md
│   ├── B-database-design.md
│   └── diagrams/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── go.mod
└── go.sum
```

## 5. Indeks Berkas & Dokumentasi

| File | Tipe | Deskripsi |
|---|---|---|
| [`A-system-design.md`](A-system-design.md) | Jawaban Soal A | Analisis System Design, arsitektur, concurrency seat-locking, restok, & refund |
| [`B-database-design.md`](B-database-design.md) | Jawaban Soal B | Analisis skema 13 tabel relasional, normalisasi 3NF, dan strategi indexing |
| [`C-api-spec.md`](C-api-spec.md) | Jawaban Soal C | Kontrak spesifikasi API Golang (Auth JWT & CRUD Jadwal Tayang) |
| [`system-topology.jpg`](system-topology.jpg) | Diagram Gambar | Topologi arsitektur cloud skala nasional resolusi tinggi (150 DPI) |
| [`database-erd.jpg`](database-erd.jpg) | Diagram Gambar | Entity Relationship Diagram (ERD) visual 13 tabel relasional |
| [`flowchart-pemesanan.jpg`](flowchart-pemesanan.jpg) | Diagram Gambar | Flowchart alur pemesanan, restok tiket otomatis, dan pembatalan refund |
| [`skema_dan_data_awal_bioskop.sql`](skema_dan_data_awal_bioskop.sql) | SQL Script | Skrip DDL PostgreSQL 13 tabel dan data awal seeder siap impor |
| [`Cinema_Ticket_System.postman_collection.json`](Cinema_Ticket_System.postman_collection.json) | Koleksi Postman | Export Postman Collection v2.1 siap pakai dengan script auto-token |
| [`diagrams/system-flow.md`](diagrams/system-flow.md) | Mermaid Diagram | Flowchart alur sistem utama pemesanan |
| [`diagrams/booking-flow.md`](diagrams/booking-flow.md) | Mermaid Diagram | Flowchart konkurensi penguncian kursi (seat locking) |
| [`diagrams/refund-flow.md`](diagrams/refund-flow.md) | Mermaid Diagram | Flowchart pembatalan jadwal dan alur pengembalian dana |
| [`diagrams/erd.md`](diagrams/erd.md) | Mermaid Diagram | Skrip diagram ERD berbasis teks Mermaid |
| [`swagger/`](swagger/) | OpenAPI Spec | Berkas spesifikasi interaktif Swagger (JSON, YAML, Go) |
| [`modules/`](modules/README.md) | Penjelasan Arsitektur | Penjelasan komprehensif modul `internal/auth`, `internal/middleware`, dan `internal/schedule` |

## 6. Menjalankan Proyek

### Prasyarat

- Go 1.22+
- Docker & Docker Compose

### 1. Jalankan PostgreSQL via Docker

```bash
docker compose up -d
```

Verifikasi kontainer:

```bash
docker compose ps
```

### 2. Konfigurasi Variabel Lingkungan

```bash
cp .env.example .env
```

### 3. Jalankan Migrasi Database & Seeder Data Awal

```bash
go run cmd/migrate/main.go -seed
```
*Atau alternatif via skrip SQL mandiri:*
```bash
psql -h localhost -p 5432 -U bioskop -d bioskop -f docs/skema_dan_data_awal_bioskop.sql
```

### 4. Jalankan Server API

```bash
go run cmd/api/main.go
```
*Server aktif di `http://localhost:8088`. Buka browser untuk Swagger UI otomatis: `http://localhost:8088/swagger/index.html`*

### 5. Jalankan Seluruh Automated Tests

```bash
go test -v -race -count=1 ./...
```

### 6. Regenerasi Dokumentasi Swagger (Opsional)

```bash
swag init -g cmd/api/main.go -o docs/swagger
```

## 7. Design Principles

### Database is the source of truth for seat state

Seat availability should not depend only on an application cache.

### Concurrency is handled with database transactions and row-level locking

For the same schedule and seat:

```text
AVAILABLE -> HELD -> SOLD
```

Only one transaction may successfully change the seat from `AVAILABLE` to `HELD`.

### Idempotency solves duplicate requests

Idempotency is useful for payment/order/refund operations that may be retried.

It is different from row locking.

### Transaction history is preserved

Cancelled or refunded transactions should not simply be deleted.

### Implementation scope remains small

The full system is designed in A and B, while C implements only:

- Login
- JWT Authorization
- Schedule CRUD
