package database

import (
	"fmt"
	"log"

	"cinema-ticket-system/internal/config"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// Connect establishes a GORM connection to PostgreSQL using the provided configuration
// and configures the database connection pool settings.
func Connect(configuration *config.Config) (*gorm.DB, error) {
	logLevel := logger.Warn
	if configuration.Environment == "development" {
		logLevel = logger.Info
	}

	databaseConnection, connectionError := gorm.Open(postgres.Open(configuration.DSN()), &gorm.Config{
		Logger: logger.Default.LogMode(logLevel),
	})
	if connectionError != nil {
		return nil, fmt.Errorf("failed to connect to PostgreSQL database: %w", connectionError)
	}

	genericSQLDatabase, databaseError := databaseConnection.DB()
	if databaseError != nil {
		return nil, fmt.Errorf("failed to retrieve generic sql.DB handle: %w", databaseError)
	}

	// Configure connection pooling
	genericSQLDatabase.SetMaxOpenConns(configuration.DatabaseMaxOpenConnections)
	genericSQLDatabase.SetMaxIdleConns(configuration.DatabaseMaxIdleConnections)
	genericSQLDatabase.SetConnMaxLifetime(configuration.DatabaseConnectionMaxLifetime)

	if pingError := genericSQLDatabase.Ping(); pingError != nil {
		return nil, fmt.Errorf("failed to ping PostgreSQL database: %w", pingError)
	}

	log.Println("Successfully connected to PostgreSQL database")
	return databaseConnection, nil
}

// ConnectDatabase is an alias for Connect.
func ConnectDatabase(configuration *config.Config) (*gorm.DB, error) {
	return Connect(configuration)
}
