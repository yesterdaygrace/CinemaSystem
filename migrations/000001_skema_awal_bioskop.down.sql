-- =============================================================================
-- CINEMA TICKET SYSTEM (SISTEM TIKET BIOSKOP)
-- Migration 000001 Down: Drop all 14 tables and extensions
-- =============================================================================

DROP TABLE IF EXISTS event_pembayaran CASCADE;
DROP TABLE IF EXISTS log_audit CASCADE;
DROP TABLE IF EXISTS pengembalian_dana CASCADE;
DROP TABLE IF EXISTS tiket CASCADE;
DROP TABLE IF EXISTS pembayaran CASCADE;
DROP TABLE IF EXISTS item_pesanan CASCADE;
DROP TABLE IF EXISTS pesanan CASCADE;
DROP TABLE IF EXISTS kursi_jadwal CASCADE;
DROP TABLE IF EXISTS jadwal CASCADE;
DROP TABLE IF EXISTS film CASCADE;
DROP TABLE IF EXISTS kursi CASCADE;
DROP TABLE IF EXISTS studio CASCADE;
DROP TABLE IF EXISTS bioskop CASCADE;
DROP TABLE IF EXISTS pengguna CASCADE;

DROP EXTENSION IF EXISTS "btree_gist";
DROP EXTENSION IF EXISTS "uuid-ossp";
