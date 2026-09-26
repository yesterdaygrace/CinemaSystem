package auth

import (
	"errors"
	"fmt"
	"strconv"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var (
	// ErrInvalidToken is returned when a JWT token is invalid or expired.
	ErrInvalidToken = errors.New("token is invalid or has expired")
)

// JWTClaims wraps the registered JWT claims along with user role information.
type JWTClaims struct {
	Role string `json:"role"`
	jwt.RegisteredClaims
}

// GenerateToken signs a new JWT token using HMAC-SHA256.
func GenerateToken(userIdentifier int64, userRole string, secretKey string, expirationHours int) (string, int64, error) {
	currentTime := time.Now().UTC()
	expirationDurationInSeconds := int64(expirationHours * 3600)
	expirationTimestamp := currentTime.Add(time.Duration(expirationHours) * time.Hour)

	claims := JWTClaims{
		Role: userRole,
		RegisteredClaims: jwt.RegisteredClaims{
			Subject:   strconv.FormatInt(userIdentifier, 10),
			IssuedAt:  jwt.NewNumericDate(currentTime),
			ExpiresAt: jwt.NewNumericDate(expirationTimestamp),
		},
	}

	jwtToken := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedTokenString, signingError := jwtToken.SignedString([]byte(secretKey))
	if signingError != nil {
		return "", 0, fmt.Errorf("failed to sign JWT token: %w", signingError)
	}

	return signedTokenString, expirationDurationInSeconds, nil
}

// ValidateToken verifies and parses a JWT token string using the provided secret key.
func ValidateToken(tokenString string, secretKey string) (*JWTClaims, error) {
	parsedToken, parseError := jwt.ParseWithClaims(tokenString, &JWTClaims{}, func(signingToken *jwt.Token) (interface{}, error) {
		if _, matches := signingToken.Method.(*jwt.SigningMethodHMAC); !matches {
			return nil, fmt.Errorf("unexpected signing method: %v", signingToken.Header["alg"])
		}
		return []byte(secretKey), nil
	})

	if parseError != nil {
		return nil, ErrInvalidToken
	}

	claims, isClaimsValid := parsedToken.Claims.(*JWTClaims)
	if !isClaimsValid || !parsedToken.Valid {
		return nil, ErrInvalidToken
	}

	return claims, nil
}
