package schedule

import (
	"context"
	"testing"
	"time"
)

type repositoriTiruan struct {
	jadwalPeta         map[int64]*Jadwal
	idBerikutnya       int64
	fungsiTumpangTindih func(studioID int64, startTime, endTime time.Time, excludeID int64) bool
}

func baruRepositoriTiruan() *repositoriTiruan {
	return &repositoriTiruan{
		jadwalPeta:   make(map[int64]*Jadwal),
		idBerikutnya: 1,
	}
}

func (m *repositoriTiruan) AmbilSemua(ctx context.Context) ([]Jadwal, error) {
	var daftar []Jadwal
	for _, j := range m.jadwalPeta {
		daftar = append(daftar, *j)
	}
	return daftar, nil
}

func (m *repositoriTiruan) FindAll(ctx context.Context) ([]Jadwal, error) {
	return m.AmbilSemua(ctx)
}

func (m *repositoriTiruan) AmbilBerdasarkanID(ctx context.Context, id int64) (*Jadwal, error) {
	j, ada := m.jadwalPeta[id]
	if !ada {
		return nil, GalatJadwalTidakDitemukan
	}
	return j, nil
}

func (m *repositoriTiruan) FindByID(ctx context.Context, id int64) (*Jadwal, error) {
	return m.AmbilBerdasarkanID(ctx, id)
}

func (m *repositoriTiruan) Buat(ctx context.Context, j *Jadwal) error {
	j.ID = m.idBerikutnya
	m.idBerikutnya++
	m.jadwalPeta[j.ID] = j
	return nil
}

func (m *repositoriTiruan) Create(ctx context.Context, s *Schedule) error {
	return m.Buat(ctx, s)
}

func (m *repositoriTiruan) Perbarui(ctx context.Context, j *Jadwal) error {
	m.jadwalPeta[j.ID] = j
	return nil
}

func (m *repositoriTiruan) Update(ctx context.Context, s *Schedule) error {
	return m.Perbarui(ctx, s)
}

func (m *repositoriTiruan) Batalkan(ctx context.Context, id int64) (*Jadwal, error) {
	j, ada := m.jadwalPeta[id]
	if !ada {
		return nil, GalatJadwalTidakDitemukan
	}
	j.Status = StatusDibatalkan
	return j, nil
}

func (m *repositoriTiruan) Cancel(ctx context.Context, id int64) (*Jadwal, error) {
	return m.Batalkan(ctx, id)
}

func (m *repositoriTiruan) CekTumpangTindih(ctx context.Context, studioID int64, waktuMulai, waktuSelesai time.Time, kecualikanID int64) (bool, error) {
	if m.fungsiTumpangTindih != nil {
		return m.fungsiTumpangTindih(studioID, waktuMulai, waktuSelesai, kecualikanID), nil
	}
	for _, j := range m.jadwalPeta {
		if j.StudioID == studioID && j.Status != StatusDibatalkan {
			if kecualikanID > 0 && j.ID == kecualikanID {
				continue
			}
			if waktuMulai.Before(j.WaktuSelesai) && waktuSelesai.After(j.WaktuMulai) {
				return true, nil
			}
		}
	}
	return false, nil
}

func (m *repositoriTiruan) HasOverlap(ctx context.Context, studioID int64, startTime, endTime time.Time, excludeID int64) (bool, error) {
	return m.CekTumpangTindih(ctx, studioID, startTime, endTime, excludeID)
}

func TestScheduleService_Create(t *testing.T) {
	repo := baruRepositoriTiruan()
	layanan := BaruLayanan(repo)
	konteks := context.Background()

	sekarang := time.Now()
	waktuMulai := sekarang.Add(2 * time.Hour)
	waktuSelesai := waktuMulai.Add(2 * time.Hour)

	// 1. Waktu tidak valid: waktu_selesai <= waktu_mulai
	_, galat := layanan.BuatJadwal(konteks, PermintaanBuatJadwal{
		FilmID:       1,
		StudioID:     1,
		WaktuMulai:   waktuSelesai,
		WaktuSelesai: waktuMulai,
	})
	if galat == nil {
		t.Fatal("diharapkan galat saat waktu_selesai <= waktu_mulai, didapat nil")
	}

	// 2. Pembuatan jadwal berhasil
	dibuat, galat := layanan.BuatJadwal(konteks, PermintaanBuatJadwal{
		FilmID:       1,
		StudioID:     1,
		WaktuMulai:   waktuMulai,
		WaktuSelesai: waktuSelesai,
	})
	if galat != nil {
		t.Fatalf("diharapkan pembuatan jadwal berhasil, didapat: %v", galat)
	}
	if dibuat.ID != 1 || dibuat.Status != StatusJadwal {
		t.Fatalf("jadwal tidak sesuai: %+v", dibuat)
	}

	// 3. Konflik tumpang tindih waktu pada studio yang sama
	mulaiKonflik := waktuMulai.Add(30 * time.Minute)
	selesaiKonflik := waktuSelesai.Add(30 * time.Minute)
	_, galat = layanan.BuatJadwal(konteks, PermintaanBuatJadwal{
		FilmID:       2,
		StudioID:     1,
		WaktuMulai:   mulaiKonflik,
		WaktuSelesai: selesaiKonflik,
	})
	if galat != GalatKonflikJadwal {
		t.Fatalf("diharapkan GalatKonflikJadwal, didapat: %v", galat)
	}

	// 4. Pembuatan di studio lain berhasil
	_, galat = layanan.BuatJadwal(konteks, PermintaanBuatJadwal{
		FilmID:       2,
		StudioID:     2,
		WaktuMulai:   mulaiKonflik,
		WaktuSelesai: selesaiKonflik,
	})
	if galat != nil {
		t.Fatalf("diharapkan pembuatan di studio berbeda berhasil, didapat: %v", galat)
	}

	// 5. Batalkan jadwal
	if galat := layanan.BatalkanJadwal(konteks, 1); galat != nil {
		t.Fatalf("gagal membatalkan jadwal: %v", galat)
	}

	// 6. Setelah dibatalkan, slot waktu dapat dipesan kembali tanpa bentrok
	_, galat = layanan.BuatJadwal(konteks, PermintaanBuatJadwal{
		FilmID:       1,
		StudioID:     1,
		WaktuMulai:   waktuMulai,
		WaktuSelesai: waktuSelesai,
	})
	if galat != nil {
		t.Fatalf("diharapkan slot yang dibatalkan dapat dipesan kembali, didapat: %v", galat)
	}
}
