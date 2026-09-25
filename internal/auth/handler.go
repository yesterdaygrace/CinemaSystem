package auth

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
)

// HandlerAutentikasi menangani request HTTP untuk modul autentikasi.
type HandlerAutentikasi struct {
	layanan LayananAutentikasi
}

// Handler adalah alias untuk HandlerAutentikasi.
type Handler = HandlerAutentikasi

// BaruHandler menginisialisasi handler autentikasi baru.
func BaruHandler(layanan LayananAutentikasi) *HandlerAutentikasi {
	return &HandlerAutentikasi{layanan: layanan}
}

// NewHandler adalah alias konstruktor untuk BaruHandler.
func NewHandler(service Service) *HandlerAutentikasi {
	return BaruHandler(service)
}

// Login godoc
// @Summary Login pengguna
// @Description Otentikasi pengguna menggunakan email dan kata sandi untuk memperoleh token akses JWT
// @Tags Autentikasi
// @Accept json
// @Produce json
// @Param request body PermintaanLogin true "Kredensial login pengguna"
// @Success 200 {object} ResponsLogin
// @Failure 400 {object} ResponsGalat
// @Failure 401 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /auth/login [post]
func (h *HandlerAutentikasi) Login(c *gin.Context) {
	var permintaan PermintaanLogin
	if galat := c.ShouldBindJSON(&permintaan); galat != nil {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Format email tidak valid atau field wajib belum diisi",
			},
		})
		return
	}

	if permintaan.KataSandiEfektif() == "" {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Kata sandi wajib diisi",
			},
		})
		return
	}

	respons, galat := h.layanan.Login(c.Request.Context(), permintaan)
	if galat != nil {
		if errors.Is(galat, GalatKredensialTidakValid) {
			c.JSON(http.StatusUnauthorized, ResponsGalat{
				Error: DetailGalat{
					Code:    "INVALID_CREDENTIALS",
					Message: "Invalid email or password",
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Terjadi kesalahan internal pada server",
			},
		})
		return
	}

	c.JSON(http.StatusOK, respons)
}
