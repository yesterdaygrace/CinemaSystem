package auth

import (
	"errors"
	"fmt"
	"strconv"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var (
	GalatTokenTidakValid = errors.New("token tidak valid atau telah kedaluwarsa")
	ErrInvalidToken      = GalatTokenTidakValid
)

// KlaimJWT membungkus klaim standar JWT beserta peran pengguna.
type KlaimJWT struct {
	Peran string `json:"role"`
	jwt.RegisteredClaims
}

// JWTClaims adalah alias untuk KlaimJWT.
type JWTClaims = KlaimJWT

// BuatToken menandatangani token JWT baru menggunakan HMAC-SHA256.
func BuatToken(idPengguna int64, peran string, rahasia string, jamKedaluwarsa int) (string, int64, error) {
	waktuSekarang := time.Now().UTC()
	detikKedaluwarsa := int64(jamKedaluwarsa * 3600)
	waktuKedaluwarsa := waktuSekarang.Add(time.Duration(jamKedaluwarsa) * time.Hour)

	klaim := KlaimJWT{
		Peran: peran,
		RegisteredClaims: jwt.RegisteredClaims{
			Subject:   strconv.FormatInt(idPengguna, 10),
			IssuedAt:  jwt.NewNumericDate(waktuSekarang),
			ExpiresAt: jwt.NewNumericDate(waktuKedaluwarsa),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, klaim)
	stringToken, galat := token.SignedString([]byte(rahasia))
	if galat != nil {
		return "", 0, fmt.Errorf("gagal menandatangani token: %w", galat)
	}

	return stringToken, detikKedaluwarsa, nil
}

// GenerateToken adalah alias untuk BuatToken.
func GenerateToken(userID int64, role string, secret string, expireHours int) (string, int64, error) {
	return BuatToken(userID, role, secret, expireHours)
}

// ValidasiToken memverifikasi token string terhadap kunci rahasia.
func ValidasiToken(stringToken string, rahasia string) (*KlaimJWT, error) {
	token, galat := jwt.ParseWithClaims(stringToken, &KlaimJWT{}, func(t *jwt.Token) (interface{}, error) {
		if _, cocok := t.Method.(*jwt.SigningMethodHMAC); !cocok {
			return nil, fmt.Errorf("metode penandatanganan tidak sesuai: %v", t.Header["alg"])
		}
		return []byte(rahasia), nil
	})

	if galat != nil {
		return nil, GalatTokenTidakValid
	}

	klaim, cocok := token.Claims.(*KlaimJWT)
	if !cocok || !token.Valid {
		return nil, GalatTokenTidakValid
	}

	return klaim, nil
}

// ValidateToken adalah alias untuk ValidasiToken.
func ValidateToken(tokenStr string, secret string) (*KlaimJWT, error) {
	return ValidasiToken(tokenStr, secret)
}
