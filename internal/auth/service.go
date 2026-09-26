package auth

import (
	"context"
	"errors"

	"golang.org/x/crypto/bcrypt"
)

var (
	// ErrInvalidCredentials indicates that the provided email or password does not match.
	ErrInvalidCredentials = errors.New("invalid email or password")
)

// AuthService defines the business logic contract for authentication.
type AuthService interface {
	Login(requestContext context.Context, loginRequest LoginRequest) (*LoginResponse, error)
}

type authService struct {
	userRepository     UserRepository
	jwtSecretKey       string
	jwtExpirationHours int
}

// NewService constructs a new AuthService implementation instance.
func NewService(userRepository UserRepository, jwtSecretKey string, jwtExpirationHours int) AuthService {
	return &authService{
		userRepository:     userRepository,
		jwtSecretKey:       jwtSecretKey,
		jwtExpirationHours: jwtExpirationHours,
	}
}

// Login authenticates a user by email and password, returning a JWT token on success.
func (service *authService) Login(requestContext context.Context, loginRequest LoginRequest) (*LoginResponse, error) {
	userRecord, findUserError := service.userRepository.FindByEmail(requestContext, loginRequest.Email)
	if findUserError != nil {
		if errors.Is(findUserError, ErrUserNotFound) {
			return nil, ErrInvalidCredentials
		}
		return nil, findUserError
	}

	providedPassword := loginRequest.EffectivePassword()
	if passwordComparisonError := bcrypt.CompareHashAndPassword([]byte(userRecord.PasswordHash), []byte(providedPassword)); passwordComparisonError != nil {
		return nil, ErrInvalidCredentials
	}

	accessTokenString, expirationDurationInSeconds, tokenGenerationError := GenerateToken(
		userRecord.ID,
		userRecord.Role,
		service.jwtSecretKey,
		service.jwtExpirationHours,
	)
	if tokenGenerationError != nil {
		return nil, tokenGenerationError
	}

	return &LoginResponse{
		AccessToken: accessTokenString,
		TokenType:   "Bearer",
		ExpiresIn:   expirationDurationInSeconds,
	}, nil
}
