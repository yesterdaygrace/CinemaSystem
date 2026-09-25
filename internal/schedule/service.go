package schedule

import (
	"context"
	"errors"
	"time"
)

var (
	GalatKonflikJadwal          = errors.New("studio already has an overlapping schedule")
	GalatRentangWaktuTidakValid = errors.New("end_time must be after start_time")

	ErrScheduleConflict = GalatKonflikJadwal
	ErrInvalidTimeRange = GalatRentangWaktuTidakValid
)

// LayananJadwal mendefinisikan antarmuka logika bisnis jadwal tayang.
type LayananJadwal interface {
	DaftarJadwal(ctx context.Context) ([]DTOJadwal, error)
	AmbilJadwal(ctx context.Context, id int64) (*DTOJadwal, error)
	BuatJadwal(ctx context.Context, permintaan PermintaanBuatJadwal) (*DTOJadwal, error)
	PerbaruiJadwal(ctx context.Context, id int64, permintaan PermintaanPerbaruiJadwal) (*DTOJadwal, error)
	BatalkanJadwal(ctx context.Context, id int64) error

	ListSchedules(ctx context.Context) ([]ScheduleDTO, error)
	GetSchedule(ctx context.Context, id int64) (*ScheduleDTO, error)
	CreateSchedule(ctx context.Context, req CreateScheduleRequest) (*ScheduleDTO, error)
	UpdateSchedule(ctx context.Context, id int64, req UpdateScheduleRequest) (*ScheduleDTO, error)
	CancelSchedule(ctx context.Context, id int64) error
}

// Service adalah alias untuk LayananJadwal.
type Service = LayananJadwal

type layanan struct {
	repo RepositoriJadwal
}

// BaruLayanan mengembalikan instance baru layanan jadwal.
func BaruLayanan(repo RepositoriJadwal) LayananJadwal {
	return &layanan{repo: repo}
}

// NewService adalah alias konstruktor untuk BaruLayanan.
func NewService(repo Repository) Service {
	return BaruLayanan(repo)
}

func (l *layanan) DaftarJadwal(ctx context.Context) ([]DTOJadwal, error) {
	daftarJadwal, galat := l.repo.AmbilSemua(ctx)
	if galat != nil {
		return nil, galat
	}

	hasil := make([]DTOJadwal, len(daftarJadwal))
	for i, item := range daftarJadwal {
		hasil[i] = DariModel(&item)
	}
	return hasil, nil
}

func (l *layanan) ListSchedules(ctx context.Context) ([]ScheduleDTO, error) {
	return l.DaftarJadwal(ctx)
}

func (l *layanan) AmbilJadwal(ctx context.Context, id int64) (*DTOJadwal, error) {
	jadwal, galat := l.repo.AmbilBerdasarkanID(ctx, id)
	if galat != nil {
		return nil, galat
	}
	dto := DariModel(jadwal)
	return &dto, nil
}

func (l *layanan) GetSchedule(ctx context.Context, id int64) (*ScheduleDTO, error) {
	return l.AmbilJadwal(ctx, id)
}

func (l *layanan) BuatJadwal(ctx context.Context, permintaan PermintaanBuatJadwal) (*DTOJadwal, error) {
	if galat := permintaan.Validasi(); galat != nil {
		return nil, galat
	}

	filmID := permintaan.AmbilFilmID()
	waktuMulai := permintaan.AmbilWaktuMulai()
	waktuSelesai := permintaan.AmbilWaktuSelesai()

	adaKonflik, galat := l.repo.CekTumpangTindih(ctx, permintaan.StudioID, waktuMulai, waktuSelesai, 0)
	if galat != nil {
		return nil, galat
	}
	if adaKonflik {
		return nil, GalatKonflikJadwal
	}

	sekarang := time.Now().UTC()
	jadwalBaru := &Jadwal{
		FilmID:         filmID,
		StudioID:       permintaan.StudioID,
		WaktuMulai:     waktuMulai,
		WaktuSelesai:   waktuSelesai,
		Status:         StatusJadwal,
		DibuatPada:     sekarang,
		DiperbaruiPada: sekarang,
	}

	if galat := l.repo.Buat(ctx, jadwalBaru); galat != nil {
		return nil, galat
	}

	dto := DariModel(jadwalBaru)
	return &dto, nil
}

func (l *layanan) CreateSchedule(ctx context.Context, req CreateScheduleRequest) (*ScheduleDTO, error) {
	return l.BuatJadwal(ctx, req)
}

func (l *layanan) PerbaruiJadwal(ctx context.Context, id int64, permintaan PermintaanPerbaruiJadwal) (*DTOJadwal, error) {
	if galat := permintaan.Validasi(); galat != nil {
		return nil, galat
	}

	jadwalLama, galat := l.repo.AmbilBerdasarkanID(ctx, id)
	if galat != nil {
		return nil, galat
	}

	filmID := permintaan.AmbilFilmID()
	waktuMulai := permintaan.AmbilWaktuMulai()
	waktuSelesai := permintaan.AmbilWaktuSelesai()

	adaKonflik, galat := l.repo.CekTumpangTindih(ctx, permintaan.StudioID, waktuMulai, waktuSelesai, id)
	if galat != nil {
		return nil, galat
	}
	if adaKonflik {
		return nil, GalatKonflikJadwal
	}

	jadwalLama.FilmID = filmID
	jadwalLama.StudioID = permintaan.StudioID
	jadwalLama.WaktuMulai = waktuMulai
	jadwalLama.WaktuSelesai = waktuSelesai
	jadwalLama.DiperbaruiPada = time.Now().UTC()

	if galat := l.repo.Perbarui(ctx, jadwalLama); galat != nil {
		return nil, galat
	}

	dto := DariModel(jadwalLama)
	return &dto, nil
}

func (l *layanan) UpdateSchedule(ctx context.Context, id int64, req UpdateScheduleRequest) (*ScheduleDTO, error) {
	return l.PerbaruiJadwal(ctx, id, req)
}

func (l *layanan) BatalkanJadwal(ctx context.Context, id int64) error {
	_, galat := l.repo.Batalkan(ctx, id)
	return galat
}

func (l *layanan) CancelSchedule(ctx context.Context, id int64) error {
	return l.BatalkanJadwal(ctx, id)
}
