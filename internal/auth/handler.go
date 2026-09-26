package auth

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
)

// AuthHandler handles HTTP requests for authentication.
type AuthHandler struct {
	authService AuthService
}

// NewHandler initializes a new AuthHandler with the given service.
func NewHandler(authService AuthService) *AuthHandler {
	return &AuthHandler{authService: authService}
}

// Login handles user authentication via email and password.
// @Summary User login
// @Description Authenticate user using email and password to obtain a JWT access token
// @Tags Authentication
// @Accept json
// @Produce json
// @Param request body LoginRequest true "User login credentials"
// @Success 200 {object} LoginResponse
// @Failure 400 {object} ErrorResponse
// @Failure 401 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /auth/login [post]
func (handler *AuthHandler) Login(ginContext *gin.Context) {
	var requestPayload LoginRequest
	if bindingError := ginContext.ShouldBindJSON(&requestPayload); bindingError != nil {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid email format or missing required fields",
			},
		})
		return
	}

	if requestPayload.EffectivePassword() == "" {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Password is required",
			},
		})
		return
	}

	loginResponse, authenticationError := handler.authService.Login(ginContext.Request.Context(), requestPayload)
	if authenticationError != nil {
		if errors.Is(authenticationError, ErrInvalidCredentials) {
			ginContext.JSON(http.StatusUnauthorized, ErrorResponse{
				Error: ErrorDetail{
					Code:    "INVALID_CREDENTIALS",
					Message: "Invalid email or password",
				},
			})
			return
		}

		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Internal server error occurred",
			},
		})
		return
	}

	ginContext.JSON(http.StatusOK, loginResponse)
}
