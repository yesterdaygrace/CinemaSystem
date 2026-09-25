CREATE TABLE IF NOT EXISTS pengembalian_dana (
    id BIGSERIAL PRIMARY KEY,
    pesanan_id BIGINT NOT NULL REFERENCES pesanan(id) ON DELETE CASCADE,
    pembayaran_id BIGINT REFERENCES pembayaran(id) ON DELETE SET NULL,
    jumlah NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    alasan TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    referensi_pengembalian VARCHAR(100),
    diajukan_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    selesai_pada TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_pengembalian_status ON pengembalian_dana(status);
