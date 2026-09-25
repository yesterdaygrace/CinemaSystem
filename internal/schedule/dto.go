package schedule

import (
	"errors"
	"time"
)

// DTOJadwal merepresentasikan payload satu jadwal tayang dalam respons API.
type DTOJadwal struct {
	ID           int64     `json:"id" example:"1"`
	MovieID      int64     `json:"movie_id" example:"1"`
	StudioID     int64     `json:"studio_id" example:"1"`
	StartTime    time.Time `json:"start_time" example:"2026-10-01T19:00:00+07:00"`
	EndTime      time.Time `json:"end_time" example:"2026-10-01T21:10:00+07:00"`
	Status       string    `json:"status" example:"SCHEDULED"`
}

// ScheduleDTO adalah alias untuk DTOJadwal.
type ScheduleDTO = DTOJadwal

// DariModel mengonversi entitas model Jadwal menjadi DTOJadwal.
func DariModel(j *Jadwal) DTOJadwal {
	return DTOJadwal{
		ID:        j.ID,
		MovieID:   j.FilmID,
		StudioID:  j.StudioID,
		StartTime: j.WaktuMulai,
		EndTime:   j.WaktuSelesai,
		Status:    j.Status,
	}
}

// FromModel adalah alias untuk DariModel.
func FromModel(s *Schedule) ScheduleDTO {
	return DariModel(s)
}

// ResponsJadwalTunggal membungkus satu jadwal dalam respons JSON.
type ResponsJadwalTunggal struct {
	Data DTOJadwal `json:"data"`
}

// SingleScheduleResponse adalah alias untuk ResponsJadwalTunggal.
type SingleScheduleResponse = ResponsJadwalTunggal

// ResponsDaftarJadwal membungkus daftar jadwal tayang dalam respons JSON.
type ResponsDaftarJadwal struct {
	Data []DTOJadwal `json:"data"`
}

// ListScheduleResponse adalah alias untuk ResponsDaftarJadwal.
type ListScheduleResponse = ResponsDaftarJadwal

// PermintaanBuatJadwal mendefinisikan payload untuk pembuatan jadwal tayang.
type PermintaanBuatJadwal struct {
	MovieID      int64     `json:"movie_id" example:"1"`
	FilmID       int64     `json:"film_id" example:"1"`
	StudioID     int64     `json:"studio_id" binding:"required,gt=0" example:"1"`
	StartTime    time.Time `json:"start_time" example:"2026-10-01T19:00:00+07:00"`
	WaktuMulai   time.Time `json:"waktu_mulai" example:"2026-10-01T19:00:00+07:00"`
	EndTime      time.Time `json:"end_time" example:"2026-10-01T21:10:00+07:00"`
	WaktuSelesai time.Time `json:"waktu_selesai" example:"2026-10-01T21:10:00+07:00"`
}

func (r *PermintaanBuatJadwal) AmbilFilmID() int64 {
	if r.FilmID > 0 {
		return r.FilmID
	}
	return r.MovieID
}

func (r *PermintaanBuatJadwal) AmbilWaktuMulai() time.Time {
	if !r.WaktuMulai.IsZero() {
		return r.WaktuMulai
	}
	return r.StartTime
}

func (r *PermintaanBuatJadwal) AmbilWaktuSelesai() time.Time {
	if !r.WaktuSelesai.IsZero() {
		return r.WaktuSelesai
	}
	return r.EndTime
}

// Validasi memeriksa aturan bisnis pada data pembuatan jadwal.
func (r *PermintaanBuatJadwal) Validasi() error {
	filmID := r.AmbilFilmID()
	if filmID <= 0 {
		return errors.New("movie_id atau film_id harus lebih besar dari 0")
	}
	if r.StudioID <= 0 {
		return errors.New("studio_id harus lebih besar dari 0")
	}
	mulai := r.AmbilWaktuMulai()
	selesai := r.AmbilWaktuSelesai()
	if mulai.IsZero() || selesai.IsZero() {
		return errors.New("waktu_mulai dan waktu_selesai wajib diisi")
	}
	if !selesai.After(mulai) {
		return errors.New("end_time must be after start_time")
	}
	return nil
}

// Validate adalah alias untuk Validasi.
func (r *PermintaanBuatJadwal) Validate() error {
	return r.Validasi()
}

// CreateScheduleRequest adalah alias untuk PermintaanBuatJadwal.
type CreateScheduleRequest = PermintaanBuatJadwal

// PermintaanPerbaruiJadwal mendefinisikan payload untuk pembaruan jadwal tayang.
type PermintaanPerbaruiJadwal struct {
	MovieID      int64     `json:"movie_id" example:"1"`
	FilmID       int64     `json:"film_id" example:"1"`
	StudioID     int64     `json:"studio_id" binding:"required,gt=0" example:"2"`
	StartTime    time.Time `json:"start_time" example:"2026-10-01T20:00:00+07:00"`
	WaktuMulai   time.Time `json:"waktu_mulai" example:"2026-10-01T20:00:00+07:00"`
	EndTime      time.Time `json:"end_time" example:"2026-10-01T22:10:00+07:00"`
	WaktuSelesai time.Time `json:"waktu_selesai" example:"2026-10-01T22:10:00+07:00"`
}

func (r *PermintaanPerbaruiJadwal) AmbilFilmID() int64 {
	if r.FilmID > 0 {
		return r.FilmID
	}
	return r.MovieID
}

func (r *PermintaanPerbaruiJadwal) AmbilWaktuMulai() time.Time {
	if !r.WaktuMulai.IsZero() {
		return r.WaktuMulai
	}
	return r.StartTime
}

func (r *PermintaanPerbaruiJadwal) AmbilWaktuSelesai() time.Time {
	if !r.WaktuSelesai.IsZero() {
		return r.WaktuSelesai
	}
	return r.EndTime
}

// Validasi memeriksa aturan bisnis pada data pembaruan jadwal.
func (r *PermintaanPerbaruiJadwal) Validasi() error {
	filmID := r.AmbilFilmID()
	if filmID <= 0 {
		return errors.New("movie_id atau film_id harus lebih besar dari 0")
	}
	if r.StudioID <= 0 {
		return errors.New("studio_id harus lebih besar dari 0")
	}
	mulai := r.AmbilWaktuMulai()
	selesai := r.AmbilWaktuSelesai()
	if mulai.IsZero() || selesai.IsZero() {
		return errors.New("waktu_mulai dan waktu_selesai wajib diisi")
	}
	if !selesai.After(mulai) {
		return errors.New("end_time must be after start_time")
	}
	return nil
}

// Validate adalah alias untuk Validasi.
func (r *PermintaanPerbaruiJadwal) Validate() error {
	return r.Validasi()
}

// UpdateScheduleRequest adalah alias untuk PermintaanPerbaruiJadwal.
type UpdateScheduleRequest = PermintaanPerbaruiJadwal

// DetailGalat mendefinisikan informasi rincian kode galat dan pesan.
type DetailGalat struct {
	Code    string `json:"code" example:"SCHEDULE_NOT_FOUND"`
	Message string `json:"message" example:"Schedule not found"`
}

// ErrorDetail adalah alias untuk DetailGalat.
type ErrorDetail = DetailGalat

// ResponsGalat mendefinisikan amplop respons error standar.
type ResponsGalat struct {
	Error DetailGalat `json:"error"`
}

// ErrorResponse adalah alias untuk ResponsGalat.
type ErrorResponse = ResponsGalat
