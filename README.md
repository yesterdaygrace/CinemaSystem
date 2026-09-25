# Cinema Ticket System (Golang + Gin + PostgreSQL)

> **Technical Assessment - Tim MKP (Mitra Kasih Perkasa)**  
> **Nama Lengkap Kandidat:** Kevan Deschans (vinkanaka)  
> **Email:** kevandeschans@gmail.com  
> **Posisi:** Backend Engineer  

Sistem backend pembelian tiket bioskop online untuk skala nasional dengan banyak cabang, proteksi konkurensi jadwal tayang, validasi konflik jadwal per studio, pembatalan logis, otentikasi JWT dengan role-based access control (`ADMIN` dan `CUSTOMER`), dokumentasi Swagger, serta migrasi database relasional.

---

## 📋 Berkas Jawaban & Deliverables Tes MKP

| Poin Instruksi | Berkas / Tautan | Keterangan |
|---|---|---|
| **1. System Design (Topologi JPG)** | [**`docs/system-topology.jpg`**](docs/system-topology.jpg)<br>[**`docs/flowchart-pemesanan.jpg`**](docs/flowchart-pemesanan.jpg)<br>[**`docs/A-system-design.md`**](docs/A-system-design.md) | Diagram topologi arsitektur cloud skala nasional (Redis, Kafka, Multi-AZ DB), flowchart alur pemesanan awam, mekanisme seat-locking, restok tiket, dan auto-refund |
| **2. Database Design (ERD JPG & SQL)** | [**`docs/database-erd.jpg`**](docs/database-erd.jpg)<br>[**`docs/skema_dan_data_awal_bioskop.sql`**](docs/skema_dan_data_awal_bioskop.sql)<br>[**`docs/B-database-design.md`**](docs/B-database-design.md) | Diagram relasi 13 tabel (ERD), skrip import DDL PostgreSQL + data awal siap impor |
| **3. Skill Test (Golang API)** | [**`cmd/api/main.go`**](cmd/api/main.go)<br>[**`internal/schedule/`**](internal/schedule/)<br>[**`internal/auth/`**](internal/auth/) | Implementasi RESTful API Golang + Gin + GORM + PostgreSQL: Login User JWT & CRUD Jadwal dengan proteksi overlap 409 Conflict |
| **4. Export Postman Collection** | [**`docs/Cinema_Ticket_System.postman_collection.json`**](docs/Cinema_Ticket_System.postman_collection.json) | Koleksi Postman lengkap dengan script auto-save token JWT dan uji skenario sukses/gagal (200, 201, 204, 401, 403, 409) |

---

## 1. Arsitektur & Teknologi

Sistem dibangun menggunakan pola **Modular Monolith** dengan layering:
```
Handler (HTTP Parsing, Validation & DTOs)
   ↓
Service (Business Logic, Validation, Overlap Check)
   ↓
Repository (Database Queries & Persistence)
   ↓
GORM ORM + PostgreSQL Driver
   ↓
PostgreSQL 15 (Docker)
```

| Komponen | Teknologi |
|---|---|
| Bahasa | Go 1.22+ / 1.26 |
| HTTP Router | Gin (`github.com/gin-gonic/gin`) |
| ORM | GORM (`gorm.io/gorm`) |
| Database | PostgreSQL 15 |
| Migrasi Database | `golang-migrate` (`github.com/golang-migrate/migrate/v4`) |
| Autentikasi | JWT (`github.com/golang-jwt/jwt/v5`) + bcrypt |
| API Docs | Swagger / OpenAPI (`github.com/swaggo/gin-swagger`) |
| Container | Docker & Docker Compose |
| Testing | Go testing + `net/http/httptest` |

---

## 2. Struktur Proyek

```text
.
├── cmd/
│   ├── api/
│   │   └── main.go              # Server entrypoint & routing
│   └── migrate/
│       └── main.go              # Database migration & seeder CLI
├── docs/
│   ├── A-system-design.md       # Jawaban System Design Test
│   ├── B-database-design.md     # Jawaban Database Design Test
│   ├── C-api-spec.md            # Kontrak API implementasi
│   ├── swagger/                 # Swagger / OpenAPI generated files
│   └── *.md                     # Diagram & flowchart
├── internal/
│   ├── auth/                    # Modul Auth: Handler, Service, Repo, JWT, Model
│   ├── schedule/                # Modul Schedule: Handler, Service, Repo, DTO, Model
│   ├── middleware/              # Gin Auth Middleware (JWT & RBAC)
│   ├── database/                # GORM Connection pool, seeder, migrate runner
│   └── config/                  # Environment variable configuration
├── migrations/                  # 13 SQL migration files (.up.sql & .down.sql)
├── tests/
│   └── api_test.go              # E2E integration test suite
├── tasks/
│   ├── plan.md                  # Implementation plan
│   └── todo.md                  # Detailed task checklist
├── docker-compose.yml           # PostgreSQL container setup
├── .env.example                 # Template environment variables
├── .env                         # Local environment configuration
├── go.mod
└── go.sum
```

---

## 3. Menjalankan Aplikasi

### A. Prasyarat
- Go (1.22 atau lebih baru)
- Docker & Docker Compose

### B. Langkah Menjalankan

1. **Jalankan PostgreSQL via Docker Compose**:
   ```bash
   docker compose up -d
   ```
   *Container `bioskop_postgres` akan berjalan dengan database `bioskop` dan kredensial bawaan.*

2. **Konfigurasi Environment**:
   ```bash
   cp .env.example .env
   ```

3. **Jalankan Migrasi Database dan Seeder**:
   ```bash
   go run cmd/migrate/main.go -seed
   ```
   *Perintah ini akan menjalankan 13 file migrasi SQL berbahasa Indonesia dan mengisikan akun default admin, customer, studio, bioskop, film, dan jadwal.*

4. **Jalankan API Server**:
   ```bash
   go run cmd/api/main.go
   ```
   Server aktif di `http://localhost:8088` (atau port sesuai `.env`).

---

## 4. Swagger Documentation

Akses dokumentasi interaktif Swagger UI pada browser:
```text
http://localhost:8088/swagger/index.html
```

Untuk meregenerasi file swagger:
```bash
swag init -g cmd/api/main.go -o docs/swagger
```

---

## 5. Menjalankan Automated Tests

Jalankan seluruh unit test dan end-to-end integration test:
```bash
go test -v -count=1 ./...
```

Hasil test mencakup:
- Token JWT generation dan validation
- Middleware RBAC (200, 401 unauthorized, 403 forbidden)
- Login autentikasi dengan bcrypt
- Schedule CRUD
- Deteksi tumpang tindih waktu penayangan pada studio yang sama (HTTP 409 `SCHEDULE_CONFLICT`)
- Pembatalan logis schedule (HTTP 204 No Content dan status menjadi `CANCELLED`)

---

## 6. Akun Default (Seeded)

| Role | Email | Password | Izin |
|---|---|---|---|
| **ADMIN** | `admin@example.com` | `password123` | Read Schedules, Create, Update, Cancel Schedule |
| **CUSTOMER** | `customer@example.com` | `password123` | Read Schedules |

---

## 7. Contoh Pemanggilan API (cURL)

### A. Login Admin
```bash
curl -X POST http://localhost:8088/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```
Response:
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### B. Ambil Daftar Jadwal (Customer / Admin)
```bash
curl -X GET http://localhost:8088/api/v1/schedules \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### C. Buat Jadwal Baru (Admin Only)
```bash
curl -X POST http://localhost:8088/api/v1/schedules \
  -H "Authorization: Bearer <ADMIN_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "studio_id": 2,
    "start_time": "2026-10-02T19:00:00+07:00",
    "end_time": "2026-10-02T21:30:00+07:00"
  }'
```

### D. Cek Proteksi Konflik Jadwal (Studio Overlap)
Jika mengirim jadwal pada studio yang sama dengan rentang waktu yang bertabrakan:
```json
{
  "error": {
    "code": "SCHEDULE_CONFLICT",
    "message": "Studio already has an overlapping schedule"
  }
}
```
HTTP Status: `409 Conflict`.

### E. Pembatalan Jadwal (Admin Only)
```bash
curl -X DELETE http://localhost:8088/api/v1/schedules/1 \
  -H "Authorization: Bearer <ADMIN_JWT_TOKEN>"
```
HTTP Status: `204 No Content`. Jadwal diubah menjadi status `CANCELLED` tanpa menghapus riwayat data transaksi terkait.
