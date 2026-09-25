CREATE TABLE IF NOT EXISTS kursi_jadwal (
    id BIGSERIAL PRIMARY KEY,
    jadwal_id BIGINT NOT NULL REFERENCES jadwal(id) ON DELETE CASCADE,
    kursi_id BIGINT NOT NULL REFERENCES kursi(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE',
    ditahan_oleh BIGINT REFERENCES pengguna(id) ON DELETE SET NULL,
    ditahan_sampai TIMESTAMP WITH TIME ZONE,
    terjual_pada TIMESTAMP WITH TIME ZONE,
    diperbarui_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(jadwal_id, kursi_id)
);

CREATE INDEX IF NOT EXISTS idx_kursi_jadwal_status ON kursi_jadwal(jadwal_id, status);
