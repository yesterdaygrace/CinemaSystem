# Daftar Tugas: Sistem Tiket Bioskop

## Fase 1: Fondasi Lingkungan & Proyek

### Tugas 1.1: Inisialisasi Proyek & Penyiapan Dependensi
**Deskripsi:** Inisialisasi modul Go (`go.mod`), konfigurasi `.mise.toml` untuk mengunci Go 1.22+, pembuatan struktur direktori sesuai ketentuan pada `docs/README.md`, dan penambahan dependensi utama (Gin, GORM, driver postgres, golang-jwt/jwt/v5, bcrypt, godotenv).
**Kriteria Penerimaan:**
- [x] `go.mod` terbuat dengan nama modul `cinema-ticket-system`
- [x] Dependensi inti berhasil diunduh dan tersinkronisasi
- [x] Struktur folder direktori terbuat rapi
**Verifikasi:**
- [x] `go mod tidy` selesai dengan kode keluar 0
- [x] `go build ./...` berhasil tanpa error
**Ketergantungan:** Tidak ada
**Berkas Terkait:**
- `go.mod`
- `go.sum`
- `mise.toml`
**Estimasi Ruang Lingkup:** Kecil (2-3 berkas)

---

### Tugas 1.2: Konfigurasi Lingkungan & Infrastruktur Docker
**Deskripsi:** Konfigurasi `.env.example`, `.env`, `.gitignore`, dan `docker-compose.yml` untuk menjalankan container PostgreSQL 15 pada port 5432 dengan kredensial database terstandar.
**Kriteria Penerimaan:**
- [x] `docker-compose.yml` memuat layanan PostgreSQL dengan persistensi volume dan healthcheck
- [x] `.env.example` mendokumentasikan parameter wajib (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `PORT`, `JWT_SECRET`, `JWT_EXPIRES_HOURS`)
- [x] `.gitignore` mengamankan berkas binary, .env, dan berkas sementara
**Verifikasi:**
- [x] `docker compose config` tervalidasi tanpa error
- [x] Layanan PostgreSQL berjalan normal
**Ketergantungan:** Tugas 1.1
**Berkas Terkait:**
- `docker-compose.yml`
- `.env.example`
- `.env`
- `.gitignore`
**Estimasi Ruang Lingkup:** Kecil (3 berkas)

---

### Tugas 1.3: Lapisan Konfigurasi dan Koneksi Database
**Deskripsi:** Implementasi `internal/config/config.go` untuk memuat variabel lingkungan dan `internal/database/postgres.go` untuk membangun koneksi GORM ke PostgreSQL lengkap dengan konfigurasi *connection pooling* (`SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`).
**Kriteria Penerimaan:**
- [x] Struct konfigurasi memuat dan memvalidasi seluruh variabel lingkungan dengan nilai bawaan
- [x] Konektor database mengonfigurasi parameter connection pool
- [x] Mengembalikan pesan error jelas apabila koneksi gagal
**Verifikasi:**
- [x] Fungsi koneksi database teruji dan berhasil terhubung
**Ketergantungan:** Tugas 1.2
**Berkas Terkait:**
- `internal/config/config.go`
- `internal/database/postgres.go`
**Estimasi Ruang Lingkup:** Kecil (2 berkas)

---

### Titik Periksa: Fondasi
- [x] Proyek dapat di-compile dengan bersih
- [x] Konfigurasi dan modul koneksi database terverifikasi

---

## Fase 2: Skema Database, Migrasi & Data Awal (Seeder)

### Tugas 2.1: Migrasi SQL untuk Skema Relasional
**Deskripsi:** Pembuatan berkas migrasi SQL berurutan pada `migrations/` sesuai spesifikasi `docs/B-database-design.md` (`users`, `cinemas`, `studios`, `seats`, `movies`, `schedules`, `show_seats`, `orders`, `order_items`, `payments`, `tickets`, `refunds`, `audit_logs`).
**Kriteria Penerimaan:**
- [x] Skrip migrasi SQL berurutan dilengkapi berkas `.up.sql` dan `.down.sql`
- [x] Primary key, foreign key, batasan unik (`email`, `schedule_id + seat_id`), dan indeks terdefinisi lengkap
- [x] Runner migrasi Go programatik tersedia untuk eksekusi mandiri
**Verifikasi:**
- [x] Migrasi berhasil dieksekusi terhadap database PostgreSQL
**Ketergantungan:** Tugas 1.3
**Berkas Terkait:**
- `migrations/*.up.sql` dan `migrations/*.down.sql` (13 pasang)
- `internal/database/migrate.go`
**Estimasi Ruang Lingkup:** Menengah (13 pasang berkas migrasi + runner)

---

### Tugas 2.2: Seeder Database untuk Data Awal
**Deskripsi:** Implementasi mekanisme pengisian data awal (`internal/database/seed.go`) untuk akun Admin (`admin@example.com` / `password123` dengan peran `ADMIN`), Customer (`customer@example.com` / `password123` dengan peran `CUSTOMER`), bioskop contoh, studio, kursi, film, dan jadwal tayang awal.
**Kriteria Penerimaan:**
- [x] Kata sandi di-hash menggunakan algoritma bcrypt (faktor biaya >= 10)
- [x] Menggunakan nama dan deskripsi berbahasa Indonesia
- [x] Fungsi seeder bersifat idempoten (tidak menduplikasi baris jika sudah ada)
**Verifikasi:**
- [x] Data berhasil masuk ke tabel `users`, `cinemas`, `studios`, `seats`, `movies`, `schedules`
**Ketergantungan:** Tugas 2.1
**Berkas Terkait:**
- `internal/database/seed.go`
- `cmd/migrate/main.go`
**Estimasi Ruang Lingkup:** Kecil (1-2 berkas)

---

### Titik Periksa: Database & Migrasi
- [x] Seluruh migrasi teraplikasikan dengan sukses
- [x] Database terisi data awal tanpa kendala

---

## Fase 3: Autentikasi & Middleware Otorisasi

### Tugas 3.1: Model Autentikasi, Repositori, dan Utilitas JWT
**Deskripsi:** Implementasi model entitas `User`, antarmuka `UserRepository` (pencarian berdasarkan email dan ID), serta pembantu utilitas JWT pada `internal/auth/` untuk pembuatan dan verifikasi token dengan klaim `sub`, `role`, `iat`, dan `exp`.
**Kriteria Penerimaan:**
- [x] `GenerateToken` menghasilkan token JWT valid dengan masa aktif yang dapat dikonfigurasi
- [x] `ValidateToken` mem-parsing dan memverifikasi tanda tangan serta klaim peran
- [x] `UserRepository.FindByEmail` mengambil data pengguna secara aman
**Verifikasi:**
- [x] Pengujian unit pembuatan dan validasi token JWT lulus
**Ketergantungan:** Tugas 2.2
**Berkas Terkait:**
- `internal/auth/model.go`
- `internal/auth/jwt.go`
- `internal/auth/repository.go`
- `internal/auth/jwt_test.go`
**Estimasi Ruang Lingkup:** Menengah (4 berkas)

---

### Tugas 3.2: Service Autentikasi, Handler, dan Endpoint Login
**Deskripsi:** Implementasi `AuthService` dan `AuthHandler` untuk endpoint `POST /api/v1/auth/login`. Memverifikasi kata sandi dengan bcrypt dan mengembalikan respons terstandar (`access_token`, `token_type`, `expires_in` pada status 200, dan format error `{ "error": { "code": "INVALID_CREDENTIALS", "message": "..." } }` pada status 401).
**Kriteria Penerimaan:**
- [x] Kata sandi benar mengembalikan HTTP 200 disertai token JWT dan metadata
- [x] Kredensial tidak valid mengembalikan HTTP 401 dengan format error standar
- [x] Payload tidak valid mengembalikan HTTP 400 dengan kode `INVALID_REQUEST`
**Verifikasi:**
- [x] Pengujian integrasi handler via `httptest` memvalidasi skenario sukses dan gagal
**Ketergantungan:** Tugas 3.1
**Berkas Terkait:**
- `internal/auth/service.go`
- `internal/auth/handler.go`
**Estimasi Ruang Lingkup:** Menengah (2 berkas)

---

### Tugas 3.3: Middleware Gin untuk JWT Auth & RBAC
**Deskripsi:** Implementasi middleware `internal/middleware/auth.go` yang memeriksa header `Authorization: Bearer <token>`, memvalidasi token JWT, menyematkan user ID dan peran ke context Gin, serta menyediakan penjaga akses berbasis peran (`RequireRoles("ADMIN")`).
**Kriteria Penerimaan:**
- [x] Header otorisasi tidak ada atau keliru mengembalikan 401 `UNAUTHORIZED`
- [x] Token kedaluwarsa atau tidak valid mengembalikan 401 `INVALID_TOKEN`
- [x] Peran pengguna tidak memiliki hak akses mengembalikan 403 `FORBIDDEN`
- [x] Token valid mengizinkan request berlanjut dengan konteks terisi
**Verifikasi:**
- [x] Pengujian middleware memvalidasi skenario 200, 401, dan 403
**Ketergantungan:** Tugas 3.2
**Berkas Terkait:**
- `internal/middleware/auth.go`
- `internal/middleware/auth_test.go`
**Estimasi Ruang Lingkup:** Kecil (2 berkas)

---

### Titik Periksa: Autentikasi & Otorisasi
- [x] Endpoint login berfungsi sesuai kontrak spesifikasi
- [x] Middleware RBAC membatasi pengguna biasa dan meloloskan admin

---

## Fase 4: Implementasi Modul Jadwal Tayang (Schedule)

### Tugas 4.1: Model Jadwal, DTO & Validasi
**Deskripsi:** Implementasi model domain Schedule dan DTO pada `internal/schedule/model.go` dan `dto.go`. Menetapkan aturan validasi data (`movie_id > 0`, `studio_id > 0`, timestamp RFC3339 valid, `end_time > start_time`).
**Kriteria Penerimaan:**
- [x] Model sesuai dengan tabel database `schedules`
- [x] DTO request dan response terdefinisi rapi
- [x] Validasi menangkap input tidak valid dan memastikan `end_time > start_time`
**Verifikasi:**
- [x] Pengujian unit validasi DTO lulus
**Ketergantungan:** Tugas 3.3
**Berkas Terkait:**
- `internal/schedule/model.go`
- `internal/schedule/dto.go`
**Estimasi Ruang Lingkup:** Kecil (2 berkas)

---

### Tugas 4.2: Repositori Jadwal & Pengecekan Overlap
**Deskripsi:** Implementasi `internal/schedule/repository.go` dengan method GORM: `FindAll`, `FindByID`, `Create`, `Update`, `Cancel` (pembatalan logis status `CANCELLED`), dan `HasOverlap(studioID, startTime, endTime, excludeScheduleID)`.
**Kriteria Penerimaan:**
- [x] Query `HasOverlap` mengecek bentrokan waktu: `start_time < :new_end AND end_time > :new_start AND status != 'CANCELLED'`
- [x] Mengabaikan ID jadwal saat operasi pembaruan (update)
- [x] Pembatalan logis mengubah status tanpa menghapus baris data
**Verifikasi:**
- [x] Query overlap teruji secara akurat
**Ketergantungan:** Tugas 4.1
**Berkas Terkait:**
- `internal/schedule/repository.go`
**Estimasi Ruang Lingkup:** Kecil (1-2 berkas)

---

### Tugas 4.3: Logika Bisnis Service Jadwal
**Deskripsi:** Implementasi `internal/schedule/service.go` yang memuat logika bisnis pengelolaan jadwal: validasi rentang waktu dan penolakan konflik jadwal tayang (mengembalikan error `SCHEDULE_CONFLICT` -> HTTP 409).
**Kriteria Penerimaan:**
- [x] Pembuatan jadwal bentrok pada studio sama ditolak dengan error konflik
- [x] Pembaruan jadwal bentrok ditolak dengan error konflik
- [x] Pembatalan jadwal tidak ditemukan mengembalikan error `SCHEDULE_NOT_FOUND` -> HTTP 404
**Verifikasi:**
- [x] Pengujian unit service dengan mock repository memvalidasi skenario bentrok dan normal
**Ketergantungan:** Tugas 4.2
**Berkas Terkait:**
- `internal/schedule/service.go`
- `internal/schedule/service_test.go`
**Estimasi Ruang Lingkup:** Menengah (2 berkas)

---

### Tugas 4.4: Handler & Routing Jadwal Tayang
**Deskripsi:** Implementasi `internal/schedule/handler.go` dengan endpoint HTTP:
- `GET /api/v1/schedules` (CUSTOMER & ADMIN)
- `GET /api/v1/schedules/:id` (CUSTOMER & ADMIN)
- `POST /api/v1/schedules` (Hanya ADMIN, HTTP 201)
- `PUT /api/v1/schedules/:id` (Hanya ADMIN, HTTP 200)
- `DELETE /api/v1/schedules/:id` (Hanya ADMIN, HTTP 204)
**Kriteria Penerimaan:**
- [x] Status code sesuai spesifikasi: 200, 201, 204, 400, 401, 403, 404, 409
- [x] Format error konsisten `{ "error": { "code": "...", "message": "..." } }`
**Verifikasi:**
- [x] Pengujian integrasi handler untuk seluruh endpoint
**Ketergantungan:** Tugas 4.3
**Berkas Terkait:**
- `internal/schedule/handler.go`
**Estimasi Ruang Lingkup:** Menengah (1 berkas)

---

### Titik Periksa: Modul Jadwal Tayang
- [x] Seluruh endpoint CRUD jadwal operasional
- [x] Pembatasan hak akses peran dan validasi konflik bisnis aktif

---

## Fase 5: Dokumentasi Swagger & Server Entrypoint

### Tugas 5.1: Anotasi Swagger & Pembangkitan Dokumen
**Deskripsi:** Penambahan komentar deklaratif Swagger pada seluruh handler dan `main.go`. Menghasilkan spesifikasi OpenAPI ke dalam `docs/swagger/` menggunakan alat Swag.
**Kriteria Penerimaan:**
- [x] Seluruh endpoint, payload body, parameter, skema keamanan Bearer JWT, dan respons terdokumentasi
- [x] Pembangkitan menghasilkan `swagger.json` dan `swagger.yaml` yang valid
**Verifikasi:**
- [x] `swag init` menghasilkan dokumen tanpa galat
**Ketergantungan:** Tugas 4.4
**Berkas Terkait:**
- `cmd/api/main.go`
- `internal/auth/handler.go`
- `internal/schedule/handler.go`
- `docs/swagger/*`
**Estimasi Ruang Lingkup:** Kecil (3 berkas + dokumen hasil generate)

---

### Tugas 5.2: Perakitan Server & Rute Aplikasi
**Deskripsi:** Implementasi `cmd/api/main.go` yang merakit konfigurasi, koneksi database, middleware, router autentikasi, router jadwal, dan Swagger UI di `/swagger/*any` disertai mekanisme *graceful shutdown*.
**Kriteria Penerimaan:**
- [x] Server menginisialisasi dependensi dan mengikat rute dengan bersih
- [x] Swagger UI dapat dibuka pada browser
- [x] Server mati dengan aman saat menerima sinyal SIGINT/SIGTERM
**Verifikasi:**
- [x] Server berhasil dijalankan dan melayani request HTTP
**Ketergantungan:** Tugas 5.1
**Berkas Terkait:**
- `cmd/api/main.go`
**Estimasi Ruang Lingkup:** Kecil (1 berkas)

---

## Fase 6: Pengujian End-to-End Otomatis & Dokumentasi

### Tugas 6.1: Pengujian Integrasi End-to-End
**Deskripsi:** Pembuatan rangkaian pengujian integrasi komprehensif pada `tests/api_test.go` yang menyimulasikan alur kerja pengguna nyata: login customer, login admin, pembuatan jadwal oleh admin, penolakan konflik jadwal bentrok, customer melihat jadwal, penolakan hak akses customer (403), pembaruan jadwal, dan pembatalan logis.
**Kriteria Penerimaan:**
- [x] Seluruh perjalanan pengguna teruji end-to-end
- [x] Kondisi batas dan skenario error terverifikasi
**Verifikasi:**
- [x] `go test -v ./tests/...` lulus 100%
**Ketergantungan:** Tugas 5.2
**Berkas Terkait:**
- `tests/api_test.go`
**Estimasi Ruang Lingkup:** Menengah (1 berkas)

---

### Tugas 6.2: Dokumentasi README & Verifikasi Operasional
**Deskripsi:** Pembuatan dan pembaruan `README.md` utama dengan instruksi lengkap berbahasa Indonesia untuk menjalankan proyek via Docker, migrasi, seeding, testing, dan contoh request cURL.
**Kriteria Penerimaan:**
- [x] Instruksi akurat dan terverifikasi terhadap perintah nyata
- [x] Contoh request cURL lengkap disediakan untuk pengujian manual
**Verifikasi:**
- [x] Seluruh perintah pada README dieksekusi tanpa kendala
**Ketergantungan:** Tugas 6.1
**Berkas Terkait:**
- `README.md`
**Estimasi Ruang Lingkup:** Kecil (1 berkas)

---

### Titik Periksa: Verifikasi Selesai
- [x] Seluruh pengujian unit, integrasi, dan end-to-end lulus (`go test ./...`)
- [x] Docker compose dan migrasi berjalan mulus
- [x] Siap untuk serah terima produksi
