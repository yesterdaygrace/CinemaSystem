package auth

import (
	"context"
	"errors"

	"gorm.io/gorm"
)

var (
	GalatPenggunaTidakDitemukan = errors.New("pengguna tidak ditemukan")
	ErrUserNotFound             = GalatPenggunaTidakDitemukan
)

// RepositoriPengguna mendefinisikan kontrak akses data pengguna pada basis data.
type RepositoriPengguna interface {
	CariBerdasarkanEmail(ctx context.Context, email string) (*Pengguna, error)
	CariBerdasarkanID(ctx context.Context, id int64) (*Pengguna, error)
	FindByEmail(ctx context.Context, email string) (*Pengguna, error)
	FindByID(ctx context.Context, id int64) (*Pengguna, error)
}

// Repository adalah alias antarmuka untuk RepositoriPengguna.
type Repository = RepositoriPengguna

type repositori struct {
	db *gorm.DB
}

// BaruRepositori mengembalikan instance repositori baru dengan koneksi GORM.
func BaruRepositori(db *gorm.DB) RepositoriPengguna {
	return &repositori{db: db}
}

// NewRepository adalah alias konstruktor untuk BaruRepositori.
func NewRepository(db *gorm.DB) RepositoriPengguna {
	return BaruRepositori(db)
}

func (r *repositori) CariBerdasarkanEmail(ctx context.Context, email string) (*Pengguna, error) {
	var pengguna Pengguna
	if galat := r.db.WithContext(ctx).Where("email = ?", email).First(&pengguna).Error; galat != nil {
		if errors.Is(galat, gorm.ErrRecordNotFound) {
			return nil, GalatPenggunaTidakDitemukan
		}
		return nil, galat
	}
	return &pengguna, nil
}

func (r *repositori) FindByEmail(ctx context.Context, email string) (*Pengguna, error) {
	return r.CariBerdasarkanEmail(ctx, email)
}

func (r *repositori) CariBerdasarkanID(ctx context.Context, id int64) (*Pengguna, error) {
	var pengguna Pengguna
	if galat := r.db.WithContext(ctx).First(&pengguna, id).Error; galat != nil {
		if errors.Is(galat, gorm.ErrRecordNotFound) {
			return nil, GalatPenggunaTidakDitemukan
		}
		return nil, galat
	}
	return &pengguna, nil
}

func (r *repositori) FindByID(ctx context.Context, id int64) (*Pengguna, error) {
	return r.CariBerdasarkanID(ctx, id)
}
