package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"cinema-ticket-system/internal/auth"
	"cinema-ticket-system/internal/config"
	"cinema-ticket-system/internal/database"
	"cinema-ticket-system/internal/middleware"
	"cinema-ticket-system/internal/schedule"
	"cinema-ticket-system/internal/web"

	_ "cinema-ticket-system/docs/swagger"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title Cinema Ticket System API
// @version 1.0
// @description Enterprise Cinema Ticket Reservation Backend API with JWT Authentication and Screening Schedule Management
// @host localhost:8088
// @BasePath /api/v1
// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization
// @description Enter 'Bearer <token>' for authorization
func main() {
	appConfig, configErr := config.LoadConfig()
	if configErr != nil {
		log.Fatalf("Failed to load configuration: %v", configErr)
	}

	if appConfig.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	// Connect to PostgreSQL database
	dbConnection, dbErr := database.ConnectDatabase(appConfig)
	if dbErr != nil {
		log.Fatalf("Database connection failed: %v", dbErr)
	}

	// Initialize repositories, domain services, and HTTP handlers
	userRepository := auth.NewRepository(dbConnection)
	authService := auth.NewService(userRepository, appConfig.JWTSecret, appConfig.JWTExpireHours)
	authHandler := auth.NewHandler(authService)

	scheduleRepository := schedule.NewRepository(dbConnection)
	scheduleService := schedule.NewService(scheduleRepository)
	scheduleHandler := schedule.NewHandler(scheduleService)

	// Initialize Gin HTTP router
	httpRouter := gin.Default()

	// Serve docs directory statically for diagrams, SQL scripts, and documentation assets
	httpRouter.Static("/docs", "./docs")

	// Web demo page handler (reads live file in development, falls back to embedded)
	serveWebIndex := func(ginContext *gin.Context) {
		ginContext.Header("Content-Type", "text/html; charset=utf-8")
		if content, err := os.ReadFile("internal/web/index.html"); err == nil {
			ginContext.Data(http.StatusOK, "text/html; charset=utf-8", content)
			return
		}
		ginContext.Data(http.StatusOK, "text/html; charset=utf-8", web.IndexHTML)
	}

	// Web demo aliases
	httpRouter.GET("/", rootHandler(appConfig, serveWebIndex))
	httpRouter.GET("/demo", serveWebIndex)
	httpRouter.GET("/app", serveWebIndex)

	// Swagger redirection handler
	httpRouter.GET("/swagger", func(ginContext *gin.Context) {
		ginContext.Redirect(http.StatusMovedPermanently, "/swagger/index.html")
	})

	// Swagger documentation handler with trailing slash support
	httpRouter.GET("/swagger/*any", func(ginContext *gin.Context) {
		routeParam := ginContext.Param("any")
		if routeParam == "/" || routeParam == "" {
			ginContext.Redirect(http.StatusMovedPermanently, "/swagger/index.html")
			return
		}
		ginSwagger.WrapHandler(swaggerFiles.Handler)(ginContext)
	})

	// Health check probe endpoint
	httpRouter.GET("/health", healthCheckHandler)

	// API version 1 route group
	v1ApiGroup := httpRouter.Group("/api/v1")
	{
		// Health check endpoint under /api/v1
		v1ApiGroup.GET("/health", healthCheckHandler)

		// Public authentication route
		v1ApiGroup.POST("/auth/login", authHandler.Login)

		// JWT authenticated route group
		protectedRouteGroup := v1ApiGroup.Group("")
		protectedRouteGroup.Use(middleware.JWTMiddleware(appConfig.JWTSecret))
		{
			// Schedules accessible by Customer and Admin
			protectedRouteGroup.GET("/schedules", scheduleHandler.List)
			protectedRouteGroup.GET("/schedules/:id", scheduleHandler.GetByID)

			// Admin-only mutation routes
			adminOnlyRouteGroup := protectedRouteGroup.Group("")
			adminOnlyRouteGroup.Use(middleware.RequireRole(auth.RoleAdmin))
			{
				adminOnlyRouteGroup.POST("/schedules", scheduleHandler.Create)
				adminOnlyRouteGroup.PUT("/schedules/:id", scheduleHandler.Update)
				adminOnlyRouteGroup.DELETE("/schedules/:id", scheduleHandler.Delete)
			}
		}
	}

	httpServer := &http.Server{
		Addr:         fmt.Sprintf(":%s", appConfig.Port),
		Handler:      httpRouter,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// Launch server in background goroutine
	go func() {
		log.Printf("Server listening on port %s (environment: %s)...", appConfig.Port, appConfig.Environment)
		log.Printf("Swagger documentation available at http://localhost:%s/swagger/index.html", appConfig.Port)
		if listenErr := httpServer.ListenAndServe(); listenErr != nil && !errors.Is(listenErr, http.ErrServerClosed) {
			log.Fatalf("Server ListenAndServe error: %v", listenErr)
		}
	}()

	// Await operating system interrupt signal for graceful termination
	shutdownSignalChannel := make(chan os.Signal, 1)
	signal.Notify(shutdownSignalChannel, syscall.SIGINT, syscall.SIGTERM)
	<-shutdownSignalChannel
	log.Println("Initiating graceful server shutdown...")

	shutdownContext, cancelShutdown := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancelShutdown()

	if shutdownErr := httpServer.Shutdown(shutdownContext); shutdownErr != nil {
		log.Fatalf("Server forced to shutdown: %v", shutdownErr)
	}

	log.Println("Server gracefully terminated successfully")
}

// HealthResponse represents system health probe output.
type HealthResponse struct {
	Status    string    `json:"status" example:"UP"`
	Timestamp time.Time `json:"timestamp" example:"2026-09-26T10:00:00Z"`
}

// SystemInfoResponse represents system discovery and link summary.
type SystemInfoResponse struct {
	Application string `json:"application" example:"Cinema Ticket System API"`
	Status      string `json:"status" example:"ACTIVE"`
	WebDemo     string `json:"web_demo" example:"http://localhost:8088/demo"`
	DocsSwagger string `json:"docs_swagger" example:"http://localhost:8088/swagger/index.html"`
	HealthCheck string `json:"health_check" example:"http://localhost:8088/health"`
}

// healthCheckHandler returns the operational health status of the API server.
// @Summary System Health Check
// @Description Returns the operational health status of the Cinema Ticket System API server
// @Tags System
// @Produce json
// @Success 200 {object} HealthResponse
// @Router /health [get]
func healthCheckHandler(ginContext *gin.Context) {
	ginContext.JSON(http.StatusOK, HealthResponse{
		Status:    "UP",
		Timestamp: time.Now().UTC(),
	})
}

// rootHandler serves the interactive web demo console or JSON status summary.
func rootHandler(appConfig *config.Config, serveWebIndex func(*gin.Context)) gin.HandlerFunc {
	return func(ginContext *gin.Context) {
		if ginContext.GetHeader("Accept") == "application/json" {
			ginContext.JSON(http.StatusOK, SystemInfoResponse{
				Application: "Cinema Ticket System API",
				Status:      "ACTIVE",
				WebDemo:     fmt.Sprintf("http://localhost:%s/demo", appConfig.Port),
				DocsSwagger: fmt.Sprintf("http://localhost:%s/swagger/index.html", appConfig.Port),
				HealthCheck: fmt.Sprintf("http://localhost:%s/health", appConfig.Port),
			})
			return
		}
		serveWebIndex(ginContext)
	}
}
