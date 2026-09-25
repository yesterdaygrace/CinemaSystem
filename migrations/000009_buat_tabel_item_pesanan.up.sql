CREATE TABLE IF NOT EXISTS item_pesanan (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    kursi_jadwal_id BIGINT NOT NULL REFERENCES kursi_jadwal(id) ON DELETE RESTRICT,
    harga NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);

CREATE INDEX IF NOT EXISTS idx_item_pesanan_pesanan ON item_pesanan(pesanan_id);
