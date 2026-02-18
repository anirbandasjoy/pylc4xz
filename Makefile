.PHONY: help start stop restart logs install db-shell db-clean test clean dev dev-all cleanup

# Default target
help:
	@echo "FastAPI Authentication System - Available Commands:"
	@echo ""
	@echo "  🚀 Start Commands:"
	@echo "    make start       - Start PostgreSQL with Docker Compose (background)"
	@echo "    make start-fg    - Start PostgreSQL in foreground (interactive)"
	@echo "    make run         - Run FastAPI application"
	@echo "    make dev         - Start PostgreSQL (bg) + FastAPI"
	@echo "    make dev-all     - Interactive menu for everything"
	@echo ""
	@echo "  🛑 Stop Commands:"
	@echo "    make stop        - Stop Docker containers"
	@echo "    make cleanup     - Stop and remove all containers"
	@echo ""
	@echo "  📊 Management:"
	@echo "    make logs        - Show PostgreSQL logs"
	@echo "    make db-shell    - Open PostgreSQL shell"
	@echo "    make status      - Show all container status"
	@echo ""
	@echo "  🔧 Maintenance:"
	@echo "    make install     - Install Python dependencies"
	@echo "    make db-clean    - Remove Docker volumes (DELETES ALL DATA)"
	@echo "    make clean       - Clean Python cache"
	@echo ""

# Start PostgreSQL (background)
start:
	@echo "🐚 Starting PostgreSQL in background..."
	docker-compose up -d
	@echo "✅ PostgreSQL started"
	@echo "📊 Check logs: make logs"

# Start PostgreSQL (foreground/interactive)
start-fg:
	@echo "🐚 Starting PostgreSQL in foreground (Press Ctrl+C to stop)..."
	docker-compose up

# Stop containers
stop:
	@echo "Stopping containers..."
	docker-compose down
	@echo "✅ Containers stopped"

# Restart containers
restart: stop start

# Show logs
logs:
	docker-compose logs -f postgres

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Open PostgreSQL shell
db-shell:
	docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db

# Clean database (WARNING: deletes all data)
db-clean:
	@echo "⚠️  This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "✅ Database cleaned"; \
	else \
		echo "Cancelled"; \
	fi

# Run FastAPI application
run:
	@echo "Starting FastAPI application..."
	uvicorn main:app --reload

# Run tests
test:
	@echo "Running tests..."
	pytest

# Clean Python cache
clean:
	@echo "Cleaning Python cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Clean completed"

# Development mode - Start PostgreSQL in background
dev:
	@echo "🚀 Starting development environment..."
	@make install
	@make start
	@echo ""
	@echo "✅ PostgreSQL started in background"
	@echo "🐍 Now run FastAPI in another terminal:"
	@echo "   source venv/bin/activate"
	@echo "   uvicorn main:app --reload"
	@echo ""
	@echo "📚 API: http://localhost:8000/docs"
	@echo ""

# Interactive menu
dev-all:
	@echo "🚀 Launching interactive menu..."
	./run-project.sh

# Show status
status:
	@echo "📊 Container Status:"
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "No containers running"
	@echo ""
	@if docker ps | grep -q "fastapi_postgres"; then \
		echo "✅ PostgreSQL: Running"; \
	else \
		echo "❌ PostgreSQL: Stopped"; \
	fi
	@if curl -s http://localhost:8000/health > /dev/null 2>&1; then \
		echo "✅ FastAPI: Running"; \
	else \
		echo "❌ FastAPI: Stopped"; \
	fi

# Cleanup all containers
cleanup:
	@echo "🧹 Cleaning up all containers..."
	@docker stop $(docker ps -aq) 2>/dev/null || echo "No running containers"
	@docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"
	@echo "✅ Cleanup complete"
