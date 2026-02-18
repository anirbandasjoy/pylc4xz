#!/bin/bash

# FastAPI Authentication System - Start with Alternative Port
# This script starts PostgreSQL on port 5433 instead of 5432
# Use this when port 5432 is already in use

set -e

echo "================================================"
echo "  FastAPI - Starting with Alternative Port"
echo "  PostgreSQL will run on port 5433"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    exit 1
fi

echo "🐚 Starting PostgreSQL on port 5433..."
docker-compose -f docker-compose-alt-port.yml up -d

echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

if docker-compose -f docker-compose-alt-port.yml ps | grep -q "fastapi_postgres.*Up"; then
    echo "✅ PostgreSQL is running on port 5433"
else
    echo "❌ Failed to start PostgreSQL."
    exit 1
fi

echo ""

# Create .env file with alternative port
if [ ! -f .env ]; then
    echo "📝 Creating .env file with alternative port configuration..."
    cp .env.alt-port .env
    echo "✅ .env file created (using port 5433)"
elif ! grep -q "5433" .env; then
    echo "⚠️  .env file exists but uses port 5432"
    echo "📝 Updating .env to use port 5433..."
    cp .env.alt-port .env
    echo "✅ .env file updated to use port 5433"
else
    echo "✅ .env file already configured for port 5433"
fi

echo ""
echo "================================================"
echo "  ✅ Setup Complete!"
echo "================================================"
echo ""
echo "📝 To start the FastAPI application:"
echo ""
echo "   uvicorn main:app --reload"
echo ""
echo "🌐 Your endpoints:"
echo "   - API:        http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - pgAdmin:    http://localhost:5050"
echo ""
echo "📚 Database credentials:"
echo "   - Database: fastapi_db"
echo "   - Username: fastapi_user"
echo "   - Password: fastapi_password"
echo "   - Host:     localhost"
echo "   - Port:     5433 (alternative port)"
echo ""
echo "🛑 To stop PostgreSQL:"
echo "   docker-compose -f docker-compose-alt-port.yml down"
echo ""
echo "================================================"
