package database

import (
	"errors"
	"fmt"
	"log"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
)

// RunMigrations executes all pending 'up' SQL migrations from the file path to the database.
func RunMigrations(databaseURL string, migrationPath string) error {
	sourceURL := fmt.Sprintf("file://%s", migrationPath)
	migrationInstance, initializationError := migrate.New(sourceURL, databaseURL)
	if initializationError != nil {
		return fmt.Errorf("failed to initialize migration instance: %w", initializationError)
	}
	defer migrationInstance.Close()

	if migrationError := migrationInstance.Up(); migrationError != nil && !errors.Is(migrationError, migrate.ErrNoChange) {
		return fmt.Errorf("failed to apply migrations: %w", migrationError)
	}

	log.Println("Database migrations applied successfully")
	return nil
}
