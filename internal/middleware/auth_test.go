package middleware

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"cinema-ticket-system/internal/auth"

	"github.com/gin-gonic/gin"
)

func TestMiddlewareAuthAndRoles(testRunner *testing.T) {
	gin.SetMode(gin.TestMode)
	secretKey := "secret-test-key-321"

	adminToken, _, _ := auth.GenerateToken(1, auth.RoleAdmin, secretKey, 1)
	customerToken, _, _ := auth.GenerateToken(2, auth.RoleCustomer, secretKey, 1)

	setupTestRouter := func() *gin.Engine {
		routerEngine := gin.New()
		protectedGroup := routerEngine.Group("/protected")
		protectedGroup.Use(JWTAuth(secretKey))
		{
			protectedGroup.GET("/all", func(ginContext *gin.Context) {
				ginContext.JSON(http.StatusOK, gin.H{"status": "ok"})
			})
			protectedGroup.POST("/admin-only", RequireRoles(auth.RoleAdmin), func(ginContext *gin.Context) {
				ginContext.JSON(http.StatusCreated, gin.H{"status": "created"})
			})
		}
		return routerEngine
	}

	routerEngine := setupTestRouter()

	// 1. Missing token -> 401 Unauthorized
	missingTokenRequest, _ := http.NewRequest(http.MethodGet, "/protected/all", nil)
	missingTokenRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(missingTokenRecorder, missingTokenRequest)
	if missingTokenRecorder.Code != http.StatusUnauthorized {
		testRunner.Fatalf("expected 401 for missing token, got %d", missingTokenRecorder.Code)
	}

	// 2. Valid token -> 200 OK
	validTokenRequest, _ := http.NewRequest(http.MethodGet, "/protected/all", nil)
	validTokenRequest.Header.Set("Authorization", "Bearer "+customerToken)
	validTokenRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(validTokenRecorder, validTokenRequest)
	if validTokenRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected 200 for valid token, got %d", validTokenRecorder.Code)
	}

	// 3. Customer accessing admin-only route -> 403 Forbidden
	forbiddenRoleRequest, _ := http.NewRequest(http.MethodPost, "/protected/admin-only", nil)
	forbiddenRoleRequest.Header.Set("Authorization", "Bearer "+customerToken)
	forbiddenRoleRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(forbiddenRoleRecorder, forbiddenRoleRequest)
	if forbiddenRoleRecorder.Code != http.StatusForbidden {
		testRunner.Fatalf("expected 403 for customer on admin-only route, got %d", forbiddenRoleRecorder.Code)
	}
	var parsedErrorResponse auth.ErrorResponse
	_ = json.Unmarshal(forbiddenRoleRecorder.Body.Bytes(), &parsedErrorResponse)
	if parsedErrorResponse.Error.Code != "FORBIDDEN" {
		testRunner.Fatalf("expected error code FORBIDDEN, got %s", parsedErrorResponse.Error.Code)
	}

	// 4. Admin accessing admin-only route -> 201 Created
	authorizedAdminRequest, _ := http.NewRequest(http.MethodPost, "/protected/admin-only", nil)
	authorizedAdminRequest.Header.Set("Authorization", "Bearer "+adminToken)
	authorizedAdminRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(authorizedAdminRecorder, authorizedAdminRequest)
	if authorizedAdminRecorder.Code != http.StatusCreated {
		testRunner.Fatalf("expected 201 for admin on admin-only route, got %d", authorizedAdminRecorder.Code)
	}
}
