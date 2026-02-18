@echo off
REM FastAPI Authentication System - Quick Start Script for Windows
REM This script sets up PostgreSQL with Docker and starts the FastAPI application

echo ================================================
echo   FastAPI Authentication System - Quick Start
echo ================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Visit: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose found
echo.

REM Start PostgreSQL
echo 🐚 Starting PostgreSQL with Docker Compose...
docker-compose up -d

echo.
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

echo.
echo ✅ PostgreSQL started
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env >nul
    echo ✅ .env file created from .env.example
) else (
    echo ✅ .env file already exists
)

echo.
echo ================================================
echo   ✅ Setup Complete!
echo ================================================
echo.
echo 📝 To start the FastAPI application, run:
echo.
echo    uvicorn main:app --reload
echo.
echo 🌐 Your endpoints:
echo    - API:        http://localhost:8000
echo    - Swagger UI: http://localhost:8000/docs
echo    - ReDoc:      http://localhost:8000/redoc
echo    - pgAdmin:    http://localhost:5050
echo.
echo 📚 Database credentials (Docker):
echo    - Database: fastapi_db
echo    - Username: fastapi_user
echo    - Password: fastapi_password
echo    - Host:     localhost
echo    - Port:     5432
echo.
echo 🛑 To stop PostgreSQL:
echo    docker-compose down
echo.
echo ================================================
pause
