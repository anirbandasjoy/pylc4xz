#!/bin/bash
set -e

echo "Initializing PostgreSQL database..."

# Create additional extensions if needed
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Enable UUID extension (useful for future features)
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Create a simple health check table
    CREATE TABLE IF NOT EXISTS health_check (
        id SERIAL PRIMARY KEY,
        status VARCHAR(50) DEFAULT 'healthy',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Insert initial health check record
    INSERT INTO health_check (status) VALUES ('healthy');
EOSQL

echo "PostgreSQL initialization completed!"
