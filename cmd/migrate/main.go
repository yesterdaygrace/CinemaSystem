package main

import (
	"flag"
	"log"

	"cinema-ticket-system/internal/config"
	"cinema-ticket-system/internal/database"
)

func main() {
	flagDataAwal := flag.Bool("seed", false, "Isi data awal setelah migrasi berhasil")
	flag.Parse()

	konfigurasi, galat := config.MuatKonfigurasi()
	if galat != nil {
		log.Fatalf("Gagal memuat konfigurasi: %v", galat)
	}

	log.Printf("Menghubungkan ke basis data di %s:%s...", konfigurasi.HostDB, konfigurasi.PortDB)
	if galat := database.JalankanMigrasi(konfigurasi.URL(), "migrations"); galat != nil {
		log.Fatalf("Migrasi gagal: %v", galat)
	}

	if *flagDataAwal {
		db, galat := database.HubungkanDatabase(konfigurasi)
		if galat != nil {
			log.Fatalf("Koneksi ke basis data gagal: %v", galat)
		}
		if galat := database.IsiDataAwal(db); galat != nil {
			log.Fatalf("Gagal mengisi data awal: %v", galat)
		}
	}

	log.Println("Perintah migrasi berhasil diselesaikan")
}
