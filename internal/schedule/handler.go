package schedule

import (
	"errors"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

// ScheduleHandler handles all HTTP requests for movie screening schedules.
type ScheduleHandler struct {
	scheduleService ScheduleService
}

// NewHandler initializes a new ScheduleHandler instance.
func NewHandler(scheduleService ScheduleService) *ScheduleHandler {
	return &ScheduleHandler{scheduleService: scheduleService}
}

// List handles retrieving all movie schedules.
// @Summary Get schedule list
// @Description Retrieve all movie screening schedules
// @Tags Schedules
// @Accept json
// @Produce json
// @Security BearerAuth
// @Success 200 {object} ListScheduleResponse
// @Failure 401 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /schedules [get]
func (handler *ScheduleHandler) List(ginContext *gin.Context) {
	scheduleList, serviceError := handler.scheduleService.ListSchedules(ginContext.Request.Context())
	if serviceError != nil {
		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Failed to retrieve schedule list",
			},
		})
		return
	}

	ginContext.JSON(http.StatusOK, ListScheduleResponse{Data: scheduleList})
}

// GetByID handles retrieving a single schedule by ID.
// @Summary Get schedule by ID
// @Description Retrieve detailed information for a single screening schedule
// @Tags Schedules
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "Schedule ID"
// @Success 200 {object} SingleScheduleResponse
// @Failure 400 {object} ErrorResponse
// @Failure 401 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /schedules/{id} [get]
func (handler *ScheduleHandler) GetByID(ginContext *gin.Context) {
	idParameterString := ginContext.Param("id")
	scheduleIdentifier, parsingError := strconv.ParseInt(idParameterString, 10, 64)
	if parsingError != nil || scheduleIdentifier <= 0 {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid schedule ID parameter format",
			},
		})
		return
	}

	scheduleDTO, serviceError := handler.scheduleService.GetSchedule(ginContext.Request.Context(), scheduleIdentifier)
	if serviceError != nil {
		if errors.Is(serviceError, ErrScheduleNotFound) {
			ginContext.JSON(http.StatusNotFound, ErrorResponse{
				Error: ErrorDetail{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}

		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Failed to retrieve schedule",
			},
		})
		return
	}

	ginContext.JSON(http.StatusOK, SingleScheduleResponse{Data: *scheduleDTO})
}

// Create handles creating a new screening schedule (Admin only).
// @Summary Create a new schedule
// @Description Create a new movie screening schedule (Admin only)
// @Tags Schedules
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateScheduleRequest true "New schedule payload"
// @Success 201 {object} SingleScheduleResponse
// @Failure 400 {object} ErrorResponse
// @Failure 401 {object} ErrorResponse
// @Failure 403 {object} ErrorResponse
// @Failure 409 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /schedules [post]
func (handler *ScheduleHandler) Create(ginContext *gin.Context) {
	var requestPayload CreateScheduleRequest
	if bindingError := ginContext.ShouldBindJSON(&requestPayload); bindingError != nil {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid request payload or time format is not RFC3339",
			},
		})
		return
	}

	if validationError := requestPayload.Validate(); validationError != nil {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: validationError.Error(),
			},
		})
		return
	}

	createdScheduleDTO, serviceError := handler.scheduleService.CreateSchedule(ginContext.Request.Context(), requestPayload)
	if serviceError != nil {
		if errors.Is(serviceError, ErrScheduleConflict) {
			ginContext.JSON(http.StatusConflict, ErrorResponse{
				Error: ErrorDetail{
					Code:    "SCHEDULE_CONFLICT",
					Message: "Studio already has an overlapping schedule",
				},
			})
			return
		}

		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Failed to create schedule",
			},
		})
		return
	}

	ginContext.JSON(http.StatusCreated, SingleScheduleResponse{Data: *createdScheduleDTO})
}

// Update handles updating an existing screening schedule (Admin only).
// @Summary Update schedule
// @Description Update an existing screening schedule (Admin only)
// @Tags Schedules
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "Schedule ID"
// @Param request body UpdateScheduleRequest true "Updated schedule payload"
// @Success 200 {object} SingleScheduleResponse
// @Failure 400 {object} ErrorResponse
// @Failure 401 {object} ErrorResponse
// @Failure 403 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 409 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /schedules/{id} [put]
func (handler *ScheduleHandler) Update(ginContext *gin.Context) {
	idParameterString := ginContext.Param("id")
	scheduleIdentifier, parsingError := strconv.ParseInt(idParameterString, 10, 64)
	if parsingError != nil || scheduleIdentifier <= 0 {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid schedule ID parameter format",
			},
		})
		return
	}

	var requestPayload UpdateScheduleRequest
	if bindingError := ginContext.ShouldBindJSON(&requestPayload); bindingError != nil {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid request payload or time format is not RFC3339",
			},
		})
		return
	}

	if validationError := requestPayload.Validate(); validationError != nil {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: validationError.Error(),
			},
		})
		return
	}

	updatedScheduleDTO, serviceError := handler.scheduleService.UpdateSchedule(ginContext.Request.Context(), scheduleIdentifier, requestPayload)
	if serviceError != nil {
		if errors.Is(serviceError, ErrScheduleNotFound) {
			ginContext.JSON(http.StatusNotFound, ErrorResponse{
				Error: ErrorDetail{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}
		if errors.Is(serviceError, ErrScheduleConflict) {
			ginContext.JSON(http.StatusConflict, ErrorResponse{
				Error: ErrorDetail{
					Code:    "SCHEDULE_CONFLICT",
					Message: "Studio already has an overlapping schedule",
				},
			})
			return
		}

		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Failed to update schedule",
			},
		})
		return
	}

	ginContext.JSON(http.StatusOK, SingleScheduleResponse{Data: *updatedScheduleDTO})
}

// Delete handles logically cancelling a screening schedule (Admin only).
// @Summary Cancel schedule
// @Description Logically cancel a screening schedule (Admin only)
// @Tags Schedules
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path int true "Schedule ID"
// @Success 204 "No Content"
// @Failure 400 {object} ErrorResponse
// @Failure 401 {object} ErrorResponse
// @Failure 403 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /schedules/{id} [delete]
func (handler *ScheduleHandler) Delete(ginContext *gin.Context) {
	idParameterString := ginContext.Param("id")
	scheduleIdentifier, parsingError := strconv.ParseInt(idParameterString, 10, 64)
	if parsingError != nil || scheduleIdentifier <= 0 {
		ginContext.JSON(http.StatusBadRequest, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INVALID_REQUEST",
				Message: "Invalid schedule ID parameter format",
			},
		})
		return
	}

	if serviceError := handler.scheduleService.CancelSchedule(ginContext.Request.Context(), scheduleIdentifier); serviceError != nil {
		if errors.Is(serviceError, ErrScheduleNotFound) {
			ginContext.JSON(http.StatusNotFound, ErrorResponse{
				Error: ErrorDetail{
					Code:    "SCHEDULE_NOT_FOUND",
					Message: "Schedule not found",
				},
			})
			return
		}

		ginContext.JSON(http.StatusInternalServerError, ErrorResponse{
			Error: ErrorDetail{
				Code:    "INTERNAL_ERROR",
				Message: "Failed to cancel schedule",
			},
		})
		return
	}

	ginContext.Status(http.StatusNoContent)
}
