package schedule

import (
	"context"
	"errors"
	"time"
)

var (
	// ErrScheduleConflict is returned when a studio already has an active overlapping schedule.
	ErrScheduleConflict = errors.New("studio already has an overlapping schedule")
	// ErrInvalidTimeRange is returned when the schedule end time is before or equal to start time.
	ErrInvalidTimeRange = errors.New("end_time must be after start_time")
)

// ScheduleService defines the business logic contract for managing movie screening schedules.
type ScheduleService interface {
	ListSchedules(requestContext context.Context) ([]ScheduleDTO, error)
	GetSchedule(requestContext context.Context, scheduleIdentifier int64) (*ScheduleDTO, error)
	CreateSchedule(requestContext context.Context, requestPayload CreateScheduleRequest) (*ScheduleDTO, error)
	UpdateSchedule(requestContext context.Context, scheduleIdentifier int64, requestPayload UpdateScheduleRequest) (*ScheduleDTO, error)
	CancelSchedule(requestContext context.Context, scheduleIdentifier int64) error
}

type scheduleService struct {
	scheduleRepository ScheduleRepository
}

// NewService initializes a new ScheduleService instance with the repository.
func NewService(scheduleRepository ScheduleRepository) ScheduleService {
	return &scheduleService{scheduleRepository: scheduleRepository}
}


// ListSchedules retrieves all schedules as DTOs.
func (service *scheduleService) ListSchedules(requestContext context.Context) ([]ScheduleDTO, error) {
	scheduleList, fetchError := service.scheduleRepository.FindAll(requestContext)
	if fetchError != nil {
		return nil, fetchError
	}

	resultList := make([]ScheduleDTO, len(scheduleList))
	for index, scheduleRecord := range scheduleList {
		resultList[index] = FromModel(&scheduleRecord)
	}
	return resultList, nil
}

// GetSchedule retrieves a single schedule by ID as a DTO.
func (service *scheduleService) GetSchedule(requestContext context.Context, scheduleIdentifier int64) (*ScheduleDTO, error) {
	scheduleRecord, fetchError := service.scheduleRepository.FindByID(requestContext, scheduleIdentifier)
	if fetchError != nil {
		return nil, fetchError
	}
	scheduleDTO := FromModel(scheduleRecord)
	return &scheduleDTO, nil
}

// CreateSchedule validates and creates a new schedule ensuring no time overlap in the studio.
func (service *scheduleService) CreateSchedule(requestContext context.Context, requestPayload CreateScheduleRequest) (*ScheduleDTO, error) {
	if validationError := requestPayload.Validate(); validationError != nil {
		return nil, validationError
	}

	movieIdentifier := requestPayload.MovieID
	startTime := requestPayload.StartTime
	endTime := requestPayload.EndTime

	hasTimeOverlap, overlapCheckError := service.scheduleRepository.HasOverlap(requestContext, requestPayload.StudioID, startTime, endTime, 0)
	if overlapCheckError != nil {
		return nil, overlapCheckError
	}
	if hasTimeOverlap {
		return nil, ErrScheduleConflict
	}

	currentTimestamp := time.Now().UTC()
	newScheduleRecord := &Schedule{
		MovieID:   movieIdentifier,
		StudioID:  requestPayload.StudioID,
		StartTime: startTime,
		EndTime:   endTime,
		Status:    StatusScheduled,
		CreatedAt: currentTimestamp,
		UpdatedAt: currentTimestamp,
	}

	if creationError := service.scheduleRepository.Create(requestContext, newScheduleRecord); creationError != nil {
		return nil, creationError
	}

	scheduleDTO := FromModel(newScheduleRecord)
	return &scheduleDTO, nil
}


// UpdateSchedule validates and updates an existing schedule ensuring no time overlap with others.
func (service *scheduleService) UpdateSchedule(requestContext context.Context, scheduleIdentifier int64, requestPayload UpdateScheduleRequest) (*ScheduleDTO, error) {
	if validationError := requestPayload.Validate(); validationError != nil {
		return nil, validationError
	}

	existingScheduleRecord, fetchError := service.scheduleRepository.FindByID(requestContext, scheduleIdentifier)
	if fetchError != nil {
		return nil, fetchError
	}

	movieIdentifier := requestPayload.MovieID
	startTime := requestPayload.StartTime
	endTime := requestPayload.EndTime

	hasTimeOverlap, overlapCheckError := service.scheduleRepository.HasOverlap(requestContext, requestPayload.StudioID, startTime, endTime, scheduleIdentifier)
	if overlapCheckError != nil {
		return nil, overlapCheckError
	}
	if hasTimeOverlap {
		return nil, ErrScheduleConflict
	}

	existingScheduleRecord.MovieID = movieIdentifier
	existingScheduleRecord.StudioID = requestPayload.StudioID
	existingScheduleRecord.StartTime = startTime
	existingScheduleRecord.EndTime = endTime
	existingScheduleRecord.UpdatedAt = time.Now().UTC()

	if updateError := service.scheduleRepository.Update(requestContext, existingScheduleRecord); updateError != nil {
		return nil, updateError
	}

	scheduleDTO := FromModel(existingScheduleRecord)
	return &scheduleDTO, nil
}


// CancelSchedule marks a schedule as CANCELLED logically.
func (service *scheduleService) CancelSchedule(requestContext context.Context, scheduleIdentifier int64) error {
	_, cancelError := service.scheduleRepository.Cancel(requestContext, scheduleIdentifier)
	return cancelError
}

