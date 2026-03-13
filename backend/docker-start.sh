#!/bin/bash
# ===========================================
# Customer Success Digital FTE - Docker Quick Start
# ===========================================
# Usage:
#   ./docker-start.sh              # Start infrastructure (PostgreSQL + Kafka)
#   ./docker-start.sh backend      # Start infrastructure + backend
#   ./docker-stop.sh               # Stop all services
# ===========================================

set -e

echo "=========================================="
echo "Customer Success Digital FTE"
echo "Docker Infrastructure Startup"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Start infrastructure services
echo ""
echo "Starting PostgreSQL and Kafka..."
docker-compose up -d postgres kafka kafka-init

# Wait for services to be healthy
echo ""
echo "Waiting for services to be ready..."
sleep 15

# Check service status
echo ""
echo "Service Status:"
docker-compose ps

# Show connection info
echo ""
echo "=========================================="
echo "Connection Information"
echo "=========================================="
echo "PostgreSQL (local): localhost:5432"
echo "  - Database: cs_fte"
echo "  - User: postgres"
echo "  - Password: postgres (from .env)"
echo ""
echo "Kafka: localhost:9092"
echo "  - Topics: tickets.create, tickets.update, messages.send, escalations.trigger"
echo ""
echo "=========================================="

# Start backend if requested
if [ "$1" = "backend" ]; then
    echo ""
    echo "Building and starting backend..."
    docker-compose up -d backend
    echo ""
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
fi

echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: ./docker-stop.sh"
echo "=========================================="
