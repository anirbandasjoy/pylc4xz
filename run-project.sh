#!/bin/bash

# FastAPI Full Project Runner - Interactive Mode
# This script helps you run the complete project in interactive mode

set -e

echo "================================================"
echo "  🚀 FastAPI Authentication System"
echo "  Interactive Mode Setup"
echo "================================================"
echo ""

# Check if required commands exist
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ All prerequisites found!"
echo ""

# Function to show menu
show_menu() {
    echo ""
    echo "================================================"
    echo "  What would you like to do?"
    echo "================================================"
    echo ""
    echo "  1) 🚀 Start PostgreSQL (Docker)"
    echo "  2) 🐍 Start FastAPI Application"
    echo "  3) 🔄 Start Both (PostgreSQL + FastAPI)"
    echo "  4) 🧹 Cleanup All Containers"
    echo "  5) 📊 Check Status"
    echo "  6) 🗄️  Open Database Shell"
    echo "  7) 📚 View Logs"
    echo "  8) ❌ Exit"
    echo ""
    read -p "Enter your choice [1-8]: " choice
    echo ""
}

# Function to start PostgreSQL
start_postgres() {
    echo "🐚 Starting PostgreSQL in Docker..."
    echo ""
    echo "Starting docker-compose (interactive mode)..."
    echo "Press Ctrl+C to stop PostgreSQL"
    echo ""
    docker-compose up
}

# Function to start FastAPI
start_fastapi() {
    echo "🐍 Starting FastAPI Application..."
    echo ""

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
        echo "✅ Virtual environment created"
    fi

    # Activate virtual environment
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate

    # Install dependencies if needed
    if ! python -c "import fastapi" 2>/dev/null; then
        echo "📥 Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        echo "✅ Dependencies installed"
    fi

    # Create .env if needed
    if [ ! -f .env ]; then
        echo "📝 Creating .env file..."
        cp .env.example .env
        echo "✅ .env file created"
    fi

    echo ""
    echo "✅ Starting FastAPI on http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop FastAPI"
    echo ""
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to check status
check_status() {
    echo "📊 System Status"
    echo ""
    echo "Docker Containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  No containers running"
    echo ""

    if docker ps | grep -q "fastapi_postgres"; then
        echo "✅ PostgreSQL is running"
    else
        echo "❌ PostgreSQL is NOT running"
    fi

    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ FastAPI is running"
    else
        echo "❌ FastAPI is NOT running"
    fi
    echo ""

    read -p "Press Enter to continue..."
}

# Function to open database shell
open_db_shell() {
    if docker ps | grep -q "fastapi_postgres"; then
        echo "🗄️  Opening PostgreSQL shell..."
        echo "Type '\\q' to exit"
        echo ""
        docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db
    else
        echo "❌ PostgreSQL is not running. Start it first (option 1)"
    fi
    read -p "Press Enter to continue..."
}

# Function to view logs
view_logs() {
    echo "📚 Showing PostgreSQL logs (Ctrl+C to exit)..."
    echo ""
    docker-compose logs -f postgres
}

# Function to cleanup
cleanup_all() {
    echo "🧹 Cleaning up..."
    echo ""

    read -p "Stop all containers? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker stop $(docker ps -aq) 2>/dev/null || echo "No running containers"
        echo "✅ All containers stopped"
    fi

    read -p "Remove all containers? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"
        echo "✅ All containers removed"
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# Function to start both
start_both() {
    echo "🔄 Starting PostgreSQL and FastAPI..."
    echo ""
    echo "You will need TWO terminal windows:"
    echo ""
    echo "Terminal 1 (this one): PostgreSQL"
    echo "Terminal 2: FastAPI"
    echo ""
    read -p "Press Enter to start PostgreSQL, then open a new terminal for FastAPI..."

    start_postgres
}

# Main loop
while true; do
    clear
    echo "================================================"
    echo "  🚀 FastAPI Authentication System"
    echo "  Current Status:"
    echo "================================================"
    echo ""

    # Show quick status
    if docker ps | grep -q "fastapi_postgres"; then
        echo "  ✅ PostgreSQL: Running"
    else
        echo "  ❌ PostgreSQL: Stopped"
    fi

    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "  ✅ FastAPI: Running"
    else
        echo "  ❌ FastAPI: Stopped"
    fi

    show_menu

    case $choice in
        1)
            start_postgres
            ;;
        2)
            start_fastapi
            ;;
        3)
            start_both
            ;;
        4)
            cleanup_all
            ;;
        5)
            check_status
            ;;
        6)
            open_db_shell
            ;;
        7)
            view_logs
            ;;
        8)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            sleep 2
            ;;
    esac
done
