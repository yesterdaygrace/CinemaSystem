package schedule

import (
	"errors"
	"time"
)

// ScheduleDTO represents a single schedule payload in API responses.
type ScheduleDTO struct {
	ID        int64     `json:"id" example:"1"`
	MovieID   int64     `json:"movie_id" example:"1"`
	StudioID  int64     `json:"studio_id" example:"1"`
	StartTime time.Time `json:"start_time" example:"2026-10-01T19:00:00+07:00"`
	EndTime   time.Time `json:"end_time" example:"2026-10-01T21:10:00+07:00"`
	Status    string    `json:"status" example:"SCHEDULED"`
}

// FromModel converts a Schedule database model entity into a ScheduleDTO.
func FromModel(scheduleRecord *Schedule) ScheduleDTO {
	return ScheduleDTO{
		ID:        scheduleRecord.ID,
		MovieID:   scheduleRecord.MovieID,
		StudioID:  scheduleRecord.StudioID,
		StartTime: scheduleRecord.StartTime,
		EndTime:   scheduleRecord.EndTime,
		Status:    scheduleRecord.Status,
	}
}

// SingleScheduleResponse wraps a single schedule item in a standard JSON response.
type SingleScheduleResponse struct {
	Data ScheduleDTO `json:"data"`
}

// ListScheduleResponse wraps a slice of schedule items in a standard JSON response.
type ListScheduleResponse struct {
	Data []ScheduleDTO `json:"data"`
}

// CreateScheduleRequest defines the payload for creating a new schedule.
type CreateScheduleRequest struct {
	MovieID   int64     `json:"movie_id" binding:"required,gt=0" example:"1"`
	StudioID  int64     `json:"studio_id" binding:"required,gt=0" example:"1"`
	StartTime time.Time `json:"start_time" binding:"required" example:"2026-10-01T19:00:00+07:00"`
	EndTime   time.Time `json:"end_time" binding:"required" example:"2026-10-01T21:10:00+07:00"`
}

// Validate checks business rules on the create schedule payload.
func (request *CreateScheduleRequest) Validate() error {
	if request.MovieID <= 0 {
		return errors.New("movie_id must be greater than 0")
	}
	if request.StudioID <= 0 {
		return errors.New("studio_id must be greater than 0")
	}
	if request.StartTime.IsZero() || request.EndTime.IsZero() {
		return errors.New("start_time and end_time are required")
	}
	if !request.EndTime.After(request.StartTime) {
		return errors.New("end_time must be after start_time")
	}
	return nil
}

// UpdateScheduleRequest defines the payload for updating an existing schedule.
type UpdateScheduleRequest struct {
	MovieID   int64     `json:"movie_id" binding:"required,gt=0" example:"1"`
	StudioID  int64     `json:"studio_id" binding:"required,gt=0" example:"2"`
	StartTime time.Time `json:"start_time" binding:"required" example:"2026-10-01T20:00:00+07:00"`
	EndTime   time.Time `json:"end_time" binding:"required" example:"2026-10-01T22:10:00+07:00"`
}

// Validate checks business rules on the update schedule payload.
func (request *UpdateScheduleRequest) Validate() error {
	if request.MovieID <= 0 {
		return errors.New("movie_id must be greater than 0")
	}
	if request.StudioID <= 0 {
		return errors.New("studio_id must be greater than 0")
	}
	if request.StartTime.IsZero() || request.EndTime.IsZero() {
		return errors.New("start_time and end_time are required")
	}
	if !request.EndTime.After(request.StartTime) {
		return errors.New("end_time must be after start_time")
	}
	return nil
}

// ErrorDetail defines detailed error information for API responses.
type ErrorDetail struct {
	Code    string `json:"code" example:"SCHEDULE_NOT_FOUND"`
	Message string `json:"message" example:"Schedule not found"`
}

// ErrorResponse wraps the standard API error response payload.
type ErrorResponse struct {
	Error ErrorDetail `json:"error"`
}
