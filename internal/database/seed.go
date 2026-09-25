package database

import (
	"log"
	"time"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

// IsiDataAwal mengisi data awal ke basis data secara idempoten dalam Bahasa Indonesia.
func IsiDataAwal(db *gorm.DB) error {
	log.Println("Memulai pengisian data awal (seeding)...")

	hashAdmin, galat := bcrypt.GenerateFromPassword([]byte("password123"), bcrypt.DefaultCost)
	if galat != nil {
		return galat
	}
	hashPelanggan, galat := bcrypt.GenerateFromPassword([]byte("password123"), bcrypt.DefaultCost)
	if galat != nil {
		return galat
	}

	// 1. Data Awal Pengguna (Tabel: pengguna)
	daftarPengguna := []map[string]interface{}{
		{
			"id":              1,
			"nama":            "Administrator Sistem",
			"email":           "admin@example.com",
			"hash_kata_sandi": string(hashAdmin),
			"peran":           "ADMIN",
		},
		{
			"id":              2,
			"nama":            "Budi Pelanggan",
			"email":           "customer@example.com",
			"hash_kata_sandi": string(hashPelanggan),
			"peran":           "CUSTOMER",
		},
	}
	for _, p := range daftarPengguna {
		if galat := db.Table("pengguna").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "email"}},
				DoUpdates: clause.AssignmentColumns([]string{"nama", "peran", "hash_kata_sandi"}),
			}).
			Create(&p).Error; galat != nil {
			return galat
		}
	}

	// 2. Data Awal Bioskop (Tabel: bioskop)
	dataBioskop := map[string]interface{}{
		"id":      1,
		"nama":    "Bioskop Grand Indonesia",
		"kota":    "Jakarta",
		"alamat":  "Jl. M.H. Thamrin No. 1, Jakarta Pusat",
		"status":  "ACTIVE",
	}
	if galat := db.Table("bioskop").
		Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "id"}},
			DoUpdates: clause.AssignmentColumns([]string{"nama", "kota", "alamat", "status"}),
		}).
		Create(&dataBioskop).Error; galat != nil {
		return galat
	}

	// 3. Data Awal Studio (Tabel: studio)
	daftarStudio := []map[string]interface{}{
		{
			"id":         1,
			"bioskop_id": 1,
			"nama":       "Studio 1",
			"kapasitas":  50,
			"tipe":       "IMAX",
		},
		{
			"id":         2,
			"bioskop_id": 1,
			"nama":       "Studio 2",
			"kapasitas":  40,
			"tipe":       "REGULAR",
		},
	}
	for _, s := range daftarStudio {
		if galat := db.Table("studio").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "id"}},
				DoUpdates: clause.AssignmentColumns([]string{"nama", "kapasitas", "tipe"}),
			}).
			Create(&s).Error; galat != nil {
			return galat
		}
	}

	// 4. Data Awal Kursi (Tabel: kursi)
	var daftarKursi []map[string]interface{}
	barisKursi := []string{"A", "B", "C"}
	for _, b := range barisKursi {
		for no := 1; no <= 5; no++ {
			daftarKursi = append(daftarKursi, map[string]interface{}{
				"studio_id":   1,
				"label_baris": b,
				"nomor_kursi": no,
				"tipe_kursi":  "REGULAR",
			})
		}
	}
	for _, k := range daftarKursi {
		if galat := db.Table("kursi").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "studio_id"}, {Name: "label_baris"}, {Name: "nomor_kursi"}},
				DoNothing: true,
			}).
			Create(&k).Error; galat != nil {
			return galat
		}
	}

	// 5. Data Awal Film (Tabel: film)
	daftarFilm := []map[string]interface{}{
		{
			"id":           1,
			"judul":        "Inception",
			"durasi_menit": 148,
			"deskripsi":    "Seorang pencuri yang mencuri rahasia perusahaan melalui teknologi berbagi mimpi.",
			"rating_usia":  "13+",
			"status":       "ACTIVE",
		},
		{
			"id":           2,
			"judul":        "Interstellar",
			"durasi_menit": 169,
			"deskripsi":    "Sebuah tim penjelajah melintasi lubang cacing di luar angkasa.",
			"rating_usia":  "13+",
			"status":       "ACTIVE",
		},
	}
	for _, f := range daftarFilm {
		if galat := db.Table("film").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "id"}},
				DoUpdates: clause.AssignmentColumns([]string{"judul", "durasi_menit", "deskripsi", "rating_usia", "status"}),
			}).
			Create(&f).Error; galat != nil {
			return galat
		}
	}

	// 6. Data Awal Jadwal Tayang (Tabel: jadwal)
	lokasiWIB, _ := time.LoadLocation("Asia/Jakarta")
	if lokasiWIB == nil {
		lokasiWIB = time.FixedZone("WIB", 7*3600)
	}
	waktuMulai := time.Date(2026, 10, 1, 19, 0, 0, 0, lokasiWIB)
	waktuSelesai := time.Date(2026, 10, 1, 21, 28, 0, 0, lokasiWIB)

	jadwalAwal := map[string]interface{}{
		"id":            1,
		"film_id":       1,
		"studio_id":     1,
		"waktu_mulai":   waktuMulai,
		"waktu_selesai": waktuSelesai,
		"status":        "SCHEDULED",
	}
	if galat := db.Table("jadwal").
		Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "id"}},
			DoUpdates: clause.AssignmentColumns([]string{"film_id", "studio_id", "waktu_mulai", "waktu_selesai", "status"}),
		}).
		Create(&jadwalAwal).Error; galat != nil {
		return galat
	}

	// Reset sequence PostgreSQL agar penambahan auto-increment berikutnya tidak bentrok
	tabelList := []string{"pengguna", "bioskop", "studio", "kursi", "film", "jadwal"}
	for _, t := range tabelList {
		_ = db.Exec("SELECT setval(pg_get_serial_sequence(?, 'id'), COALESCE(MAX(id), 1)) FROM " + t, t).Error
	}

	log.Println("Data awal basis data berhasil diisi")
	return nil
}

// SeedDatabase adalah alias untuk IsiDataAwal.
func SeedDatabase(db *gorm.DB) error {
	return IsiDataAwal(db)
}
