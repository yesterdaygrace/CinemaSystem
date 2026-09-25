package middleware

import (
	"net/http"
	"strconv"
	"strings"

	"cinema-ticket-system/internal/auth"

	"github.com/gin-gonic/gin"
)

const (
	KunciKonteksIDPengguna    = "userID"
	KunciKonteksPeranPengguna = "userRole"

	CtxUserIDKey   = KunciKonteksIDPengguna
	CtxUserRoleKey = KunciKonteksPeranPengguna
)

// AutentikasiJWT memvalidasi token Bearer pada header Authorization.
func AutentikasiJWT(rahasia string) gin.HandlerFunc {
	return func(c *gin.Context) {
		headerOtorisasi := c.GetHeader("Authorization")
		if headerOtorisasi == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "UNAUTHORIZED",
					Message: "Authorization header is required",
				},
			})
			return
		}

		bagianHeader := strings.SplitN(headerOtorisasi, " ", 2)
		if len(bagianHeader) != 2 || !strings.EqualFold(bagianHeader[0], "Bearer") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "UNAUTHORIZED",
					Message: "Invalid authorization header format. Expected 'Bearer <token>'",
				},
			})
			return
		}

		stringToken := bagianHeader[1]
		klaim, galat := auth.ValidasiToken(stringToken, rahasia)
		if galat != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "INVALID_TOKEN",
					Message: "Invalid or expired token",
				},
			})
			return
		}

		idPengguna, galat := strconv.ParseInt(klaim.Subject, 10, 64)
		if galat != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "INVALID_TOKEN",
					Message: "Invalid token subject",
				},
			})
			return
		}

		c.Set(KunciKonteksIDPengguna, idPengguna)
		c.Set(KunciKonteksPeranPengguna, klaim.Peran)
		c.Next()
	}
}

// JWTAuth adalah alias pemanggil untuk AutentikasiJWT.
func JWTAuth(secret string) gin.HandlerFunc {
	return AutentikasiJWT(secret)
}

// WajibPeran membatasi akses endpoint hanya untuk peran yang ditentukan.
func WajibPeran(peranDiizinkan ...string) gin.HandlerFunc {
	petaPeran := make(map[string]bool)
	for _, p := range peranDiizinkan {
		petaPeran[p] = true
	}

	return func(c *gin.Context) {
		nilaiPeran, ada := c.Get(KunciKonteksPeranPengguna)
		if !ada {
			c.AbortWithStatusJSON(http.StatusUnauthorized, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "UNAUTHORIZED",
					Message: "Authentication required",
				},
			})
			return
		}

		peranPengguna, valid := nilaiPeran.(string)
		if !valid || !petaPeran[peranPengguna] {
			c.AbortWithStatusJSON(http.StatusForbidden, auth.ResponsGalat{
				Error: auth.DetailGalat{
					Code:    "FORBIDDEN",
					Message: "Insufficient permissions to access this resource",
				},
			})
			return
		}

		c.Next()
	}
}

// RequireRoles adalah alias pemanggil untuk WajibPeran.
func RequireRoles(allowedRoles ...string) gin.HandlerFunc {
	return WajibPeran(allowedRoles...)
}
