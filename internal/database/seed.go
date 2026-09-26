package database

import (
	"log"
	"time"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

// SeedDatabase seeds initial reference data idempotently into the database.
func SeedDatabase(databaseConnection *gorm.DB) error {
	log.Println("Starting database seeding...")

	adminPasswordHash, adminHashingError := bcrypt.GenerateFromPassword([]byte("password123"), bcrypt.DefaultCost)
	if adminHashingError != nil {
		return adminHashingError
	}
	customerPasswordHash, customerHashingError := bcrypt.GenerateFromPassword([]byte("password123"), bcrypt.DefaultCost)
	if customerHashingError != nil {
		return customerHashingError
	}

	// 1. Initial Users (Table: pengguna)
	userSeedList := []map[string]interface{}{
		{
			"id":              1,
			"nama":            "Administrator Sistem",
			"email":           "admin@example.com",
			"hash_kata_sandi": string(adminPasswordHash),
			"peran":           "ADMIN",
		},
		{
			"id":              2,
			"nama":            "Budi Pelanggan",
			"email":           "customer@example.com",
			"hash_kata_sandi": string(customerPasswordHash),
			"peran":           "CUSTOMER",
		},
		{
			"id":              3,
			"nama":            "Siti Pelanggan 2",
			"email":           "customer2@example.com",
			"hash_kata_sandi": string(customerPasswordHash),
			"peran":           "CUSTOMER",
		},
	}
	for _, userRecord := range userSeedList {
		if insertionError := databaseConnection.Table("pengguna").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "email"}},
				DoUpdates: clause.AssignmentColumns([]string{"nama", "peran", "hash_kata_sandi"}),
			}).
			Create(&userRecord).Error; insertionError != nil {
			return insertionError
		}
	}

	// 2. Initial Cinema (Table: bioskop)
	cinemaSeedRecord := map[string]interface{}{
		"id":         1,
		"nama":       "Bioskop Grand Indonesia",
		"kota":       "Jakarta",
		"zona_waktu": "Asia/Jakarta",
		"alamat":     "Jl. M.H. Thamrin No. 1, Jakarta Pusat",
		"status":     "ACTIVE",
	}
	if insertionError := databaseConnection.Table("bioskop").
		Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "id"}},
			DoUpdates: clause.AssignmentColumns([]string{"nama", "kota", "zona_waktu", "alamat", "status"}),
		}).
		Create(&cinemaSeedRecord).Error; insertionError != nil {
		return insertionError
	}

	// 3. Initial Studios (Table: studio)
	studioSeedList := []map[string]interface{}{
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
	for _, studioRecord := range studioSeedList {
		if insertionError := databaseConnection.Table("studio").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "id"}},
				DoUpdates: clause.AssignmentColumns([]string{"nama", "kapasitas", "tipe"}),
			}).
			Create(&studioRecord).Error; insertionError != nil {
			return insertionError
		}
	}

	// 4. Initial Seats (Table: kursi)
	var seatSeedList []map[string]interface{}
	seatRowLetters := []string{"A", "B", "C"}
	for _, rowLetter := range seatRowLetters {
		for seatNumber := 1; seatNumber <= 5; seatNumber++ {
			seatSeedList = append(seatSeedList, map[string]interface{}{
				"studio_id":   1,
				"label_baris": rowLetter,
				"nomor_kursi": seatNumber,
				"tipe_kursi":  "REGULAR",
			})
		}
	}
	for _, seatRecord := range seatSeedList {
		if insertionError := databaseConnection.Table("kursi").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "studio_id"}, {Name: "label_baris"}, {Name: "nomor_kursi"}},
				DoNothing: true,
			}).
			Create(&seatRecord).Error; insertionError != nil {
			return insertionError
		}
	}

	// 5. Initial Movies (Table: film)
	movieSeedList := []map[string]interface{}{
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
	for _, movieRecord := range movieSeedList {
		if insertionError := databaseConnection.Table("film").
			Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "id"}},
				DoUpdates: clause.AssignmentColumns([]string{"judul", "durasi_menit", "deskripsi", "rating_usia", "status"}),
			}).
			Create(&movieRecord).Error; insertionError != nil {
			return insertionError
		}
	}

	// 6. Initial Schedule (Table: jadwal)
	jakartaTimezone, _ := time.LoadLocation("Asia/Jakarta")
	if jakartaTimezone == nil {
		jakartaTimezone = time.FixedZone("WIB", 7*3600)
	}
	initialStartTime := time.Date(2026, 10, 1, 19, 0, 0, 0, jakartaTimezone)
	initialEndTime := time.Date(2026, 10, 1, 21, 28, 0, 0, jakartaTimezone)

	initialScheduleRecord := map[string]interface{}{
		"id":            1,
		"film_id":       1,
		"studio_id":     1,
		"waktu_mulai":   initialStartTime,
		"waktu_selesai": initialEndTime,
		"status":        "SCHEDULED",
	}
	if insertionError := databaseConnection.Table("jadwal").
		Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "id"}},
			DoUpdates: clause.AssignmentColumns([]string{"film_id", "studio_id", "waktu_mulai", "waktu_selesai", "status"}),
		}).
		Create(&initialScheduleRecord).Error; insertionError != nil {
		return insertionError
	}

	// Reset PostgreSQL serial sequences to prevent sequence conflict on future inserts
	tableNamesToResetSequences := []string{"pengguna", "bioskop", "studio", "kursi", "film", "jadwal"}
	for _, tableName := range tableNamesToResetSequences {
		_ = databaseConnection.Exec("SELECT setval(pg_get_serial_sequence(?, 'id'), COALESCE(MAX(id), 1)) FROM "+tableName, tableName).Error
	}

	log.Println("Database initial seed completed successfully")
	return nil
}

// SeedInitialData is an alias for SeedDatabase.
func SeedInitialData(databaseConnection *gorm.DB) error {
	return SeedDatabase(databaseConnection)
}
