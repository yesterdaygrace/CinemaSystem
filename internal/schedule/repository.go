package schedule

import (
	"context"
	"errors"
	"time"

	"gorm.io/gorm"
)

var (
	// ErrScheduleNotFound is returned when a requested schedule cannot be found.
	ErrScheduleNotFound = errors.New("schedule not found")
)

// ScheduleRepository defines query and persistence operations for movie schedules.
type ScheduleRepository interface {
	FindAll(requestContext context.Context) ([]Schedule, error)
	FindByID(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error)
	Create(requestContext context.Context, scheduleRecord *Schedule) error
	Update(requestContext context.Context, scheduleRecord *Schedule) error
	Cancel(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error)
	HasOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error)
	CheckOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error)
}

type scheduleRepository struct {
	databaseConnection *gorm.DB
}

// NewRepository initializes a new ScheduleRepository instance.
func NewRepository(databaseConnection *gorm.DB) ScheduleRepository {
	return &scheduleRepository{databaseConnection: databaseConnection}
}

// FindAll retrieves all schedules sorted by start time ascending.
func (repository *scheduleRepository) FindAll(requestContext context.Context) ([]Schedule, error) {
	var scheduleList []Schedule
	if queryError := repository.databaseConnection.WithContext(requestContext).Order("waktu_mulai ASC").Find(&scheduleList).Error; queryError != nil {
		return nil, queryError
	}
	return scheduleList, nil
}

// FindByID retrieves a single schedule record by its primary key identifier.
func (repository *scheduleRepository) FindByID(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error) {
	var scheduleRecord Schedule
	if databaseError := repository.databaseConnection.WithContext(requestContext).First(&scheduleRecord, scheduleIdentifier).Error; databaseError != nil {
		if errors.Is(databaseError, gorm.ErrRecordNotFound) {
			return nil, ErrScheduleNotFound
		}
		return nil, databaseError
	}
	return &scheduleRecord, nil
}

// Create inserts a new schedule into the database.
func (repository *scheduleRepository) Create(requestContext context.Context, scheduleRecord *Schedule) error {
	return repository.databaseConnection.WithContext(requestContext).Create(scheduleRecord).Error
}

// Update saves changes to an existing schedule record.
func (repository *scheduleRepository) Update(requestContext context.Context, scheduleRecord *Schedule) error {
	return repository.databaseConnection.WithContext(requestContext).Save(scheduleRecord).Error
}

// Cancel updates a schedule's status to CANCELLED logically.
func (repository *scheduleRepository) Cancel(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error) {
	var scheduleRecord Schedule
	if findError := repository.databaseConnection.WithContext(requestContext).First(&scheduleRecord, scheduleIdentifier).Error; findError != nil {
		if errors.Is(findError, gorm.ErrRecordNotFound) {
			return nil, ErrScheduleNotFound
		}
		return nil, findError
	}

	scheduleRecord.Status = StatusCancelled
	scheduleRecord.UpdatedAt = time.Now().UTC()
	if saveError := repository.databaseConnection.WithContext(requestContext).Save(&scheduleRecord).Error; saveError != nil {
		return nil, saveError
	}

	return &scheduleRecord, nil
}

// HasOverlap determines whether another non-cancelled schedule conflicts with the specified time range.
func (repository *scheduleRepository) HasOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error) {
	var overlapCount int64
	overlapQuery := repository.databaseConnection.WithContext(requestContext).
		Model(&Schedule{}).
		Where("studio_id = ?", studioIdentifier).
		Where("status != ?", StatusCancelled).
		Where("waktu_mulai < ? AND waktu_selesai > ?", endTime, startTime)

	if excludeScheduleID > 0 {
		overlapQuery = overlapQuery.Where("id != ?", excludeScheduleID)
	}

	if countError := overlapQuery.Count(&overlapCount).Error; countError != nil {
		return false, countError
	}

	return overlapCount > 0, nil
}

// CheckOverlap is an alias for HasOverlap.
func (repository *scheduleRepository) CheckOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error) {
	return repository.HasOverlap(requestContext, studioIdentifier, startTime, endTime, excludeScheduleID)
}
