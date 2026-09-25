package database

import (
	"errors"
	"fmt"
	"log"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
)

// JalankanMigrasi mengeksekusi semua migrasi 'up' dari jalur berkas ke basis data.
func JalankanMigrasi(urlDB string, jalurMigrasi string) error {
	urlSumber := fmt.Sprintf("file://%s", jalurMigrasi)
	instansiMigrasi, galat := migrate.New(urlSumber, urlDB)
	if galat != nil {
		return fmt.Errorf("gagal menginisialisasi migrasi: %w", galat)
	}
	defer instansiMigrasi.Close()

	if galat := instansiMigrasi.Up(); galat != nil && !errors.Is(galat, migrate.ErrNoChange) {
		return fmt.Errorf("gagal menerapkan migrasi: %w", galat)
	}

	log.Println("Migrasi basis data berhasil diterapkan")
	return nil
}

// RunMigrations adalah alias untuk JalankanMigrasi.
func RunMigrations(dbURL string, migrationsPath string) error {
	return JalankanMigrasi(dbURL, migrationsPath)
}
