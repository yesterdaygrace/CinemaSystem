package schedule

import "time"

const (
	StatusJadwal      = "SCHEDULED"
	StatusDibatalkan  = "CANCELLED"
	StatusSelesai     = "COMPLETED"

	// Alias status
	StatusScheduled = StatusJadwal
	StatusCancelled = StatusDibatalkan
	StatusCompleted = StatusSelesai
)

// Jadwal merepresentasikan tabel jadwal pada basis data PostgreSQL.
type Jadwal struct {
	ID            int64     `gorm:"primaryKey;autoIncrement" json:"id"`
	FilmID        int64     `gorm:"column:film_id;not null;index" json:"movie_id"`
	StudioID      int64     `gorm:"column:studio_id;not null;index" json:"studio_id"`
	WaktuMulai    time.Time `gorm:"column:waktu_mulai;not null" json:"start_time"`
	WaktuSelesai  time.Time `gorm:"column:waktu_selesai;not null" json:"end_time"`
	Status        string    `gorm:"column:status;type:varchar(50);not null;default:'SCHEDULED'" json:"status"`
	DibuatPada    time.Time `gorm:"column:dibuat_pada" json:"created_at,omitempty"`
	DiperbaruiPada time.Time `gorm:"column:diperbarui_pada" json:"updated_at,omitempty"`
}

// TableName menentukan nama tabel relasional GORM.
func (Jadwal) TableName() string {
	return "jadwal"
}

// Schedule adalah alias untuk Jadwal demi kompatibilitas.
type Schedule = Jadwal
