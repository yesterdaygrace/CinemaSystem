package tests

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"
	"time"

	"cinema-ticket-system/internal/auth"
	"cinema-ticket-system/internal/config"
	"cinema-ticket-system/internal/database"
	"cinema-ticket-system/internal/middleware"
	"cinema-ticket-system/internal/schedule"

	"github.com/gin-gonic/gin"
)

func siapkanAplikasiUji(t *testing.T) (*gin.Engine, *config.Konfigurasi) {
	gin.SetMode(gin.TestMode)
	konfigurasi, galat := config.MuatKonfigurasi()
	if galat != nil {
		t.Fatalf("gagal memuat konfigurasi: %v", galat)
	}

	basisData, galat := database.HubungkanDatabase(konfigurasi)
	if galat != nil {
		t.Fatalf("gagal terhubung ke basis data: %v", galat)
	}

	// Pastikan migrasi tabel dan data awal telah terpasang
	_ = database.JalankanMigrasi(konfigurasi.URL(), "../migrations")
	_ = database.IsiDataAwal(basisData)

	repoAuth := auth.BaruRepositori(basisData)
	layananAuth := auth.BaruLayanan(repoAuth, konfigurasi.RahasiaJWT, konfigurasi.KedaluwarsaJWTJam)
	handlerAuth := auth.BaruHandler(layananAuth)

	repoJadwal := schedule.BaruRepositori(basisData)
	layananJadwal := schedule.BaruLayanan(repoJadwal)
	handlerJadwal := schedule.BaruHandler(layananJadwal)

	perute := gin.New()
	perute.Use(gin.Recovery())

	perute.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	v1 := perute.Group("/api/v1")
	{
		v1.POST("/auth/login", handlerAuth.Login)

		terproteksi := v1.Group("")
		terproteksi.Use(middleware.AutentikasiJWT(konfigurasi.RahasiaJWT))
		{
			terproteksi.GET("/schedules", handlerJadwal.Daftar)
			terproteksi.GET("/schedules/:id", handlerJadwal.AmbilBerdasarkanID)

			khususAdmin := terproteksi.Group("")
			khususAdmin.Use(middleware.WajibPeran(auth.PeranAdmin))
			{
				khususAdmin.POST("/schedules", handlerJadwal.Buat)
				khususAdmin.PUT("/schedules/:id", handlerJadwal.Perbarui)
				khususAdmin.DELETE("/schedules/:id", handlerJadwal.Hapus)
			}
		}
	}

	return perute, konfigurasi
}

func masuk(t *testing.T, perute *gin.Engine, surel, kataSandi string) string {
	muatan, _ := json.Marshal(map[string]string{
		"email":    surel,
		"password": kataSandi,
	})
	permintaan, _ := http.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewBuffer(muatan))
	permintaan.Header.Set("Content-Type", "application/json")
	perekam := httptest.NewRecorder()
	perute.ServeHTTP(perekam, permintaan)

	if perekam.Code != http.StatusOK {
		t.Fatalf("login gagal untuk %s dengan status %d: %s", surel, perekam.Code, perekam.Body.String())
	}

	var respons auth.ResponsLogin
	_ = json.Unmarshal(perekam.Body.Bytes(), &respons)
	return respons.AccessToken
}

func TestPemeriksaanKesehatan(t *testing.T) {
	perute, _ := siapkanAplikasiUji(t)

	permintaan, _ := http.NewRequest(http.MethodGet, "/health", nil)
	perekam := httptest.NewRecorder()
	perute.ServeHTTP(perekam, permintaan)

	if perekam.Code != http.StatusOK {
		t.Fatalf("diharapkan status 200, didapat %d", perekam.Code)
	}
}

func TestAutentikasi_Login(t *testing.T) {
	perute, _ := siapkanAplikasiUji(t)

	// 1. Berhasil login sebagai Admin
	tokenAdmin := masuk(t, perute, "admin@example.com", "password123")
	if tokenAdmin == "" {
		t.Fatal("token admin tidak boleh kosong")
	}

	// 2. Berhasil login sebagai Pelanggan
	tokenPelanggan := masuk(t, perute, "customer@example.com", "password123")
	if tokenPelanggan == "" {
		t.Fatal("token pelanggan tidak boleh kosong")
	}

	// 3. Kredensial tidak valid
	muatanSalah, _ := json.Marshal(map[string]string{
		"email":    "admin@example.com",
		"password": "wrongpassword",
	})
	permintaan, _ := http.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewBuffer(muatanSalah))
	permintaan.Header.Set("Content-Type", "application/json")
	perekam := httptest.NewRecorder()
	perute.ServeHTTP(perekam, permintaan)

	if perekam.Code != http.StatusUnauthorized {
		t.Fatalf("diharapkan status 401, didapat %d", perekam.Code)
	}
	var responsGalat auth.ResponsGalat
	_ = json.Unmarshal(perekam.Body.Bytes(), &responsGalat)
	if responsGalat.Error.Code != "INVALID_CREDENTIALS" {
		t.Fatalf("diharapkan INVALID_CREDENTIALS, didapat: %s", responsGalat.Error.Code)
	}
}

func TestJadwal_HakAkses(t *testing.T) {
	perute, _ := siapkanAplikasiUji(t)

	tokenPelanggan := masuk(t, perute, "customer@example.com", "password123")

	// 1. Permintaan tanpa token otentikasi -> 401
	permintaan1, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules", nil)
	perekam1 := httptest.NewRecorder()
	perute.ServeHTTP(perekam1, permintaan1)
	if perekam1.Code != http.StatusUnauthorized {
		t.Fatalf("diharapkan status 401, didapat %d", perekam1.Code)
	}

	// 2. Pelanggan melihat daftar jadwal -> 200
	permintaan2, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules", nil)
	permintaan2.Header.Set("Authorization", "Bearer "+tokenPelanggan)
	perekam2 := httptest.NewRecorder()
	perute.ServeHTTP(perekam2, permintaan2)
	if perekam2.Code != http.StatusOK {
		t.Fatalf("diharapkan status 200, didapat %d", perekam2.Code)
	}

	// 3. Pelanggan mencoba membuat jadwal baru -> 403 Forbidden
	bodiJadwal, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  1,
		"start_time": time.Now().Add(24 * time.Hour).Format(time.RFC3339),
		"end_time":   time.Now().Add(26 * time.Hour).Format(time.RFC3339),
	})
	permintaan3, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(bodiJadwal))
	permintaan3.Header.Set("Authorization", "Bearer "+tokenPelanggan)
	permintaan3.Header.Set("Content-Type", "application/json")
	perekam3 := httptest.NewRecorder()
	perute.ServeHTTP(perekam3, permintaan3)
	if perekam3.Code != http.StatusForbidden {
		t.Fatalf("diharapkan status 403, didapat %d: %s", perekam3.Code, perekam3.Body.String())
	}
}

func TestJadwal_SiklusHidupAdminDanKonflik(t *testing.T) {
	perute, konfigurasi := siapkanAplikasiUji(t)
	basisData, _ := database.HubungkanDatabase(konfigurasi)
	// Bersihkan data uji jadwal di Studio 2
	basisData.Exec("DELETE FROM jadwal WHERE studio_id = 2")
	t.Cleanup(func() {
		basisData.Exec("DELETE FROM jadwal WHERE studio_id = 2")
	})

	tokenAdmin := masuk(t, perute, "admin@example.com", "password123")

	waktuMulai := time.Date(2027, 1, 15, 14, 0, 0, 0, time.UTC)
	waktuSelesai := waktuMulai.Add(2 * time.Hour)

	// 1. Admin membuat jadwal baru di Studio 2
	bodiBuat, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  2,
		"start_time": waktuMulai.Format(time.RFC3339),
		"end_time":   waktuSelesai.Format(time.RFC3339),
	})
	permintaan1, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(bodiBuat))
	permintaan1.Header.Set("Authorization", "Bearer "+tokenAdmin)
	permintaan1.Header.Set("Content-Type", "application/json")
	perekam1 := httptest.NewRecorder()
	perute.ServeHTTP(perekam1, permintaan1)
	if perekam1.Code != http.StatusCreated {
		t.Fatalf("diharapkan status 201 Created, didapat %d: %s", perekam1.Code, perekam1.Body.String())
	}

	var responsDibuat schedule.ResponsJadwalTunggal
	_ = json.Unmarshal(perekam1.Body.Bytes(), &responsDibuat)
	idJadwalDibuat := responsDibuat.Data.ID

	// 2. Admin membuat jadwal yang bentrok (overlapping) di Studio 2 -> 409 Conflict
	mulaiBentrok := waktuMulai.Add(30 * time.Minute)
	selesaiBentrok := waktuSelesai.Add(30 * time.Minute)
	bodiBentrok, _ := json.Marshal(map[string]interface{}{
		"movie_id":   2,
		"studio_id":  2,
		"start_time": mulaiBentrok.Format(time.RFC3339),
		"end_time":   selesaiBentrok.Format(time.RFC3339),
	})
	permintaan2, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(bodiBentrok))
	permintaan2.Header.Set("Authorization", "Bearer "+tokenAdmin)
	permintaan2.Header.Set("Content-Type", "application/json")
	perekam2 := httptest.NewRecorder()
	perute.ServeHTTP(perekam2, permintaan2)
	if perekam2.Code != http.StatusConflict {
		t.Fatalf("diharapkan status 409 Conflict, didapat %d: %s", perekam2.Code, perekam2.Body.String())
	}
	var responsGalat schedule.ResponsGalat
	_ = json.Unmarshal(perekam2.Body.Bytes(), &responsGalat)
	if responsGalat.Error.Code != "SCHEDULE_CONFLICT" {
		t.Fatalf("diharapkan SCHEDULE_CONFLICT, didapat: %s", responsGalat.Error.Code)
	}

	// 3. Admin mengambil rincian jadwal berdasarkan ID -> 200 OK
	permintaan3, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules/"+strconv.FormatInt(idJadwalDibuat, 10), nil)
	permintaan3.Header.Set("Authorization", "Bearer "+tokenAdmin)
	perekam3 := httptest.NewRecorder()
	perute.ServeHTTP(perekam3, permintaan3)
	if perekam3.Code != http.StatusOK {
		t.Fatalf("diharapkan status 200 OK, didapat %d", perekam3.Code)
	}

	// 4. Admin memperbarui jadwal tayang -> 200 OK
	selesaiBaru := waktuSelesai.Add(15 * time.Minute)
	bodiPerbarui, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  2,
		"start_time": waktuMulai.Format(time.RFC3339),
		"end_time":   selesaiBaru.Format(time.RFC3339),
	})
	permintaan4, _ := http.NewRequest(http.MethodPut, "/api/v1/schedules/"+strconv.FormatInt(idJadwalDibuat, 10), bytes.NewBuffer(bodiPerbarui))
	permintaan4.Header.Set("Authorization", "Bearer "+tokenAdmin)
	permintaan4.Header.Set("Content-Type", "application/json")
	perekam4 := httptest.NewRecorder()
	perute.ServeHTTP(perekam4, permintaan4)
	if perekam4.Code != http.StatusOK {
		t.Fatalf("diharapkan status 200 OK saat pembaruan, didapat %d: %s", perekam4.Code, perekam4.Body.String())
	}

	// 5. Admin membatalkan jadwal secara logis -> 204 No Content
	permintaan5, _ := http.NewRequest(http.MethodDelete, "/api/v1/schedules/"+strconv.FormatInt(idJadwalDibuat, 10), nil)
	permintaan5.Header.Set("Authorization", "Bearer "+tokenAdmin)
	perekam5 := httptest.NewRecorder()
	perute.ServeHTTP(perekam5, permintaan5)
	if perekam5.Code != http.StatusNoContent {
		t.Fatalf("diharapkan status 204 No Content saat pembatalan, didapat %d: %s", perekam5.Code, perekam5.Body.String())
	}

	// 6. Verifikasi status jadwal berubah menjadi CANCELLED (tidak dihapus fisik)
	permintaan6, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules/"+strconv.FormatInt(idJadwalDibuat, 10), nil)
	permintaan6.Header.Set("Authorization", "Bearer "+tokenAdmin)
	perekam6 := httptest.NewRecorder()
	perute.ServeHTTP(perekam6, permintaan6)
	if perekam6.Code != http.StatusOK {
		t.Fatalf("diharapkan status 200 OK, didapat %d", perekam6.Code)
	}
	var responsAmbil schedule.ResponsJadwalTunggal
	_ = json.Unmarshal(perekam6.Body.Bytes(), &responsAmbil)
	if responsAmbil.Data.Status != schedule.StatusDibatalkan {
		t.Fatalf("diharapkan status CANCELLED, didapat: %s", responsAmbil.Data.Status)
	}

	// 7. Verifikasi bahwa slot waktu yang sebelumnya dibatalkan kini dapat dijadwalkan ulang
	permintaan7, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(bodiBuat))
	permintaan7.Header.Set("Authorization", "Bearer "+tokenAdmin)
	permintaan7.Header.Set("Content-Type", "application/json")
	perekam7 := httptest.NewRecorder()
	perute.ServeHTTP(perekam7, permintaan7)
	if perekam7.Code != http.StatusCreated {
		t.Fatalf("diharapkan status 201 Created setelah jadwal lama dibatalkan, didapat %d: %s", perekam7.Code, perekam7.Body.String())
	}
}
