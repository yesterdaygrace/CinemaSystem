package middleware

import (
	"net/http"
	"strconv"
	"strings"

	"cinema-ticket-system/internal/auth"

	"github.com/gin-gonic/gin"
)

const (
	ContextUserIDKey   = "userID"
	ContextUserRoleKey = "userRole"
)

// JWTAuth validates the Bearer token in the Authorization header.
func JWTAuth(jwtSecretKey string) gin.HandlerFunc {
	return func(ginContext *gin.Context) {
		authorizationHeader := ginContext.GetHeader("Authorization")
		if authorizationHeader == "" {
			ginContext.AbortWithStatusJSON(http.StatusUnauthorized, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "UNAUTHORIZED",
					Message: "Authorization header is required",
				},
			})
			return
		}

		headerParts := strings.SplitN(authorizationHeader, " ", 2)
		if len(headerParts) != 2 || !strings.EqualFold(headerParts[0], "Bearer") {
			ginContext.AbortWithStatusJSON(http.StatusUnauthorized, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "UNAUTHORIZED",
					Message: "Invalid authorization header format. Expected 'Bearer <token>'",
				},
			})
			return
		}

		bearerTokenString := headerParts[1]
		tokenClaims, tokenValidationError := auth.ValidateToken(bearerTokenString, jwtSecretKey)
		if tokenValidationError != nil {
			ginContext.AbortWithStatusJSON(http.StatusUnauthorized, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "INVALID_TOKEN",
					Message: "Invalid or expired token",
				},
			})
			return
		}

		userIdentifier, parsingError := strconv.ParseInt(tokenClaims.Subject, 10, 64)
		if parsingError != nil {
			ginContext.AbortWithStatusJSON(http.StatusUnauthorized, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "INVALID_TOKEN",
					Message: "Invalid token subject",
				},
			})
			return
		}

		ginContext.Set(ContextUserIDKey, userIdentifier)
		ginContext.Set(ContextUserRoleKey, tokenClaims.Role)
		ginContext.Next()
	}
}

// JWTMiddleware is an alias for JWTAuth.
func JWTMiddleware(jwtSecretKey string) gin.HandlerFunc {
	return JWTAuth(jwtSecretKey)
}

// RequireRole is an alias for RequireRoles for single role guarding.
func RequireRole(allowedRoles ...string) gin.HandlerFunc {
	return RequireRoles(allowedRoles...)
}

// RequireRoles restricts endpoint access to only users with the specified roles.
func RequireRoles(allowedRoles ...string) gin.HandlerFunc {
	allowedRolesMap := make(map[string]bool)
	for _, roleName := range allowedRoles {
		allowedRolesMap[roleName] = true
	}

	return func(ginContext *gin.Context) {
		roleValue, roleExists := ginContext.Get(ContextUserRoleKey)
		if !roleExists {
			ginContext.AbortWithStatusJSON(http.StatusUnauthorized, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "UNAUTHORIZED",
					Message: "Authentication required",
				},
			})
			return
		}

		userRole, isRoleString := roleValue.(string)
		if !isRoleString || !allowedRolesMap[userRole] {
			ginContext.AbortWithStatusJSON(http.StatusForbidden, auth.ErrorResponse{
				Error: auth.ErrorDetail{
					Code:    "FORBIDDEN",
					Message: "Insufficient permissions to access this resource",
				},
			})
			return
		}

		ginContext.Next()
	}
}
