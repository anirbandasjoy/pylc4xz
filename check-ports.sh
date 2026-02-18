#!/bin/bash

# Port conflict checker for FastAPI project

echo "Checking for port conflicts..."
echo ""

# Check port 5432 (PostgreSQL)
if lsof -Pi :5432 -sTCP:LISTEN -t >/dev/null 2>&1 || ss -tlnp 2>/dev/null | grep -q ":5432 "; then
    echo "❌ Port 5432 is already in use!"
    echo ""
    echo "What's using port 5432:"
    lsof -i :5432 2>/dev/null || ss -tlnp | grep 5432
    echo ""
    echo "To fix this, you have two options:"
    echo ""
    echo "Option 1: Stop your local PostgreSQL"
    echo "  sudo service postgresql stop"
    echo "  # OR"
    echo "  sudo systemctl stop postgresql"
    echo ""
    echo "Option 2: Change Docker to use a different port"
    echo "  Edit docker-compose.yml and change '5432:5432' to '5433:5432'"
    echo "  Then update .env DATABASE_URL to use port 5433"
    echo ""
    exit 1
else
    echo "✅ Port 5432 is available"
fi

# Check port 5050 (pgAdmin)
if lsof -Pi :5050 -sTCP:LISTEN -t >/dev/null 2>&1 || ss -tlnp 2>/dev/null | grep -q ":5050 "; then
    echo "⚠️  Port 5050 is already in use (pgAdmin)"
    echo "   Edit docker-compose.yml to change pgAdmin port if needed"
else
    echo "✅ Port 5050 is available"
fi

echo ""
echo "All checks passed! You can now run:"
echo "  ./start.sh"
echo "  or"
echo "  docker-compose up -d"
