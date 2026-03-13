"""
API routes for health checks and monitoring.
"""
import time
from datetime import datetime, timezone

from fastapi import APIRouter, status
from sqlalchemy import text

from app.database import get_engine
from app.schemas.health import HealthResponse, DatabaseHealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Health Check",
    description="Check API and database health status",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring and load balancers.

    Tests:
    - API is running
    - Database connection is active
    - Measures database query latency

    Returns:
        HealthResponse with status, timestamp, version, and database status
    """
    from app.config import get_settings

    settings = get_settings()

    # Default values
    db_status = "disconnected"
    db_latency_ms = None
    overall_status = "degraded"

    # Test database connection
    try:
        engine = get_engine()

        # Measure query latency
        start_time = time.perf_counter()

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        end_time = time.perf_counter()
        db_latency_ms = round((end_time - start_time) * 1000, 2)

        db_status = "connected"
        overall_status = "healthy"

    except Exception as e:
        # Log error but don't expose details
        print(f"Health check database error: {e}")
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        environment=settings.app_env,
        database=db_status,
        database_latency_ms=db_latency_ms,
    )


@router.get(
    "/health/db",
    response_model=DatabaseHealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Database Health Check",
    description="Check database connection status only",
)
async def database_health() -> DatabaseHealthResponse:
    """
    Database health check endpoint.

    Tests database connection and measures query latency.

    Returns:
        DatabaseHealthResponse with connection status and latency
    """
    from app.config import get_settings

    settings = get_settings()

    connected = False
    latency_ms = None

    try:
        engine = get_engine()

        start_time = time.perf_counter()

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        end_time = time.perf_counter()
        latency_ms = round((end_time - start_time) * 1000, 2)
        connected = True

    except Exception as e:
        print(f"Database health check error: {e}")

    return DatabaseHealthResponse(
        connected=connected,
        latency_ms=latency_ms,
        host=settings.postgres_host,
        database=settings.postgres_db,
    )
