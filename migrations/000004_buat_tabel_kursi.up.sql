CREATE TABLE IF NOT EXISTS kursi (
    id BIGSERIAL PRIMARY KEY,
    studio_id BIGINT NOT NULL REFERENCES studio(id) ON DELETE CASCADE,
    label_baris VARCHAR(10) NOT NULL,
    nomor_kursi INT NOT NULL,
    tipe_kursi VARCHAR(50) NOT NULL DEFAULT 'REGULAR',
    UNIQUE(studio_id, label_baris, nomor_kursi)
);

CREATE INDEX IF NOT EXISTS idx_kursi_studio_id ON kursi(studio_id);
