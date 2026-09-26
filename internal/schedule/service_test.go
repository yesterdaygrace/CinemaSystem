package schedule

import (
	"context"
	"testing"
	"time"
)

type mockScheduleRepository struct {
	scheduleMap    map[int64]*Schedule
	nextIdentifier int64
	overlapFunc    func(studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) bool
}

func newMockScheduleRepository() *mockScheduleRepository {
	return &mockScheduleRepository{
		scheduleMap:    make(map[int64]*Schedule),
		nextIdentifier: 1,
	}
}

func (mock *mockScheduleRepository) FindAll(requestContext context.Context) ([]Schedule, error) {
	var scheduleList []Schedule
	for _, scheduleRecord := range mock.scheduleMap {
		scheduleList = append(scheduleList, *scheduleRecord)
	}
	return scheduleList, nil
}

func (mock *mockScheduleRepository) FindByID(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error) {
	scheduleRecord, exists := mock.scheduleMap[scheduleIdentifier]
	if !exists {
		return nil, ErrScheduleNotFound
	}
	return scheduleRecord, nil
}

func (mock *mockScheduleRepository) Create(requestContext context.Context, scheduleRecord *Schedule) error {
	scheduleRecord.ID = mock.nextIdentifier
	mock.nextIdentifier++
	mock.scheduleMap[scheduleRecord.ID] = scheduleRecord
	return nil
}

func (mock *mockScheduleRepository) Update(requestContext context.Context, scheduleRecord *Schedule) error {
	mock.scheduleMap[scheduleRecord.ID] = scheduleRecord
	return nil
}

func (mock *mockScheduleRepository) Cancel(requestContext context.Context, scheduleIdentifier int64) (*Schedule, error) {
	scheduleRecord, exists := mock.scheduleMap[scheduleIdentifier]
	if !exists {
		return nil, ErrScheduleNotFound
	}
	scheduleRecord.Status = StatusCancelled
	return scheduleRecord, nil
}

func (mock *mockScheduleRepository) HasOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error) {
	if mock.overlapFunc != nil {
		return mock.overlapFunc(studioIdentifier, startTime, endTime, excludeScheduleID), nil
	}
	for _, scheduleRecord := range mock.scheduleMap {
		if scheduleRecord.StudioID == studioIdentifier && scheduleRecord.Status != StatusCancelled {
			if excludeScheduleID > 0 && scheduleRecord.ID == excludeScheduleID {
				continue
			}
			if startTime.Before(scheduleRecord.EndTime) && endTime.After(scheduleRecord.StartTime) {
				return true, nil
			}
		}
	}
	return false, nil
}

func (mock *mockScheduleRepository) CheckOverlap(requestContext context.Context, studioIdentifier int64, startTime, endTime time.Time, excludeScheduleID int64) (bool, error) {
	return mock.HasOverlap(requestContext, studioIdentifier, startTime, endTime, excludeScheduleID)
}

func TestScheduleService_Create(testRunner *testing.T) {
	mockRepository := newMockScheduleRepository()
	scheduleServiceInstance := NewService(mockRepository)
	testContext := context.Background()

	currentTestTime := time.Now()
	validStartTime := currentTestTime.Add(2 * time.Hour)
	validEndTime := validStartTime.Add(2 * time.Hour)

	// 1. Invalid time range: end_time <= start_time
	_, invalidTimeRangeError := scheduleServiceInstance.CreateSchedule(testContext, CreateScheduleRequest{
		MovieID:   1,
		StudioID:  1,
		StartTime: validEndTime,
		EndTime:   validStartTime,
	})
	if invalidTimeRangeError == nil {
		testRunner.Fatal("expected error when end_time <= start_time, got nil")
	}

	// 2. Successful schedule creation
	createdScheduleDTO, scheduleCreationError := scheduleServiceInstance.CreateSchedule(testContext, CreateScheduleRequest{
		MovieID:   1,
		StudioID:  1,
		StartTime: validStartTime,
		EndTime:   validEndTime,
	})
	if scheduleCreationError != nil {
		testRunner.Fatalf("expected successful schedule creation, got: %v", scheduleCreationError)
	}
	if createdScheduleDTO.ID != 1 || createdScheduleDTO.Status != StatusScheduled {
		testRunner.Fatalf("unexpected schedule data: %+v", createdScheduleDTO)
	}

	// 3. Overlapping time conflict in the same studio
	overlappingStartTime := validStartTime.Add(30 * time.Minute)
	overlappingEndTime := validEndTime.Add(30 * time.Minute)
	_, overlapScheduleError := scheduleServiceInstance.CreateSchedule(testContext, CreateScheduleRequest{
		MovieID:   2,
		StudioID:  1,
		StartTime: overlappingStartTime,
		EndTime:   overlappingEndTime,
	})
	if overlapScheduleError != ErrScheduleConflict {
		testRunner.Fatalf("expected ErrScheduleConflict, got: %v", overlapScheduleError)
	}

	// 4. Creation in a different studio succeeds even with the same time slot
	differentStudioScheduleDTO, differentStudioCreationError := scheduleServiceInstance.CreateSchedule(testContext, CreateScheduleRequest{
		MovieID:   2,
		StudioID:  2,
		StartTime: overlappingStartTime,
		EndTime:   overlappingEndTime,
	})
	if differentStudioCreationError != nil {
		testRunner.Fatalf("expected creation in different studio to succeed, got: %v", differentStudioCreationError)
	}
	if differentStudioScheduleDTO.ID != 2 {
		testRunner.Fatalf("expected schedule ID 2, got: %d", differentStudioScheduleDTO.ID)
	}

	// 5. Cancel schedule
	if cancellationError := scheduleServiceInstance.CancelSchedule(testContext, 1); cancellationError != nil {
		testRunner.Fatalf("failed to cancel schedule: %v", cancellationError)
	}

	// 6. After cancellation, the cancelled slot can be booked again without conflict
	rebookedScheduleDTO, rebookingError := scheduleServiceInstance.CreateSchedule(testContext, CreateScheduleRequest{
		MovieID:   1,
		StudioID:  1,
		StartTime: validStartTime,
		EndTime:   validEndTime,
	})
	if rebookingError != nil {
		testRunner.Fatalf("expected cancelled slot to be bookable again, got: %v", rebookingError)
	}
	if rebookedScheduleDTO.ID != 3 {
		testRunner.Fatalf("expected schedule ID 3, got: %d", rebookedScheduleDTO.ID)
	}
}
