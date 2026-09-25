package config

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
)

// Konfigurasi menyimpan seluruh parameter konfigurasi aplikasi.
type Konfigurasi struct {
	Port                   string
	Lingkungan             string
	HostDB                 string
	PortDB                 string
	PenggunaDB             string
	KataSandiDB            string
	NamaDB                 string
	ModeSSLDB              string
	MaksKoneksiTerbukaDB   int
	MaksKoneksiMenganggurDB int
	MaksMasaKoneksiDB      time.Duration
	RahasiaJWT             string
	MasaBerlakuJWTJam      int
	KedaluwarsaJWTJam      int

	// Kompatibilitas alias field jika dibutuhkan
	DBHost            string
	DBPort            string
	DBUser            string
	DBPassword        string
	DBName            string
	DBSSLMode         string
	DBMaxOpenConns    int
	DBMaxIdleConns    int
	DBConnMaxLifetime time.Duration
	JWTSecret         string
	JWTExpireHours    int
	Env               string
}

// Config adalah alias tipe untuk Konfigurasi demi kompatibilitas.
type Config = Konfigurasi

// MuatKonfigurasi memuat konfigurasi dari variabel lingkungan atau file .env.
func MuatKonfigurasi() (*Konfigurasi, error) {
	_ = godotenv.Load()

	maksKoneksiTerbuka := ambilEnvSebagaiInt("DB_MAX_OPEN_CONNS", 25)
	maksKoneksiMenganggur := ambilEnvSebagaiInt("DB_MAX_IDLE_CONNS", 10)
	masaKoneksiMenit := ambilEnvSebagaiInt("DB_CONN_MAX_LIFETIME_MINUTES", 5)
	masaBerlakuJWT := ambilEnvSebagaiInt("JWT_EXPIRE_HOURS", 24)

	port := ambilEnv("PORT", "8088")
	lingkungan := ambilEnv("ENV", "development")
	hostDB := ambilEnv("DB_HOST", "localhost")
	portDB := ambilEnv("DB_PORT", "5432")
	penggunaDB := ambilEnv("DB_USER", "bioskop")
	kataSandiDB := ambilEnv("DB_PASSWORD", "bioskop_dev")
	namaDB := ambilEnv("DB_NAME", "bioskop")
	modeSSLDB := ambilEnv("DB_SSLMODE", "disable")
	rahasiaJWT := ambilEnv("JWT_SECRET", "kunci_rahasia_jwt_sistem_bioskop_2026")

	durasiMasaKoneksi := time.Duration(masaKoneksiMenit) * time.Minute

	konfig := &Konfigurasi{
		Port:                    port,
		Lingkungan:              lingkungan,
		HostDB:                  hostDB,
		PortDB:                  portDB,
		PenggunaDB:              penggunaDB,
		KataSandiDB:             kataSandiDB,
		NamaDB:                  namaDB,
		ModeSSLDB:               modeSSLDB,
		MaksKoneksiTerbukaDB:    maksKoneksiTerbuka,
		MaksKoneksiMenganggurDB: maksKoneksiMenganggur,
		MaksMasaKoneksiDB:       durasiMasaKoneksi,
		RahasiaJWT:              rahasiaJWT,
		MasaBerlakuJWTJam:       masaBerlakuJWT,
		KedaluwarsaJWTJam:       masaBerlakuJWT,

		// Pemetaan nilai kompatibilitas
		DBHost:            hostDB,
		DBPort:            portDB,
		DBUser:            penggunaDB,
		DBPassword:        kataSandiDB,
		DBName:            namaDB,
		DBSSLMode:         modeSSLDB,
		DBMaxOpenConns:    maksKoneksiTerbuka,
		DBMaxIdleConns:    maksKoneksiMenganggur,
		DBConnMaxLifetime: durasiMasaKoneksi,
		JWTSecret:         rahasiaJWT,
		JWTExpireHours:    masaBerlakuJWT,
		Env:               lingkungan,
	}

	return konfig, nil
}

// LoadConfig adalah alias pemanggil untuk MuatKonfigurasi.
func LoadConfig() (*Konfigurasi, error) {
	return MuatKonfigurasi()
}

// DSN mengembalikan string sumber data PostgreSQL untuk GORM.
func (k *Konfigurasi) DSN() string {
	return fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=%s TimeZone=UTC",
		k.HostDB, k.PenggunaDB, k.KataSandiDB, k.NamaDB, k.PortDB, k.ModeSSLDB)
}

// URL mengembalikan format URI koneksi PostgreSQL standar.
func (k *Konfigurasi) URL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=%s",
		k.PenggunaDB, k.KataSandiDB, k.HostDB, k.PortDB, k.NamaDB, k.ModeSSLDB)
}

func ambilEnv(kunci, nilaiBawaan string) string {
	if nilai, ada := os.LookupEnv(kunci); ada && nilai != "" {
		return nilai
	}
	return nilaiBawaan
}

func ambilEnvSebagaiInt(kunci string, nilaiBawaan int) int {
	nilaiStr := ambilEnv(kunci, "")
	if nilai, err := strconv.Atoi(nilaiStr); err == nil {
		return nilai
	}
	return nilaiBawaan
}
