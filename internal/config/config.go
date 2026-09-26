package config

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
)

// Config stores all application configuration parameters.
type Config struct {
	Port                          string
	Environment                   string
	DatabaseHost                  string
	DatabasePort                  string
	DatabaseUser                  string
	DatabasePassword              string
	DatabaseName                  string
	DatabaseSSLMode               string
	DatabaseMaxOpenConnections    int
	DatabaseMaxIdleConnections    int
	DatabaseConnectionMaxLifetime time.Duration
	JWTSecretKey                  string
	JWTExpirationHours            int

	// Convenient short aliases
	DBHost            string
	DBPort            string
	DBUser            string
	DBPassword        string
	DBName            string
	DBSSLMode         string
	DBMaxOpenConns    int
	DBMaxIdleConns    int
	DBConnMaxLifetime time.Duration
	JWTSecret         string
	JWTExpireHours    int
	Env               string
}

// LoadConfig loads the configuration from environment variables or .env file.
func LoadConfig() (*Config, error) {
	_ = godotenv.Load()

	maxOpenConnections := getEnvironmentVariableAsInteger("DB_MAX_OPEN_CONNS", 25)
	maxIdleConnections := getEnvironmentVariableAsInteger("DB_MAX_IDLE_CONNS", 10)
	connectionLifetimeMinutes := getEnvironmentVariableAsInteger("DB_CONN_MAX_LIFETIME_MINUTES", 5)
	jwtExpirationHours := getEnvironmentVariableAsInteger("JWT_EXPIRE_HOURS", 24)

	serverPort := getEnvironmentVariable("PORT", "8088")
	environmentName := getEnvironmentVariable("ENV", "development")
	databaseHost := getEnvironmentVariable("DB_HOST", "localhost")
	databasePort := getEnvironmentVariable("DB_PORT", "5432")
	databaseUser := getEnvironmentVariable("DB_USER", "bioskop")
	databasePassword := getEnvironmentVariable("DB_PASSWORD", "bioskop_dev")
	databaseName := getEnvironmentVariable("DB_NAME", "bioskop")
	databaseSSLMode := getEnvironmentVariable("DB_SSLMODE", "disable")
	jwtSecretKey := getEnvironmentVariable("JWT_SECRET", "cinema_system_jwt_secret_key_2026")

	connectionLifetimeDuration := time.Duration(connectionLifetimeMinutes) * time.Minute

	applicationConfig := &Config{
		Port:                          serverPort,
		Environment:                   environmentName,
		DatabaseHost:                  databaseHost,
		DatabasePort:                  databasePort,
		DatabaseUser:                  databaseUser,
		DatabasePassword:              databasePassword,
		DatabaseName:                  databaseName,
		DatabaseSSLMode:               databaseSSLMode,
		DatabaseMaxOpenConnections:    maxOpenConnections,
		DatabaseMaxIdleConnections:    maxIdleConnections,
		DatabaseConnectionMaxLifetime: connectionLifetimeDuration,
		JWTSecretKey:                  jwtSecretKey,
		JWTExpirationHours:            jwtExpirationHours,

		// Short aliases
		DBHost:            databaseHost,
		DBPort:            databasePort,
		DBUser:            databaseUser,
		DBPassword:        databasePassword,
		DBName:            databaseName,
		DBSSLMode:         databaseSSLMode,
		DBMaxOpenConns:    maxOpenConnections,
		DBMaxIdleConns:    maxIdleConnections,
		DBConnMaxLifetime: connectionLifetimeDuration,
		JWTSecret:         jwtSecretKey,
		JWTExpireHours:    jwtExpirationHours,
		Env:               environmentName,
	}

	return applicationConfig, nil
}

// DSN returns the PostgreSQL Data Source Name string for GORM.
func (configuration *Config) DSN() string {
	return fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=%s TimeZone=UTC",
		configuration.DatabaseHost, configuration.DatabaseUser, configuration.DatabasePassword,
		configuration.DatabaseName, configuration.DatabasePort, configuration.DatabaseSSLMode)
}

// URL returns the standard PostgreSQL connection URI string.
func (configuration *Config) URL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=%s",
		configuration.DatabaseUser, configuration.DatabasePassword, configuration.DatabaseHost,
		configuration.DatabasePort, configuration.DatabaseName, configuration.DatabaseSSLMode)
}

// DatabaseURL returns the PostgreSQL connection URI.
func (configuration *Config) DatabaseURL() string {
	return configuration.URL()
}

func getEnvironmentVariable(environmentKey, fallbackValue string) string {
	if environmentValue, exists := os.LookupEnv(environmentKey); exists && environmentValue != "" {
		return environmentValue
	}
	return fallbackValue
}

func getEnvironmentVariableAsInteger(environmentKey string, fallbackValue int) int {
	environmentValueText := getEnvironmentVariable(environmentKey, "")
	if integerValue, conversionError := strconv.Atoi(environmentValueText); conversionError == nil {
		return integerValue
	}
	return fallbackValue
}
