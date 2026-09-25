-- =============================================================================
-- SKRIP BASIS DATA SISTEM PEMESANAN TIKET BIOSKOP NASIONAL
-- Dialek: PostgreSQL 15+
-- Untuk Tim Penilai MKP (Mitra Kasih Perkasa)
-- 
-- Cara Menjalankan / Mengimpor:
--   psql -h localhost -p 5432 -U bioskop -d bioskop -f docs/skema_dan_data_awal_bioskop.sql
-- Atau melalui pgAdmin / DBeaver / Docker CLI:
--   docker compose exec -T postgres psql -U bioskop -d bioskop -f /path/skema.sql
-- =============================================================================

-- Pastikan ekstensi UUID aktif jika dibutuhkan
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 1. TABEL PENGGUNA (users)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pengguna (
    id BIGSERIAL PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hash_kata_sandi VARCHAR(255) NOT NULL,
    peran VARCHAR(50) NOT NULL DEFAULT 'CUSTOMER', -- 'ADMIN', 'CUSTOMER'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pengguna_email ON pengguna(email);
CREATE INDEX IF NOT EXISTS idx_pengguna_peran ON pengguna(peran);

-- =============================================================================
-- 2. TABEL BIOSKOP (cinemas)
-- =============================================================================
CREATE TABLE IF NOT EXISTS bioskop (
    id BIGSERIAL PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    kota VARCHAR(100) NOT NULL,
    alamat TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bioskop_kota ON bioskop(kota);

-- =============================================================================
-- 3. TABEL STUDIO (studios)
-- =============================================================================
CREATE TABLE IF NOT EXISTS studio (
    id BIGSERIAL PRIMARY KEY,
    bioskop_id BIGINT NOT NULL REFERENCES bioskop(id) ON DELETE CASCADE,
    nama VARCHAR(100) NOT NULL,
    kapasitas INT NOT NULL DEFAULT 0,
    tipe VARCHAR(50) NOT NULL DEFAULT 'REGULAR', -- 'REGULAR', 'IMAX', 'PREMIERE'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_studio_bioskop_id ON studio(bioskop_id);

-- =============================================================================
-- 4. TABEL KURSI (seats)
-- =============================================================================
CREATE TABLE IF NOT EXISTS kursi (
    id BIGSERIAL PRIMARY KEY,
    studio_id BIGINT NOT NULL REFERENCES studio(id) ON DELETE CASCADE,
    label_baris VARCHAR(10) NOT NULL,
    nomor_kursi INT NOT NULL,
    tipe_kursi VARCHAR(50) NOT NULL DEFAULT 'REGULAR',
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_studio_kursi UNIQUE (studio_id, label_baris, nomor_kursi)
);

CREATE INDEX IF NOT EXISTS idx_kursi_studio_id ON kursi(studio_id);

-- =============================================================================
-- 5. TABEL FILM (movies)
-- =============================================================================
CREATE TABLE IF NOT EXISTS film (
    id BIGSERIAL PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    deskripsi TEXT,
    durasi_menit INT NOT NULL,
    rating_usia VARCHAR(20) NOT NULL DEFAULT 'SU', -- 'SU', '13+', '17+', '21+'
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',  -- 'ACTIVE', 'ARCHIVED'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_film_judul ON film(judul);
CREATE INDEX IF NOT EXISTS idx_film_status ON film(status);

-- =============================================================================
-- 6. TABEL JADWAL TAYANG (schedules)
-- =============================================================================
CREATE TABLE IF NOT EXISTS jadwal (
    id BIGSERIAL PRIMARY KEY,
    film_id BIGINT NOT NULL REFERENCES film(id) ON DELETE RESTRICT,
    studio_id BIGINT NOT NULL REFERENCES studio(id) ON DELETE RESTRICT,
    waktu_mulai TIMESTAMP WITH TIME ZONE NOT NULL,
    waktu_selesai TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'SCHEDULED', -- 'SCHEDULED', 'COMPLETED', 'CANCELLED'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_waktu_jadwal CHECK (waktu_selesai > waktu_mulai)
);

CREATE INDEX IF NOT EXISTS idx_jadwal_studio_waktu ON jadwal(studio_id, waktu_mulai, waktu_selesai);
CREATE INDEX IF NOT EXISTS idx_jadwal_film_id ON jadwal(film_id);
CREATE INDEX IF NOT EXISTS idx_jadwal_status ON jadwal(status);

-- =============================================================================
-- 7. TABEL KURSI JADWAL (show_seats)
-- Menampung ketersediaan status kursi per jadwal penayangan
-- =============================================================================
CREATE TABLE IF NOT EXISTS kursi_jadwal (
    id BIGSERIAL PRIMARY KEY,
    jadwal_id BIGINT NOT NULL REFERENCES jadwal(id) ON DELETE CASCADE,
    kursi_id BIGINT NOT NULL REFERENCES kursi(id) ON DELETE RESTRICT,
    harga DECIMAL(12, 2) NOT NULL DEFAULT 50000.00,
    status VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'RESERVED', 'BOOKED'
    dipesan_sampai TIMESTAMP WITH TIME ZONE,
    versi INT NOT NULL DEFAULT 1, -- Optimistic locking
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_jadwal_kursi UNIQUE (jadwal_id, kursi_id)
);

CREATE INDEX IF NOT EXISTS idx_kursi_jadwal_status ON kursi_jadwal(jadwal_id, status);

-- =============================================================================
-- 8. TABEL PESANAN (orders)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pesanan (
    id BIGSERIAL PRIMARY KEY,
    kode_pesanan VARCHAR(100) NOT NULL UNIQUE,
    pengguna_id BIGINT NOT NULL REFERENCES pengguna(id) ON DELETE RESTRICT,
    jadwal_id BIGINT NOT NULL REFERENCES jadwal(id) ON DELETE RESTRICT,
    total_biaya DECIMAL(12, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'PAID', 'CANCELLED', 'EXPIRED'
    kadaluarsa_pada TIMESTAMP WITH TIME ZONE NOT NULL,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pesanan_kode ON pesanan(kode_pesanan);
CREATE INDEX IF NOT EXISTS idx_pesanan_pengguna_id ON pesanan(pengguna_id);
CREATE INDEX IF NOT EXISTS idx_pesanan_status ON pesanan(status);

-- =============================================================================
-- 9. TABEL ITEM PESANAN (order_items)
-- =============================================================================
CREATE TABLE IF NOT EXISTS item_pesanan (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    kursi_jadwal_id BIGINT NOT NULL REFERENCES kursi_jadwal(id) ON DELETE RESTRICT,
    harga DECIMAL(12, 2) NOT NULL,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_pesanan_kursi_jadwal UNIQUE (pesanan_id, kursi_jadwal_id)
);

-- =============================================================================
-- 10. TABEL PEMBAYARAN (payments)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pembayaran (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE RESTRICT,
    id_transaksi_gateway VARCHAR(255) NOT NULL UNIQUE,
    metode_pembayaran VARCHAR(50) NOT NULL, -- 'QRIS', 'VIRTUAL_ACCOUNT', 'CREDIT_CARD'
    nominal DECIMAL(12, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'SUCCESS', 'FAILED', 'REFUNDED'
    dibayar_pada TIMESTAMP WITH TIME ZONE,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pembayaran_pesanan_id ON pembayaran(pesanan_id);

-- =============================================================================
-- 11. TABEL TIKET (tickets)
-- =============================================================================
CREATE TABLE IF NOT EXISTS tiket (
    id BIGSERIAL PRIMARY KEY,
    kode_tiket VARCHAR(100) NOT NULL UNIQUE,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE RESTRICT,
    kursi_jadwal_id BIGINT NOT NULL REFERENCES kursi_jadwal(id) ON DELETE RESTRICT,
    status VARCHAR(50) NOT NULL DEFAULT 'ISSUED', -- 'ISSUED', 'USED', 'CANCELLED'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tiket_kode ON tiket(kode_tiket);

-- =============================================================================
-- 12. TABEL PENGEMBALIAN DANA (refunds)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pengembalian_dana (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE RESTRICT,
    alasan TEXT NOT NULL,
    nominal DECIMAL(12, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'PROCESSED', 'REJECTED'
    diproses_pada TIMESTAMP WITH TIME ZONE,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pengembalian_dana_pesanan_id ON pengembalian_dana(pesanan_id);

-- =============================================================================
-- 13. TABEL LOG AUDIT (audit_logs)
-- =============================================================================
CREATE TABLE IF NOT EXISTS log_audit (
    id BIGSERIAL PRIMARY KEY,
    nama_entitas VARCHAR(100) NOT NULL,
    id_entitas BIGINT NOT NULL,
    aksi VARCHAR(50) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE', 'CANCEL'
    diubah_oleh VARCHAR(255) NOT NULL,
    data_lama JSONB,
    data_baru JSONB,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_log_audit_entitas ON log_audit(nama_entitas, id_entitas);

-- =============================================================================
-- PENGISIAN DATA AWAL (SEED DATA)
-- Password default: password123 (bcrypt cost 10)
-- =============================================================================

-- 1. Pengguna (Admin & Customer)
INSERT INTO pengguna (id, nama, email, hash_kata_sandi, peran)
VALUES 
    (1, 'Administrator Sistem', 'admin@example.com', '$2a$10$Dfx1FJnV4DbqhxvUNrotG.Uap0nujZGaG/PcRuMAO.LZUAg3TIHvO', 'ADMIN'),
    (2, 'Budi Pelanggan', 'customer@example.com', '$2a$10$ZpaJknm/f6uFuyzM6.vTTuZxETErT5GmrLTt3KifxzSSxWDLh0Dn6', 'CUSTOMER')
ON CONFLICT (email) DO UPDATE SET 
    nama = EXCLUDED.nama,
    peran = EXCLUDED.peran,
    hash_kata_sandi = EXCLUDED.hash_kata_sandi;

-- 2. Bioskop
INSERT INTO bioskop (id, nama, kota, alamat, status)
VALUES 
    (1, 'Bioskop Grand Indonesia', 'Jakarta', 'Jl. M.H. Thamrin No. 1, Jakarta Pusat', 'ACTIVE')
ON CONFLICT (id) DO UPDATE SET 
    nama = EXCLUDED.nama,
    kota = EXCLUDED.kota,
    alamat = EXCLUDED.alamat;

-- 3. Studio
INSERT INTO studio (id, bioskop_id, nama, kapasitas, tipe)
VALUES 
    (1, 1, 'Studio 1', 50, 'IMAX'),
    (2, 1, 'Studio 2', 40, 'REGULAR')
ON CONFLICT (id) DO UPDATE SET 
    nama = EXCLUDED.nama,
    kapasitas = EXCLUDED.kapasitas,
    tipe = EXCLUDED.tipe;

-- 4. Kursi Studio 1 (Baris A, B, C @ 5 kursi)
INSERT INTO kursi (studio_id, label_baris, nomor_kursi, tipe_kursi)
VALUES 
    (1, 'A', 1, 'REGULAR'), (1, 'A', 2, 'REGULAR'), (1, 'A', 3, 'REGULAR'), (1, 'A', 4, 'REGULAR'), (1, 'A', 5, 'REGULAR'),
    (1, 'B', 1, 'REGULAR'), (1, 'B', 2, 'REGULAR'), (1, 'B', 3, 'REGULAR'), (1, 'B', 4, 'REGULAR'), (1, 'B', 5, 'REGULAR'),
    (1, 'C', 1, 'REGULAR'), (1, 'C', 2, 'REGULAR'), (1, 'C', 3, 'REGULAR'), (1, 'C', 4, 'REGULAR'), (1, 'C', 5, 'REGULAR')
ON CONFLICT (studio_id, label_baris, nomor_kursi) DO NOTHING;

-- 5. Film
INSERT INTO film (id, judul, durasi_menit, deskripsi, rating_usia, status)
VALUES 
    (1, 'Inception', 148, 'Seorang pencuri yang mencuri rahasia perusahaan melalui teknologi berbagi mimpi.', '13+', 'ACTIVE'),
    (2, 'Interstellar', 169, 'Sebuah tim penjelajah melintasi lubang cacing di luar angkasa.', '13+', 'ACTIVE')
ON CONFLICT (id) DO UPDATE SET 
    judul = EXCLUDED.judul,
    durasi_menit = EXCLUDED.durasi_menit,
    deskripsi = EXCLUDED.deskripsi,
    rating_usia = EXCLUDED.rating_usia;

-- 6. Jadwal Tayang Awal
INSERT INTO jadwal (id, film_id, studio_id, waktu_mulai, waktu_selesai, status)
VALUES 
    (1, 1, 1, '2026-10-01 19:00:00+07', '2026-10-01 21:28:00+07', 'SCHEDULED')
ON CONFLICT (id) DO UPDATE SET 
    film_id = EXCLUDED.film_id,
    studio_id = EXCLUDED.studio_id,
    waktu_mulai = EXCLUDED.waktu_mulai,
    waktu_selesai = EXCLUDED.waktu_selesai,
    status = EXCLUDED.status;

-- 7. Sinkronisasi Urutan Sequence PostgreSQL
SELECT setval(pg_get_serial_sequence('pengguna', 'id'), COALESCE(MAX(id), 1)) FROM pengguna;
SELECT setval(pg_get_serial_sequence('bioskop', 'id'), COALESCE(MAX(id), 1)) FROM bioskop;
SELECT setval(pg_get_serial_sequence('studio', 'id'), COALESCE(MAX(id), 1)) FROM studio;
SELECT setval(pg_get_serial_sequence('kursi', 'id'), COALESCE(MAX(id), 1)) FROM kursi;
SELECT setval(pg_get_serial_sequence('film', 'id'), COALESCE(MAX(id), 1)) FROM film;
SELECT setval(pg_get_serial_sequence('jadwal', 'id'), COALESCE(MAX(id), 1)) FROM jadwal;
