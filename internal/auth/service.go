package auth

import (
	"context"
	"errors"

	"golang.org/x/crypto/bcrypt"
)

var (
	GalatKredensialTidakValid = errors.New("email atau kata sandi tidak valid")
	ErrInvalidCredentials     = GalatKredensialTidakValid
)

// LayananAutentikasi mendefinisikan kontrak logika bisnis autentikasi pengguna.
type LayananAutentikasi interface {
	Login(ctx context.Context, permintaan PermintaanLogin) (*ResponsLogin, error)
}

// Service adalah alias antarmuka untuk LayananAutentikasi.
type Service = LayananAutentikasi

type layanan struct {
	repo           RepositoriPengguna
	rahasiaJWT     string
	jamKedaluwarsa int
}

// BaruLayanan menginisialisasi layanan autentikasi baru.
func BaruLayanan(repo RepositoriPengguna, rahasiaJWT string, jamKedaluwarsa int) LayananAutentikasi {
	return &layanan{
		repo:           repo,
		rahasiaJWT:     rahasiaJWT,
		jamKedaluwarsa: jamKedaluwarsa,
	}
}

// NewService adalah alias konstruktor untuk BaruLayanan.
func NewService(repo RepositoriPengguna, jwtSecret string, expireHours int) LayananAutentikasi {
	return BaruLayanan(repo, jwtSecret, expireHours)
}

func (l *layanan) Login(ctx context.Context, permintaan PermintaanLogin) (*ResponsLogin, error) {
	pengguna, galat := l.repo.CariBerdasarkanEmail(ctx, permintaan.Email)
	if galat != nil {
		if errors.Is(galat, GalatPenggunaTidakDitemukan) {
			return nil, GalatKredensialTidakValid
		}
		return nil, galat
	}

	kataSandi := permintaan.KataSandiEfektif()
	if galat := bcrypt.CompareHashAndPassword([]byte(pengguna.HashKataSandi), []byte(kataSandi)); galat != nil {
		return nil, GalatKredensialTidakValid
	}

	tokenAkses, detikKedaluwarsa, galat := BuatToken(pengguna.ID, pengguna.Peran, l.rahasiaJWT, l.jamKedaluwarsa)
	if galat != nil {
		return nil, galat
	}

	return &ResponsLogin{
		AccessToken: tokenAkses,
		TokenType:   "Bearer",
		ExpiresIn:   detikKedaluwarsa,
	}, nil
}
