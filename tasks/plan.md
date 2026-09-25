# Rencana Implementasi: Sistem Tiket Bioskop (Golang + Gin + PostgreSQL)

## 1. Ringkasan
Sistem Tiket Bioskop adalah aplikasi backend yang dirancang untuk jaringan bioskop skala nasional yang mampu menangani penelusuran jadwal secara bersamaan (konkurensi), reservasi kursi, dan transaksi pemesanan. Berdasarkan dokumen desain sistem di folder `docs/` (`A-system-design.md`, `B-database-design.md`, `C-api-spec.md`, dan diagram alur), proyek ini mengimplementasikan layanan backend Golang dengan arsitektur **Modular Monolith** menggunakan **Gin**, **GORM**, **PostgreSQL**, **golang-migrate**, **JWT auth**, dan **Swagger/OpenAPI**.

Fokus cakupan implementasi:
1. **Autentikasi & Otorisasi Pengguna**: Login dengan verifikasi sandi bcrypt, penerbitan token JWT dengan peran (`CUSTOMER`, `ADMIN`), dan middleware otentikasi Gin untuk kontrol akses endpoint berbasis peran.
2. **Manajemen Jadwal Tayang (Schedule)**: Operasi CRUD penuh untuk jadwal tayang film (`GET /schedules`, `GET /schedules/:id`, `POST /schedules`, `PUT /schedules/:id`, `DELETE /schedules/:id`), termasuk validasi aturan bisnis (mencegah jadwal tayang tumpang tindih pada studio yang sama) dan pembatalan logis (*logical deletion/cancellation*).
3. **Database & Infrastruktur**: Docker Compose untuk PostgreSQL, migrasi database skema relasional terstruktur, pengelolaan *connection pooling*, dan seeder data awal.
4. **Dokumentasi API & Penjaminan Kualitas**: Dokumentasi Swagger terintegrasi (`/swagger/index.html`), respons error seragam, dan pengujian otomatis menyeluruh (*unit test* dan *integration test*).

---

## 2. Keputusan Desain & Arsitektur

### 2.1 Arsitektur Berlapis Bersih dalam Modular Monolith
Mengikuti struktur proyek pada `docs/README.md`:
```
cmd/api/main.go
  ├── internal/config (Pemuat konfigurasi environment)
  ├── internal/database (Pengelola koneksi GORM PostgreSQL & connection pool)
  ├── internal/middleware (Validator JWT, penjaga peran RBAC, logger, recovery)
  ├── internal/auth (Handler -> Service -> Repository -> Model/JWT)
  └── internal/schedule (Handler -> Service -> Repository -> Model/DTO)
```
- **Lapisan Handler**: Mem-parsing request HTTP, validasi input, pemetaan DTO, dan serialisasi respons sesuai format baku pada `docs/C-api-spec.md`.
- **Lapisan Service**: Menjalankan logika bisnis murni, menegakkan aturan peran, memvalidasi rentang waktu jadwal (`end_time > start_time`), dan memeriksa bentrokan jadwal studio.
- **Lapisan Repository**: Mengenkapsulasi query dan persistensi data ke database melalui GORM.
- **Format Error Seragam**:
  ```json
  {
    "error": {
      "code": "KODE_ERROR",
      "message": "Pesan deskriptif"
    }
  }
  ```

### 2.2 Pencegahan Konflik Jadwal Studio (Overlap Validation)
Untuk mencegah satu ruangan studio fisik digunakan oleh dua penayangan pada waktu bersamaan:
- Jadwal baru atau pembaruan $[start\_time_A, end\_time_A]$ bertabrakan dengan jadwal yang sudah ada $[start\_time_B, end\_time_B]$ pada studio yang sama jika:
  $$\max(start\_time_A, start\_time_B) < \min(end\_time_A, end\_time_B)$$
  dan status jadwal bukan `CANCELLED`.
- Konflik mengembalikan respons HTTP `409 Conflict` dengan kode `SCHEDULE_CONFLICT`.

### 2.3 Pembatalan Logis (Logical Cancellation)
Sesuai `docs/C-api-spec.md` dan alur refund pada `docs/refund-flow.md`, penghapusan jadwal tidak boleh menghancurkan histori transaksi:
`DELETE /schedules/:id` memperbarui status:
`SCHEDULED` $\rightarrow$ `CANCELLED`.

---

## 3. Urutan Ketergantungan & Implementasi

```
1. Lingkungan & Go Toolchain (Mise go@1.22.12, go.mod, docker-compose)
       │
2. Konfigurasi & Koneksi Database (GORM + Connection Pool)
       │
3. Migrasi Database & Seeder Data (000001_users hingga 000006_schedules + Data Awal)
       │
4. Modul Autentikasi (bcrypt, klaim JWT, login handler, middleware auth)
       │
5. Modul Jadwal Tayang (DTO, Validasi Overlap, CRUD Jadwal, Pembatalan Logis)
       │
6. Dokumentasi Swagger & Integrasi Router (swag annotations + gin-swagger)
       │
7. Pengujian Otomatis Unit & Integrasi End-to-End
```

---

## 4. Rincian Fase Implementasi

### Fase 1: Fondasi Lingkungan & Proyek
- **Tugas 1.1**: Inisialisasi Modul Go & Dependensi (`go.mod`, Gin, GORM, driver PostgreSQL, golang-jwt, bcrypt, godotenv).
- **Tugas 1.2**: Konfigurasi Docker Compose & Variabel Lingkungan (`postgres:15-alpine`, database cinema, user credentials).
- **Tugas 1.3**: Implementasi Konfigurasi & Pengelola Koneksi Database (`internal/config`, `internal/database`) dengan pengaturan *connection pooling*.

### Fase 2: Skema Database & Migrasi
- **Tugas 2.1**: Implementasi migrasi SQL bertahap (`migrations/000001_users` hingga `000013_audit_logs`) dengan skrip `up` dan `down`.
- **Tugas 2.2**: Implementasi Seeder Data untuk mengisi akun default Admin (`admin@example.com` / `password123`), Customer (`customer@example.com` / `password123`), contoh Bioskop, Studio, Kursi, Film, dan Jadwal awal.

### Fase 3: Autentikasi & Middleware
- **Tugas 3.1**: Implementasi Model Pengguna, Repositori, Utilitas JWT, dan Service Autentikasi (`internal/auth`).
- **Tugas 3.2**: Implementasi Handler Autentikasi (`POST /api/v1/auth/login`) dengan penanganan kode error (`INVALID_CREDENTIALS`, `INVALID_REQUEST`).
- **Tugas 3.3**: Implementasi Middleware JWT Auth & RBAC (`internal/middleware/auth.go`) yang memeriksa peran pengguna (`ADMIN`, `CUSTOMER`).

### Fase 4: Modul Jadwal Tayang (Schedule)
- **Tugas 4.1**: Implementasi Model Jadwal & DTO (`internal/schedule/model.go`, `dto.go`).
- **Tugas 4.2**: Implementasi Repositori Jadwal (`internal/schedule/repository.go`) dengan query pengecekan tumpang tindih waktu (*overlap*).
- **Tugas 4.3**: Implementasi Logika Bisnis Service Jadwal (`internal/schedule/service.go`) untuk validasi rentang waktu dan penolakan konflik jadwal.
- **Tugas 4.4**: Implementasi Handler & Routing Jadwal (`GET`, `GET :id`, `POST`, `PUT :id`, `DELETE :id`).

### Fase 5: Dokumentasi Swagger & Server Entrypoint
- **Tugas 5.1**: Penambahan anotasi Swagger pada seluruh handler dan regenerasi dokumentasi menggunakan `swag`.
- **Tugas 5.2**: Pengkabelan seluruh rute di `cmd/api/main.go` dan penyajian antarmuka Swagger UI di `/swagger/index.html`.

### Fase 6: Pengujian Otomatis & Verifikasi
- **Tugas 6.1**: Pengujian Unit & Logika Bisnis (pembuatan dan validasi token JWT, deteksi overlap jadwal).
- **Tugas 6.2**: Pengujian Integrasi HTTP API (`httptest`) yang mencakup seluruh endpoint, hak akses peran, pencegahan konflik, dan pembatalan logis.

---

## 5. Manajemen Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Race condition saat membuat jadwal bersamaan | Tinggi | Validasi overlap di lapisan service dan query filter terindeks pada rentang waktu studio. |
| Perbedaan zona waktu | Sedang | Seluruh timestamp disimpan dalam format UTC dengan standar ISO 8601 (`time.RFC3339`). |
| Binary CLI migrate tidak terpasang di host | Rendah | Menyediakan runner migrasi Go programatik mandiri di dalam proyek (`cmd/migrate/main.go`). |
| Kadaluarsa token JWT | Rendah | Menggunakan klaim standar dengan waktu kedaluwarsa terukur (24 jam). |
