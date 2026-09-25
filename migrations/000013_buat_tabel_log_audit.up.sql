CREATE TABLE IF NOT EXISTS log_audit (
    id BIGSERIAL PRIMARY KEY,
    pengguna_id BIGINT REFERENCES pengguna(id) ON DELETE SET NULL,
    tipe_entitas VARCHAR(100) NOT NULL,
    entitas_id BIGINT NOT NULL,
    aksi VARCHAR(100) NOT NULL,
    nilai_lama JSONB,
    nilai_baru JSONB,
    dibuat_pada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_log_audit_entitas ON log_audit(tipe_entitas, entitas_id);
