#!/bin/bash

echo "======================================="
echo "  🧹 Cleaning Up Docker Containers"
echo "======================================="
echo ""

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "No running containers found"

# Remove all containers
echo ""
echo "Removing all containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

# Clean up project volumes (WARNING: deletes database data)
read -p "❓ Do you want to delete all data volumes? This will delete your database! [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing volumes..."
    docker volume rm $(docker volume ls -q) 2>/dev/null || echo "No volumes to remove"
    echo "✅ All data deleted"
else
    echo "⏭️  Skipping volume removal"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "🚀 Start fresh with: docker-compose up"
