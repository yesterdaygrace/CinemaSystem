package schedule

import (
	"context"
	"errors"
	"time"

	"gorm.io/gorm"
)

var (
	GalatJadwalTidakDitemukan = errors.New("jadwal tidak ditemukan")
	ErrScheduleNotFound       = GalatJadwalTidakDitemukan
)

// RepositoriJadwal mendefinisikan antarmuka query dan persistensi data jadwal.
type RepositoriJadwal interface {
	AmbilSemua(ctx context.Context) ([]Jadwal, error)
	AmbilBerdasarkanID(ctx context.Context, id int64) (*Jadwal, error)
	Buat(ctx context.Context, jadwal *Jadwal) error
	Perbarui(ctx context.Context, jadwal *Jadwal) error
	Batalkan(ctx context.Context, id int64) (*Jadwal, error)
	CekTumpangTindih(ctx context.Context, studioID int64, waktuMulai, waktuSelesai time.Time, kecualikanID int64) (bool, error)

	FindAll(ctx context.Context) ([]Jadwal, error)
	FindByID(ctx context.Context, id int64) (*Jadwal, error)
	Create(ctx context.Context, schedule *Jadwal) error
	Update(ctx context.Context, schedule *Jadwal) error
	Cancel(ctx context.Context, id int64) (*Jadwal, error)
	HasOverlap(ctx context.Context, studioID int64, startTime, endTime time.Time, excludeID int64) (bool, error)
}

// Repository adalah alias untuk RepositoriJadwal.
type Repository = RepositoriJadwal

type repositori struct {
	db *gorm.DB
}

// BaruRepositori mengembalikan instance repositori jadwal baru.
func BaruRepositori(db *gorm.DB) RepositoriJadwal {
	return &repositori{db: db}
}

// NewRepository adalah alias konstruktor untuk BaruRepositori.
func NewRepository(db *gorm.DB) RepositoriJadwal {
	return BaruRepositori(db)
}

func (r *repositori) AmbilSemua(ctx context.Context) ([]Jadwal, error) {
	var daftarJadwal []Jadwal
	if galat := r.db.WithContext(ctx).Order("waktu_mulai ASC").Find(&daftarJadwal).Error; galat != nil {
		return nil, galat
	}
	return daftarJadwal, nil
}

func (r *repositori) FindAll(ctx context.Context) ([]Jadwal, error) {
	return r.AmbilSemua(ctx)
}

func (r *repositori) AmbilBerdasarkanID(ctx context.Context, id int64) (*Jadwal, error) {
	var j Jadwal
	if galat := r.db.WithContext(ctx).First(&j, id).Error; galat != nil {
		if errors.Is(galat, gorm.ErrRecordNotFound) {
			return nil, GalatJadwalTidakDitemukan
		}
		return nil, galat
	}
	return &j, nil
}

func (r *repositori) FindByID(ctx context.Context, id int64) (*Jadwal, error) {
	return r.AmbilBerdasarkanID(ctx, id)
}

func (r *repositori) Buat(ctx context.Context, j *Jadwal) error {
	return r.db.WithContext(ctx).Create(j).Error
}

func (r *repositori) Create(ctx context.Context, s *Schedule) error {
	return r.Buat(ctx, s)
}

func (r *repositori) Perbarui(ctx context.Context, j *Jadwal) error {
	return r.db.WithContext(ctx).Save(j).Error
}

func (r *repositori) Update(ctx context.Context, s *Schedule) error {
	return r.Perbarui(ctx, s)
}

func (r *repositori) Batalkan(ctx context.Context, id int64) (*Jadwal, error) {
	var j Jadwal
	if galat := r.db.WithContext(ctx).First(&j, id).Error; galat != nil {
		if errors.Is(galat, gorm.ErrRecordNotFound) {
			return nil, GalatJadwalTidakDitemukan
		}
		return nil, galat
	}

	j.Status = StatusDibatalkan
	j.DiperbaruiPada = time.Now().UTC()
	if galat := r.db.WithContext(ctx).Save(&j).Error; galat != nil {
		return nil, galat
	}

	return &j, nil
}

func (r *repositori) Cancel(ctx context.Context, id int64) (*Jadwal, error) {
	return r.Batalkan(ctx, id)
}

func (r *repositori) CekTumpangTindih(ctx context.Context, studioID int64, waktuMulai, waktuSelesai time.Time, kecualikanID int64) (bool, error) {
	var jumlah int64
	query := r.db.WithContext(ctx).
		Model(&Jadwal{}).
		Where("studio_id = ?", studioID).
		Where("status != ?", StatusDibatalkan).
		Where("waktu_mulai < ? AND waktu_selesai > ?", waktuSelesai, waktuMulai)

	if kecualikanID > 0 {
		query = query.Where("id != ?", kecualikanID)
	}

	if galat := query.Count(&jumlah).Error; galat != nil {
		return false, galat
	}

	return jumlah > 0, nil
}

func (r *repositori) HasOverlap(ctx context.Context, studioID int64, startTime, endTime time.Time, excludeID int64) (bool, error) {
	return r.CekTumpangTindih(ctx, studioID, startTime, endTime, excludeID)
}
