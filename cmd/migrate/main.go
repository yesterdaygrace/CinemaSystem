package main

import (
	"flag"
	"log"

	"cinema-ticket-system/internal/config"
	"cinema-ticket-system/internal/database"
)

func main() {
	shouldSeedDatabase := flag.Bool("seed", false, "Seed initial records after migration succeeds")
	flag.Parse()

	appConfig, configErr := config.LoadConfig()
	if configErr != nil {
		log.Fatalf("Failed to load configuration: %v", configErr)
	}

	log.Printf("Connecting to database at %s:%s...", appConfig.DBHost, appConfig.DBPort)
	if migrationErr := database.RunMigrations(appConfig.DatabaseURL(), "migrations"); migrationErr != nil {
		log.Fatalf("Database migration failed: %v", migrationErr)
	}

	if *shouldSeedDatabase {
		dbInstance, dbErr := database.ConnectDatabase(appConfig)
		if dbErr != nil {
			log.Fatalf("Database connection failed: %v", dbErr)
		}
		if seedErr := database.SeedInitialData(dbInstance); seedErr != nil {
			log.Fatalf("Failed to seed initial database records: %v", seedErr)
		}
	}

	log.Println("Database migration command completed successfully")
}
