package database

import (
	"fmt"
	"log"

	"cinema-ticket-system/internal/config"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// HubungkanDatabase membangun koneksi GORM ke PostgreSQL menggunakan konfigurasi yang diberikan
// dan mengonfigurasi kolam koneksi database (connection pool).
func HubungkanDatabase(konfig *config.Konfigurasi) (*gorm.DB, error) {
	tingkatLog := logger.Warn
	if konfig.Lingkungan == "development" {
		tingkatLog = logger.Info
	}

	db, galat := gorm.Open(postgres.Open(konfig.DSN()), &gorm.Config{
		Logger: logger.Default.LogMode(tingkatLog),
	})
	if galat != nil {
		return nil, fmt.Errorf("gagal terhubung ke database: %w", galat)
	}

	sqlDB, galat := db.DB()
	if galat != nil {
		return nil, fmt.Errorf("gagal mendapatkan objek sql.DB: %w", galat)
	}

	// Konfigurasi kolam koneksi (connection pool)
	sqlDB.SetMaxOpenConns(konfig.MaksKoneksiTerbukaDB)
	sqlDB.SetMaxIdleConns(konfig.MaksKoneksiMenganggurDB)
	sqlDB.SetConnMaxLifetime(konfig.MaksMasaKoneksiDB)

	if galat := sqlDB.Ping(); galat != nil {
		return nil, fmt.Errorf("gagal melakukan ping ke database: %w", galat)
	}

	log.Println("Berhasil terhubung ke basis data PostgreSQL")
	return db, nil
}

// Connect adalah alias pemanggil untuk HubungkanDatabase.
func Connect(cfg *config.Config) (*gorm.DB, error) {
	return HubungkanDatabase(cfg)
}
