package tests

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"
	"time"

	"cinema-ticket-system/internal/auth"
	"cinema-ticket-system/internal/config"
	"cinema-ticket-system/internal/database"
	"cinema-ticket-system/internal/middleware"
	"cinema-ticket-system/internal/schedule"

	"github.com/gin-gonic/gin"
)

func setupTestApp(testRunner *testing.T) (*gin.Engine, *config.Config) {
	gin.SetMode(gin.TestMode)
	appConfig, configError := config.LoadConfig()
	if configError != nil {
		testRunner.Fatalf("failed to load configuration: %v", configError)
	}

	databaseConnection, dbError := database.ConnectDatabase(appConfig)
	if dbError != nil {
		testRunner.Fatalf("failed to connect to database: %v", dbError)
	}

	// Ensure database schema migrations and seed records are applied
	_ = database.RunMigrations(appConfig.URL(), "../migrations")
	_ = database.SeedInitialData(databaseConnection)

	authRepository := auth.NewRepository(databaseConnection)
	authService := auth.NewService(authRepository, appConfig.JWTSecretKey, appConfig.JWTExpirationHours)
	authHandler := auth.NewHandler(authService)

	scheduleRepository := schedule.NewRepository(databaseConnection)
	scheduleService := schedule.NewService(scheduleRepository)
	scheduleHandler := schedule.NewHandler(scheduleService)

	routerEngine := gin.New()
	routerEngine.Use(gin.Recovery())

	routerEngine.GET("/health", func(ginContext *gin.Context) {
		ginContext.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	v1ApiGroup := routerEngine.Group("/api/v1")
	{
		v1ApiGroup.POST("/auth/login", authHandler.Login)

		protectedGroup := v1ApiGroup.Group("")
		protectedGroup.Use(middleware.JWTMiddleware(appConfig.JWTSecretKey))
		{
			protectedGroup.GET("/schedules", scheduleHandler.List)
			protectedGroup.GET("/schedules/:id", scheduleHandler.GetByID)

			adminOnlyGroup := protectedGroup.Group("")
			adminOnlyGroup.Use(middleware.RequireRole(auth.RoleAdmin))
			{
				adminOnlyGroup.POST("/schedules", scheduleHandler.Create)
				adminOnlyGroup.PUT("/schedules/:id", scheduleHandler.Update)
				adminOnlyGroup.DELETE("/schedules/:id", scheduleHandler.Delete)
			}
		}
	}

	return routerEngine, appConfig
}

func loginUser(testRunner *testing.T, routerEngine *gin.Engine, emailAddress, plainPassword string) string {
	requestPayload, _ := json.Marshal(map[string]string{
		"email":    emailAddress,
		"password": plainPassword,
	})
	httpRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewBuffer(requestPayload))
	httpRequest.Header.Set("Content-Type", "application/json")
	responseRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(responseRecorder, httpRequest)

	if responseRecorder.Code != http.StatusOK {
		testRunner.Fatalf("login failed for %s with status %d: %s", emailAddress, responseRecorder.Code, responseRecorder.Body.String())
	}

	var loginResponse auth.LoginResponse
	_ = json.Unmarshal(responseRecorder.Body.Bytes(), &loginResponse)
	return loginResponse.AccessToken
}

func TestHealthCheck(testRunner *testing.T) {
	routerEngine, _ := setupTestApp(testRunner)

	httpRequest, _ := http.NewRequest(http.MethodGet, "/health", nil)
	responseRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(responseRecorder, httpRequest)

	if responseRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected status 200, got %d", responseRecorder.Code)
	}
}

func TestAuthentication_Login(testRunner *testing.T) {
	routerEngine, _ := setupTestApp(testRunner)

	// 1. Successful login as Admin
	adminAccessToken := loginUser(testRunner, routerEngine, "admin@example.com", "password123")
	if adminAccessToken == "" {
		testRunner.Fatal("admin access token must not be empty")
	}

	// 2. Successful login as Customer
	customerAccessToken := loginUser(testRunner, routerEngine, "customer@example.com", "password123")
	if customerAccessToken == "" {
		testRunner.Fatal("customer access token must not be empty")
	}

	// 3. Invalid credentials rejection
	invalidPayload, _ := json.Marshal(map[string]string{
		"email":    "admin@example.com",
		"password": "wrongpassword",
	})
	invalidRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewBuffer(invalidPayload))
	invalidRequest.Header.Set("Content-Type", "application/json")
	responseRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(responseRecorder, invalidRequest)

	if responseRecorder.Code != http.StatusUnauthorized {
		testRunner.Fatalf("expected status 401 Unauthorized, got %d", responseRecorder.Code)
	}
	var errorResponse auth.ErrorResponse
	_ = json.Unmarshal(responseRecorder.Body.Bytes(), &errorResponse)
	if errorResponse.Error.Code != "INVALID_CREDENTIALS" {
		testRunner.Fatalf("expected error code INVALID_CREDENTIALS, got: %s", errorResponse.Error.Code)
	}
}

func TestSchedule_AccessPermissions(testRunner *testing.T) {
	routerEngine, _ := setupTestApp(testRunner)

	customerAccessToken := loginUser(testRunner, routerEngine, "customer@example.com", "password123")

	// 1. Request without authorization token -> 401 Unauthorized
	unauthorizedRequest, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules", nil)
	unauthorizedRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(unauthorizedRecorder, unauthorizedRequest)
	if unauthorizedRecorder.Code != http.StatusUnauthorized {
		testRunner.Fatalf("expected status 401 Unauthorized, got %d", unauthorizedRecorder.Code)
	}

	// 2. Customer listing schedules -> 200 OK
	customerListRequest, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules", nil)
	customerListRequest.Header.Set("Authorization", "Bearer "+customerAccessToken)
	customerListRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(customerListRecorder, customerListRequest)
	if customerListRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected status 200 OK, got %d", customerListRecorder.Code)
	}

	// 3. Customer attempting to create a schedule -> 403 Forbidden
	newSchedulePayload, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  1,
		"start_time": time.Now().Add(24 * time.Hour).Format(time.RFC3339),
		"end_time":   time.Now().Add(26 * time.Hour).Format(time.RFC3339),
	})
	forbiddenRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(newSchedulePayload))
	forbiddenRequest.Header.Set("Authorization", "Bearer "+customerAccessToken)
	forbiddenRequest.Header.Set("Content-Type", "application/json")
	forbiddenRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(forbiddenRecorder, forbiddenRequest)
	if forbiddenRecorder.Code != http.StatusForbidden {
		testRunner.Fatalf("expected status 403 Forbidden, got %d: %s", forbiddenRecorder.Code, forbiddenRecorder.Body.String())
	}
}

func TestSchedule_AdminLifecycleAndConflict(testRunner *testing.T) {
	routerEngine, appConfig := setupTestApp(testRunner)
	databaseConnection, _ := database.ConnectDatabase(appConfig)

	// Clean up Studio 2 schedules prior to testing
	databaseConnection.Exec("DELETE FROM jadwal WHERE studio_id = 2")
	testRunner.Cleanup(func() {
		databaseConnection.Exec("DELETE FROM jadwal WHERE studio_id = 2")
	})

	adminAccessToken := loginUser(testRunner, routerEngine, "admin@example.com", "password123")

	screeningStartTime := time.Date(2027, 1, 15, 14, 0, 0, 0, time.UTC)
	screeningEndTime := screeningStartTime.Add(2 * time.Hour)

	// 1. Admin creates a new schedule in Studio 2 -> 201 Created
	createPayload, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  2,
		"start_time": screeningStartTime.Format(time.RFC3339),
		"end_time":   screeningEndTime.Format(time.RFC3339),
	})
	createRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(createPayload))
	createRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	createRequest.Header.Set("Content-Type", "application/json")
	createRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(createRecorder, createRequest)
	if createRecorder.Code != http.StatusCreated {
		testRunner.Fatalf("expected status 201 Created, got %d: %s", createRecorder.Code, createRecorder.Body.String())
	}

	var singleResponse schedule.SingleScheduleResponse
	_ = json.Unmarshal(createRecorder.Body.Bytes(), &singleResponse)
	createdScheduleID := singleResponse.Data.ID

	// 2. Admin creates an overlapping schedule in Studio 2 -> 409 Conflict
	conflictStartTime := screeningStartTime.Add(30 * time.Minute)
	conflictEndTime := screeningEndTime.Add(30 * time.Minute)
	conflictPayload, _ := json.Marshal(map[string]interface{}{
		"movie_id":   2,
		"studio_id":  2,
		"start_time": conflictStartTime.Format(time.RFC3339),
		"end_time":   conflictEndTime.Format(time.RFC3339),
	})
	conflictRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(conflictPayload))
	conflictRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	conflictRequest.Header.Set("Content-Type", "application/json")
	conflictRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(conflictRecorder, conflictRequest)
	if conflictRecorder.Code != http.StatusConflict {
		testRunner.Fatalf("expected status 409 Conflict, got %d: %s", conflictRecorder.Code, conflictRecorder.Body.String())
	}
	var conflictErrorResponse schedule.ErrorResponse
	_ = json.Unmarshal(conflictRecorder.Body.Bytes(), &conflictErrorResponse)
	if conflictErrorResponse.Error.Code != "SCHEDULE_CONFLICT" {
		testRunner.Fatalf("expected error code SCHEDULE_CONFLICT, got: %s", conflictErrorResponse.Error.Code)
	}

	// 3. Admin retrieves schedule details by ID -> 200 OK
	getByIDRequest, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules/"+strconv.FormatInt(createdScheduleID, 10), nil)
	getByIDRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	getByIDRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(getByIDRecorder, getByIDRequest)
	if getByIDRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected status 200 OK, got %d", getByIDRecorder.Code)
	}

	// 4. Admin updates screening schedule -> 200 OK
	updatedEndTime := screeningEndTime.Add(15 * time.Minute)
	updatePayload, _ := json.Marshal(map[string]interface{}{
		"movie_id":   1,
		"studio_id":  2,
		"start_time": screeningStartTime.Format(time.RFC3339),
		"end_time":   updatedEndTime.Format(time.RFC3339),
	})
	updateRequest, _ := http.NewRequest(http.MethodPut, "/api/v1/schedules/"+strconv.FormatInt(createdScheduleID, 10), bytes.NewBuffer(updatePayload))
	updateRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	updateRequest.Header.Set("Content-Type", "application/json")
	updateRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(updateRecorder, updateRequest)
	if updateRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected status 200 OK on schedule update, got %d: %s", updateRecorder.Code, updateRecorder.Body.String())
	}

	// 5. Admin logically cancels screening schedule -> 204 No Content
	cancelRequest, _ := http.NewRequest(http.MethodDelete, "/api/v1/schedules/"+strconv.FormatInt(createdScheduleID, 10), nil)
	cancelRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	cancelRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(cancelRecorder, cancelRequest)
	if cancelRecorder.Code != http.StatusNoContent {
		testRunner.Fatalf("expected status 204 No Content on schedule cancel, got %d: %s", cancelRecorder.Code, cancelRecorder.Body.String())
	}

	// 6. Verify schedule status transitioned to CANCELLED
	verifyRequest, _ := http.NewRequest(http.MethodGet, "/api/v1/schedules/"+strconv.FormatInt(createdScheduleID, 10), nil)
	verifyRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	verifyRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(verifyRecorder, verifyRequest)
	if verifyRecorder.Code != http.StatusOK {
		testRunner.Fatalf("expected status 200 OK, got %d", verifyRecorder.Code)
	}
	var getScheduleResponse schedule.SingleScheduleResponse
	_ = json.Unmarshal(verifyRecorder.Body.Bytes(), &getScheduleResponse)
	if getScheduleResponse.Data.Status != schedule.StatusCancelled {
		testRunner.Fatalf("expected status CANCELLED, got: %s", getScheduleResponse.Data.Status)
	}

	// 7. Verify previously cancelled time slot can now be scheduled again without conflict
	rebookRequest, _ := http.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewBuffer(createPayload))
	rebookRequest.Header.Set("Authorization", "Bearer "+adminAccessToken)
	rebookRequest.Header.Set("Content-Type", "application/json")
	rebookRecorder := httptest.NewRecorder()
	routerEngine.ServeHTTP(rebookRecorder, rebookRequest)
	if rebookRecorder.Code != http.StatusCreated {
		testRunner.Fatalf("expected status 201 Created after prior schedule cancelled, got %d: %s", rebookRecorder.Code, rebookRecorder.Body.String())
	}
}
