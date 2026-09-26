package auth

import "time"

const (
	RoleAdmin    = "ADMIN"
	RoleCustomer = "CUSTOMER"
)

// User represents the 'pengguna' table in the PostgreSQL database.
type User struct {
	ID           int64     `gorm:"primaryKey;autoIncrement" json:"id"`
	Name         string    `gorm:"column:nama;type:varchar(255);not null" json:"name"`
	Email        string    `gorm:"column:email;type:varchar(255);uniqueIndex;not null" json:"email"`
	PasswordHash string    `gorm:"column:hash_kata_sandi;type:varchar(255);not null" json:"-"`
	Role         string    `gorm:"column:peran;type:varchar(50);not null;default:'CUSTOMER'" json:"role"`
	CreatedAt    time.Time `gorm:"column:dibuat_pada" json:"created_at"`
	UpdatedAt    time.Time `gorm:"column:diperbarui_pada" json:"updated_at"`
}

// TableName defines the PostgreSQL table name for GORM.
func (User) TableName() string {
	return "pengguna"
}

// GetRole returns the user's role.
func (user *User) GetRole() string {
	return user.Role
}

// GetPasswordHash returns the bcrypt password hash.
func (user *User) GetPasswordHash() string {
	return user.PasswordHash
}

// LoginRequest defines the request payload for user login (POST /auth/login).
type LoginRequest struct {
	Email    string `json:"email" binding:"required,email" example:"admin@example.com"`
	Password string `json:"password" example:"password123"`
}

// EffectivePassword resolves the password from the request payload.
func (request *LoginRequest) EffectivePassword() string {
	return request.Password
}

// LoginResponse defines the response payload returned on successful authentication.
type LoginResponse struct {
	AccessToken string `json:"access_token" example:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`
	TokenType   string `json:"token_type" example:"Bearer"`
	ExpiresIn   int64  `json:"expires_in" example:"86400"`
}

// ErrorDetail defines structured error information for API responses.
type ErrorDetail struct {
	Code    string `json:"code" example:"INVALID_CREDENTIALS"`
	Message string `json:"message" example:"Invalid email or password"`
}

// ErrorResponse wraps the standard API error response payload.
type ErrorResponse struct {
	Error ErrorDetail `json:"error"`
}
