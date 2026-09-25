package schedule

import (
	"errors"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

// HandlerJadwal menangani seluruh request HTTP untuk modul jadwal tayang.
type HandlerJadwal struct {
	layanan LayananJadwal
}

// Handler adalah alias untuk HandlerJadwal.
type Handler = HandlerJadwal

// BaruHandler mengembalikan instance baru HandlerJadwal.
func BaruHandler(layanan LayananJadwal) *HandlerJadwal {
	return &HandlerJadwal{layanan: layanan}
}

// NewHandler adalah alias konstruktor untuk BaruHandler.
func NewHandler(service Service) *HandlerJadwal {
	return BaruHandler(service)
}

// Daftar godoc
// @Summary Ambil daftar jadwal tayang
// @Description Mengambil seluruh daftar jadwal tayang film
// @Tags Jadwal
// @Accept json
// @Produce json
// @Security BearerAuth
// @Success 200 {object} ResponsDaftarJadwal
// @Failure 401 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /schedules [get]
func (h *HandlerJadwal) Daftar(c *gin.Context) {
	daftarJadwal, galat := h.layanan.DaftarJadwal(c.Request.Context())
	if galat != nil {
		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Gagal mengambil daftar jadwal tayang",
			},
		})
		return
	}

	c.JSON(http.StatusOK, ResponsDaftarJadwal{Data: daftarJadwal})
}

// List adalah alias pemanggil untuk Daftar.
func (h *HandlerJadwal) List(c *gin.Context) {
	h.Daftar(c)
}

// AmbilBerdasarkanID godoc
// @Summary Ambil jadwal tayang berdasarkan ID
// @Description Mengambil rincian informasi satu jadwal tayang berdasarkan ID
// @Tags Jadwal
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "ID Jadwal"
// @Success 200 {object} ResponsJadwalTunggal
// @Failure 400 {object} ResponsGalat
// @Failure 401 {object} ResponsGalat
// @Failure 404 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /schedules/{id} [get]
func (h *HandlerJadwal) AmbilBerdasarkanID(c *gin.Context) {
	idStr := c.Param("id")
	id, galat := strconv.ParseInt(idStr, 10, 64)
	if galat != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Format ID jadwal tidak valid",
			},
		})
		return
	}

	jadwal, galat := h.layanan.AmbilJadwal(c.Request.Context(), id)
	if galat != nil {
		if errors.Is(galat, GalatJadwalTidakDitemukan) {
			c.JSON(http.StatusNotFound, ResponsGalat{
				Error: DetailGalat{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Gagal mengambil jadwal",
			},
		})
		return
	}

	c.JSON(http.StatusOK, ResponsJadwalTunggal{Data: *jadwal})
}

// GetByID adalah alias pemanggil untuk AmbilBerdasarkanID.
func (h *HandlerJadwal) GetByID(c *gin.Context) {
	h.AmbilBerdasarkanID(c)
}

// Buat godoc
// @Summary Buat jadwal tayang baru
// @Description Membuat jadwal tayang film baru (Khusus Admin)
// @Tags Jadwal
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body PermintaanBuatJadwal true "Data jadwal tayang baru"
// @Success 201 {object} ResponsJadwalTunggal
// @Failure 400 {object} ResponsGalat
// @Failure 401 {object} ResponsGalat
// @Failure 403 {object} ResponsGalat
// @Failure 409 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /schedules [post]
func (h *HandlerJadwal) Buat(c *gin.Context) {
	var permintaan PermintaanBuatJadwal
	if galat := c.ShouldBindJSON(&permintaan); galat != nil {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Input payload tidak valid atau format waktu bukan RFC3339",
			},
		})
		return
	}

	if galat := permintaan.Validasi(); galat != nil {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: galat.Error(),
			},
		})
		return
	}

	jadwalBaru, galat := h.layanan.BuatJadwal(c.Request.Context(), permintaan)
	if galat != nil {
		if errors.Is(galat, GalatKonflikJadwal) {
			c.JSON(http.StatusConflict, ResponsGalat{
				Error: DetailGalat{
					Code:    "SCHEDULE_CONFLICT",
					Message: "Studio already has an overlapping schedule",
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Gagal membuat jadwal baru",
			},
		})
		return
	}

	c.JSON(http.StatusCreated, ResponsJadwalTunggal{Data: *jadwalBaru})
}

// Create adalah alias pemanggil untuk Buat.
func (h *HandlerJadwal) Create(c *gin.Context) {
	h.Buat(c)
}

// Perbarui godoc
// @Summary Perbarui jadwal tayang
// @Description Memperbarui data jadwal tayang yang sudah ada (Khusus Admin)
// @Tags Jadwal
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "ID Jadwal"
// @Param request body PermintaanPerbaruiJadwal true "Data pembaruan jadwal"
// @Success 200 {object} ResponsJadwalTunggal
// @Failure 400 {object} ResponsGalat
// @Failure 401 {object} ResponsGalat
// @Failure 403 {object} ResponsGalat
// @Failure 404 {object} ResponsGalat
// @Failure 409 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /schedules/{id} [put]
func (h *HandlerJadwal) Perbarui(c *gin.Context) {
	idStr := c.Param("id")
	id, galat := strconv.ParseInt(idStr, 10, 64)
	if galat != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Format ID jadwal tidak valid",
			},
		})
		return
	}

	var permintaan PermintaanPerbaruiJadwal
	if galat := c.ShouldBindJSON(&permintaan); galat != nil {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Input payload tidak valid atau format waktu bukan RFC3339",
			},
		})
		return
	}

	if galat := permintaan.Validasi(); galat != nil {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: galat.Error(),
			},
		})
		return
	}

	jadwalDiperbarui, galat := h.layanan.PerbaruiJadwal(c.Request.Context(), id, permintaan)
	if galat != nil {
		if errors.Is(galat, GalatJadwalTidakDitemukan) {
			c.JSON(http.StatusNotFound, ResponsGalat{
				Error: DetailGalat{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}
		if errors.Is(galat, GalatKonflikJadwal) {
			c.JSON(http.StatusConflict, ResponsGalat{
				Error: DetailGalat{
					Code:    "SCHEDULE_CONFLICT",
					Message: "Studio already has an overlapping schedule",
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Gagal memperbarui jadwal",
			},
		})
		return
	}

	c.JSON(http.StatusOK, ResponsJadwalTunggal{Data: *jadwalDiperbarui})
}

// Update adalah alias pemanggil untuk Perbarui.
func (h *HandlerJadwal) Update(c *gin.Context) {
	h.Perbarui(c)
}

// Hapus godoc
// @Summary Batalkan jadwal tayang
// @Description Membatalkan jadwal tayang secara logis (Khusus Admin)
// @Tags Jadwal
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "ID Jadwal"
// @Success 204 "No Content"
// @Failure 400 {object} ResponsGalat
// @Failure 401 {object} ResponsGalat
// @Failure 403 {object} ResponsGalat
// @Failure 404 {object} ResponsGalat
// @Failure 500 {object} ResponsGalat
// @Router /schedules/{id} [delete]
func (h *HandlerJadwal) Hapus(c *gin.Context) {
	idStr := c.Param("id")
	id, galat := strconv.ParseInt(idStr, 10, 64)
	if galat != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ResponsGalat{
			Error: DetailGalat{
				Code:    "INVALID_REQUEST",
				Message: "Format ID jadwal tidak valid",
			},
		})
		return
	}

	if galat := h.layanan.BatalkanJadwal(c.Request.Context(), id); galat != nil {
		if errors.Is(galat, GalatJadwalTidakDitemukan) {
			c.JSON(http.StatusNotFound, ResponsGalat{
				Error: DetailGalat{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, ResponsGalat{
			Error: DetailGalat{
				Code:    "INTERNAL_ERROR",
				Message: "Gagal membatalkan jadwal",
			},
		})
		return
	}

	c.Status(http.StatusNoContent)
}

// Delete adalah alias pemanggil untuk Hapus.
func (h *HandlerJadwal) Delete(c *gin.Context) {
	h.Hapus(c)
}
