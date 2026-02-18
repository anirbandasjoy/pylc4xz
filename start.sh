#!/bin/bash

# FastAPI Authentication System - Quick Start Script
# This script sets up PostgreSQL with Docker and starts the FastAPI application

set -e

echo "================================================"
echo "  FastAPI Authentication System - Quick Start"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Start PostgreSQL
echo "🐚 Starting PostgreSQL with Docker Compose..."
docker-compose up -d

echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is running
if docker-compose ps | grep -q "fastapi_postgres.*Up"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ Failed to start PostgreSQL. Check logs with: docker-compose logs postgres"
    exit 1
fi

echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created from .env.example"
else
    echo "✅ .env file already exists"
fi

echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "================================================"
echo "  ✅ Setup Complete!"
echo "================================================"
echo ""
echo "📝 To start the FastAPI application, run:"
echo ""
echo "   source venv/bin/activate  # Activate virtual environment"
echo "   uvicorn main:app --reload # Start FastAPI"
echo ""
echo "🌐 Your endpoints:"
echo "   - API:        http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc:      http://localhost:8000/redoc"
echo "   - pgAdmin:    http://localhost:5050"
echo ""
echo "📚 Database credentials (Docker):"
echo "   - Database: fastapi_db"
echo "   - Username: fastapi_user"
echo "   - Password: fastapi_password"
echo "   - Host:     localhost"
echo "   - Port:     5432"
echo ""
echo "🛑 To stop PostgreSQL:"
echo "   docker-compose down"
echo ""
echo "================================================"
