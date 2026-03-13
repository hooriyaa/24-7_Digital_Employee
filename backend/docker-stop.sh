#!/bin/bash
# ===========================================
# Customer Success Digital FTE - Docker Stop
# ===========================================

set -e

echo "Stopping all Docker services..."
docker-compose down

echo ""
echo "Services stopped. Data is preserved in volumes."
echo "To remove volumes: docker-compose down -v"
