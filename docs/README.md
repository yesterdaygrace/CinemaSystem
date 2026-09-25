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

## 5. Dokumentasi

| File | Isi |
|---|---|
| `docs/A-system-design.md` | Jawaban System Design Test |
| `docs/B-database-design.md` | Jawaban Database Design Test |
| `docs/C-api-spec.md` | Kontrak API implementasi |
| `docs/diagrams/system-flow.md` | Flowchart utama |
| `docs/diagrams/booking-flow.md` | Flow pemilihan dan penguncian kursi |
| `docs/diagrams/refund-flow.md` | Flow pembatalan dan refund |
| `docs/diagrams/erd.md` | ERD |

## 6. Running the Project

### Prerequisites

- Go
- Docker
- Docker Compose
- golang-migrate
- Swag CLI

### Start PostgreSQL

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

### Configure environment

```bash
cp .env.example .env
```

### Run migration

```bash
migrate \
  -path migrations \
  -database "postgres://cinema:cinema_dev@localhost:5432/cinema?sslmode=disable" \
  up
```

### Run API

```bash
go run ./cmd/api
```

### Run tests

```bash
go test ./...
```

### Generate Swagger

```bash
swag init -g cmd/api/main.go
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
