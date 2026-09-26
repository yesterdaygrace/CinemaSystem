package auth

import (
	"strconv"
	"testing"
)

func TestJWTGenerateAndValidate(testRunner *testing.T) {
	secretKey := "secret_key_test_123456"
	userIdentifier := int64(42)
	userRole := RoleAdmin

	signedTokenString, expirationDurationInSeconds, tokenCreationError := GenerateToken(userIdentifier, userRole, secretKey, 24)
	if tokenCreationError != nil {
		testRunner.Fatalf("expected no error while creating token, got: %v", tokenCreationError)
	}

	if signedTokenString == "" {
		testRunner.Fatal("expected token string not to be empty")
	}

	if expirationDurationInSeconds != 86400 {
		testRunner.Fatalf("expected 86400 seconds, got: %d", expirationDurationInSeconds)
	}

	// Validate valid token
	validatedClaims, tokenValidationError := ValidateToken(signedTokenString, secretKey)
	if tokenValidationError != nil {
		testRunner.Fatalf("expected token validation to succeed, got: %v", tokenValidationError)
	}

	if validatedClaims.Role != userRole {
		testRunner.Fatalf("expected role %s, got: %s", userRole, validatedClaims.Role)
	}

	if validatedClaims.Subject != strconv.FormatInt(userIdentifier, 10) {
		testRunner.Fatalf("expected subject %d, got: %s", userIdentifier, validatedClaims.Subject)
	}

	// Validate token with invalid secret key
	_, invalidSecretError := ValidateToken(signedTokenString, "wrong_secret_key_123")
	if invalidSecretError == nil {
		testRunner.Fatal("expected validation error with invalid secret key, got nil")
	}
}
