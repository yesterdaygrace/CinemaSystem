package auth

import (
	"context"
	"errors"

	"gorm.io/gorm"
)

var (
	// ErrUserNotFound is returned when no user matches the given criteria.
	ErrUserNotFound = errors.New("user not found")
)

// UserRepository defines database access operations for users.
type UserRepository interface {
	FindByEmail(requestContext context.Context, emailAddress string) (*User, error)
	FindByID(requestContext context.Context, userIdentifier int64) (*User, error)
}

type userRepository struct {
	databaseConnection *gorm.DB
}

// NewRepository initializes a new UserRepository instance using GORM.
func NewRepository(databaseConnection *gorm.DB) UserRepository {
	return &userRepository{databaseConnection: databaseConnection}
}

// FindByEmail searches for a user in the database by their unique email address.
func (repository *userRepository) FindByEmail(requestContext context.Context, emailAddress string) (*User, error) {
	var userRecord User
	if databaseError := repository.databaseConnection.WithContext(requestContext).Where("email = ?", emailAddress).First(&userRecord).Error; databaseError != nil {
		if errors.Is(databaseError, gorm.ErrRecordNotFound) {
			return nil, ErrUserNotFound
		}
		return nil, databaseError
	}
	return &userRecord, nil
}

// FindByID searches for a user in the database by their unique ID.
func (repository *userRepository) FindByID(requestContext context.Context, userIdentifier int64) (*User, error) {
	var userRecord User
	if databaseError := repository.databaseConnection.WithContext(requestContext).First(&userRecord, userIdentifier).Error; databaseError != nil {
		if errors.Is(databaseError, gorm.ErrRecordNotFound) {
			return nil, ErrUserNotFound
		}
		return nil, databaseError
	}
	return &userRecord, nil
}
