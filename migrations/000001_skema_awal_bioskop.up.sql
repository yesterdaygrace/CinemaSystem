-- =============================================================================
-- CINEMA TICKET SYSTEM (SISTEM TIKET BIOSKOP)
-- Standalone PostgreSQL DDL & Seed Script
-- Dialect: PostgreSQL 15+
-- Synchronized with migrations 000001 through 000014
--
-- How to import into a clean database:
--   psql -h localhost -p 5432 -U bioskop -d bioskop -f database.sql
-- Or via Docker Compose:
--   docker compose exec -T postgres psql -U bioskop -d bioskop -f /path/to/database.sql
-- =============================================================================

-- Required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- =============================================================================
-- 1. USERS TABLE (pengguna) - Migration 000001
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
-- 2. CINEMAS TABLE (bioskop) - Migration 000002 & 000014
-- =============================================================================
CREATE TABLE IF NOT EXISTS bioskop (
    id BIGSERIAL PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    kota VARCHAR(100) NOT NULL,
    zona_waktu VARCHAR(50) NOT NULL DEFAULT 'Asia/Jakarta',
    alamat TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bioskop_kota ON bioskop(kota);

-- =============================================================================
-- 3. STUDIOS TABLE (studio) - Migration 000003
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
-- 4. SEATS TABLE (kursi) - Migration 000004
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
-- 5. MOVIES TABLE (film) - Migration 000005
-- =============================================================================
CREATE TABLE IF NOT EXISTS film (
    id BIGSERIAL PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    durasi_menit INT NOT NULL,
    deskripsi TEXT,
    rating_usia VARCHAR(20) NOT NULL DEFAULT 'SU', -- 'SU', '13+', '17+', '21+'
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',  -- 'ACTIVE', 'ARCHIVED'
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_film_judul ON film(judul);
CREATE INDEX IF NOT EXISTS idx_film_status ON film(status);

-- =============================================================================
-- 6. SCREENING SCHEDULES TABLE (jadwal) - Migration 000006 & 000014
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
    CONSTRAINT chk_waktu_jadwal CHECK (waktu_selesai > waktu_mulai),
    CONSTRAINT no_overlapping_schedule EXCLUDE USING gist (
        studio_id WITH =,
        tstzrange(waktu_mulai, waktu_selesai, '[)') WITH &&
    ) WHERE (status = 'SCHEDULED')
);

CREATE INDEX IF NOT EXISTS idx_jadwal_film_mulai ON jadwal(film_id, waktu_mulai);
CREATE INDEX IF NOT EXISTS idx_jadwal_studio_mulai ON jadwal(studio_id, waktu_mulai);
CREATE INDEX IF NOT EXISTS idx_jadwal_studio_waktu ON jadwal(studio_id, waktu_mulai, waktu_selesai) WHERE status != 'CANCELLED';

-- =============================================================================
-- 7. SHOW SEATS INVENTORY TABLE (kursi_jadwal) - Migration 000007
-- Tracks seat availability state per screening schedule
-- =============================================================================
CREATE TABLE IF NOT EXISTS kursi_jadwal (
    id BIGSERIAL PRIMARY KEY,
    jadwal_id BIGINT NOT NULL REFERENCES jadwal(id) ON DELETE CASCADE,
    kursi_id BIGINT NOT NULL REFERENCES kursi(id) ON DELETE CASCADE,
    harga NUMERIC(12, 2) NOT NULL DEFAULT 50000.00,
    status VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'HELD', 'SOLD', 'INACTIVE'
    ditahan_oleh BIGINT REFERENCES pengguna(id) ON DELETE SET NULL,
    ditahan_sampai TIMESTAMP WITH TIME ZONE,
    terjual_pada TIMESTAMP WITH TIME ZONE,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_jadwal_kursi UNIQUE (jadwal_id, kursi_id)
);

CREATE INDEX IF NOT EXISTS idx_kursi_jadwal_status ON kursi_jadwal(jadwal_id, status);

-- =============================================================================
-- 8. ORDERS TABLE (pesanan) - Migration 000008
-- =============================================================================
CREATE TABLE IF NOT EXISTS pesanan (
    id BIGSERIAL PRIMARY KEY,
    pengguna_id BIGINT NOT NULL REFERENCES pengguna(id) ON DELETE RESTRICT,
    nomor_pesanan VARCHAR(100) NOT NULL UNIQUE,
    total_harga NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'PAID', 'CANCELLED', 'EXPIRED'
    kedaluwarsa_pada TIMESTAMP WITH TIME ZONE,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pesanan_pengguna ON pesanan(pengguna_id);
CREATE INDEX IF NOT EXISTS idx_pesanan_status ON pesanan(status);

-- =============================================================================
-- 9. ORDER ITEMS TABLE (item_pesanan) - Migration 000009
-- =============================================================================
CREATE TABLE IF NOT EXISTS item_pesanan (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    kursi_jadwal_id BIGINT NOT NULL REFERENCES kursi_jadwal(id) ON DELETE RESTRICT,
    harga NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    CONSTRAINT uq_pesanan_kursi_jadwal UNIQUE (pesanan_id, kursi_jadwal_id)
);

CREATE INDEX IF NOT EXISTS idx_item_pesanan_pesanan ON item_pesanan(pesanan_id);

-- =============================================================================
-- 10. PAYMENTS TABLE (pembayaran) - Migration 000010
-- =============================================================================
CREATE TABLE IF NOT EXISTS pembayaran (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    referensi_pembayaran VARCHAR(100) NOT NULL UNIQUE,
    jumlah NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'SUCCESS', 'FAILED', 'REFUNDED'
    dibayar_pada TIMESTAMP WITH TIME ZONE,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pembayaran_pesanan ON pembayaran(pesanan_id);

-- =============================================================================
-- 11. TICKETS TABLE (tiket) - Migration 000011
-- =============================================================================
CREATE TABLE IF NOT EXISTS tiket (
    id BIGSERIAL PRIMARY KEY,
    item_pesanan_id BIGINT NOT NULL REFERENCES item_pesanan(id) ON DELETE CASCADE,
    kode_tiket VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'ISSUED', -- 'ISSUED', 'USED', 'REFUNDED', 'CANCELLED'
    diterbitkan_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    dibatalkan_pada TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_tiket_kode ON tiket(kode_tiket);

-- =============================================================================
-- 12. REFUNDS TABLE (pengembalian_dana) - Migration 000012
-- =============================================================================
CREATE TABLE IF NOT EXISTS pengembalian_dana (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    pembayaran_id BIGINT REFERENCES pembayaran(id) ON DELETE SET NULL,
    jumlah NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    alasan TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'PROCESSED', 'COMPLETED', 'FAILED'
    referensi_pengembalian VARCHAR(100),
    diajukan_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    selesai_pada TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_pengembalian_status ON pengembalian_dana(status);

-- =============================================================================
-- 13. AUDIT LOGS TABLE (log_audit) - Migration 000013
-- =============================================================================
CREATE TABLE IF NOT EXISTS log_audit (
    id BIGSERIAL PRIMARY KEY,
    pengguna_id BIGINT REFERENCES pengguna(id) ON DELETE SET NULL,
    tipe_entitas VARCHAR(100) NOT NULL,
    entitas_id BIGINT NOT NULL,
    aksi VARCHAR(100) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE', 'CANCEL'
    nilai_lama JSONB,
    nilai_baru JSONB,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_log_audit_entitas ON log_audit(tipe_entitas, entitas_id);

-- =============================================================================
-- 14. PAYMENT EVENTS TABLE (event_pembayaran) - Migration 000014
-- Webhook duplicate / retry idempotency protection (provider_event_id UNIQUE)
-- =============================================================================
CREATE TABLE IF NOT EXISTS event_pembayaran (
    id BIGSERIAL PRIMARY KEY,
    id_event_provider VARCHAR(100) NOT NULL UNIQUE,
    pembayaran_id BIGINT REFERENCES pembayaran(id) ON DELETE CASCADE,
    tipe_event VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    diterima_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    diproses_pada TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_event_pembayaran_provider_id ON event_pembayaran(id_event_provider);

