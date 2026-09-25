package middleware

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"cinema-ticket-system/internal/auth"

	"github.com/gin-gonic/gin"
)

func TestMiddlewareAuthAndRoles(t *testing.T) {
	gin.SetMode(gin.TestMode)
	secret := "secret-test-key-321"

	adminToken, _, _ := auth.GenerateToken(1, auth.RoleAdmin, secret, 1)
	customerToken, _, _ := auth.GenerateToken(2, auth.RoleCustomer, secret, 1)

	setupRouter := func() *gin.Engine {
		r := gin.New()
		protected := r.Group("/protected")
		protected.Use(JWTAuth(secret))
		{
			protected.GET("/all", func(c *gin.Context) {
				c.JSON(http.StatusOK, gin.H{"status": "ok"})
			})
			protected.POST("/admin-only", RequireRoles(auth.RoleAdmin), func(c *gin.Context) {
				c.JSON(http.StatusCreated, gin.H{"status": "created"})
			})
		}
		return r
	}

	router := setupRouter()

	// 1. Missing token -> 401
	req1, _ := http.NewRequest(http.MethodGet, "/protected/all", nil)
	w1 := httptest.NewRecorder()
	router.ServeHTTP(w1, req1)
	if w1.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401 for missing token, got %d", w1.Code)
	}

	// 2. Valid token -> 200
	req2, _ := http.NewRequest(http.MethodGet, "/protected/all", nil)
	req2.Header.Set("Authorization", "Bearer "+customerToken)
	w2 := httptest.NewRecorder()
	router.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Fatalf("expected 200 for valid token, got %d", w2.Code)
	}

	// 3. Customer accessing admin-only -> 403
	req3, _ := http.NewRequest(http.MethodPost, "/protected/admin-only", nil)
	req3.Header.Set("Authorization", "Bearer "+customerToken)
	w3 := httptest.NewRecorder()
	router.ServeHTTP(w3, req3)
	if w3.Code != http.StatusForbidden {
		t.Fatalf("expected 403 for customer on admin-only route, got %d", w3.Code)
	}
	var errResp auth.ErrorResponse
	_ = json.Unmarshal(w3.Body.Bytes(), &errResp)
	if errResp.Error.Code != "FORBIDDEN" {
		t.Fatalf("expected error code FORBIDDEN, got %s", errResp.Error.Code)
	}

	// 4. Admin accessing admin-only -> 201
	req4, _ := http.NewRequest(http.MethodPost, "/protected/admin-only", nil)
	req4.Header.Set("Authorization", "Bearer "+adminToken)
	w4 := httptest.NewRecorder()
	router.ServeHTTP(w4, req4)
	if w4.Code != http.StatusCreated {
		t.Fatalf("expected 201 for admin on admin-only route, got %d", w4.Code)
	}
}
