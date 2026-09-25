package auth

import "time"

const (
	PeranAdmin    = "ADMIN"
	PeranCustomer = "CUSTOMER"

	// Alias peran
	RoleAdmin    = PeranAdmin
	RoleCustomer = PeranCustomer
)

// Pengguna merepresentasikan tabel pengguna pada basis data PostgreSQL.
type Pengguna struct {
	ID             int64     `gorm:"primaryKey;autoIncrement" json:"id"`
	Nama           string    `gorm:"column:nama;type:varchar(255);not null" json:"nama"`
	Email          string    `gorm:"column:email;type:varchar(255);uniqueIndex;not null" json:"email"`
	HashKataSandi  string    `gorm:"column:hash_kata_sandi;type:varchar(255);not null" json:"-"`
	Peran          string    `gorm:"column:peran;type:varchar(50);not null;default:'CUSTOMER'" json:"peran"`
	DibuatPada     time.Time `gorm:"column:dibuat_pada" json:"dibuat_pada"`
	DiperbaruiPada time.Time `gorm:"column:diperbarui_pada" json:"diperbarui_pada"`
}

// TableName menentukan nama tabel relasional GORM.
func (Pengguna) TableName() string {
	return "pengguna"
}

// User adalah alias untuk Pengguna demi kompatibilitas.
type User = Pengguna

// PermintaanLogin mendefinisikan payload untuk permintaan login (POST /auth/login).
type PermintaanLogin struct {
	Email     string `json:"email" binding:"required,email" example:"admin@example.com"`
	Password  string `json:"password" example:"password123"`
	KataSandi string `json:"kata_sandi" example:"password123"`
}

// KataSandiEfektif mengembalikan kata sandi baik dari field password atau kata_sandi.
func (p *PermintaanLogin) KataSandiEfektif() string {
	if p.KataSandi != "" {
		return p.KataSandi
	}
	return p.Password
}

// LoginRequest adalah alias untuk PermintaanLogin.
type LoginRequest = PermintaanLogin

// ResponsLogin mendefinisikan payload respons saat login berhasil.
type ResponsLogin struct {
	AccessToken string `json:"access_token" example:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`
	TokenType   string `json:"token_type" example:"Bearer"`
	ExpiresIn   int64  `json:"expires_in" example:"86400"`
}

// LoginResponse adalah alias untuk ResponsLogin.
type LoginResponse = ResponsLogin

// DetailGalat mendefinisikan struktur informasi error.
type DetailGalat struct {
	Code    string `json:"code" example:"INVALID_CREDENTIALS"`
	Message string `json:"message" example:"Invalid email or password"`
}

// ErrorDetail adalah alias untuk DetailGalat.
type ErrorDetail = DetailGalat

// ResponsGalat mendefinisikan pembungkus respons error standar API.
type ResponsGalat struct {
	Error DetailGalat `json:"error"`
}

// ErrorResponse adalah alias untuk ResponsGalat.
type ErrorResponse = ResponsGalat
