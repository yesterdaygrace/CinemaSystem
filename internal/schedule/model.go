package schedule

import "time"

const (
	StatusScheduled = "SCHEDULED"
	StatusCancelled = "CANCELLED"
	StatusCompleted = "COMPLETED"
)

// Schedule represents the 'jadwal' table in the PostgreSQL database.
type Schedule struct {
	ID        int64     `gorm:"primaryKey;autoIncrement" json:"id"`
	MovieID   int64     `gorm:"column:film_id;not null;index" json:"movie_id"`
	StudioID  int64     `gorm:"column:studio_id;not null;index" json:"studio_id"`
	StartTime time.Time `gorm:"column:waktu_mulai;not null" json:"start_time"`
	EndTime   time.Time `gorm:"column:waktu_selesai;not null" json:"end_time"`
	Status    string    `gorm:"column:status;type:varchar(50);not null;default:'SCHEDULED'" json:"status"`
	CreatedAt time.Time `gorm:"column:dibuat_pada" json:"created_at,omitempty"`
	UpdatedAt time.Time `gorm:"column:diperbarui_pada" json:"updated_at,omitempty"`
}

// TableName defines the PostgreSQL table name for GORM.
func (Schedule) TableName() string {
	return "jadwal"
}

// GetMovieID returns the movie identifier.
func (schedule *Schedule) GetMovieID() int64 {
	return schedule.MovieID
}

// GetStartTime returns the screening start timestamp.
func (schedule *Schedule) GetStartTime() time.Time {
	return schedule.StartTime
}

// GetEndTime returns the screening end timestamp.
func (schedule *Schedule) GetEndTime() time.Time {
	return schedule.EndTime
}

