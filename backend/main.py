"""
Customer Success Digital FTE - Backend Application

A 24/7 autonomous AI employee for multi-channel customer support.
"""
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db_engine, close_db_engine, get_db_session
from app.api.routes import router as api_router
from app.api.routes_auth import router as auth_router
from app.api.routes_agent import router as agent_router
from app.api.routes_main import router as main_router
from app.api.routes_tickets import router as tickets_router
from app.api.routes_conversations import router as conversations_router
from app.api.webhooks import router as webhooks_router
from app.services.gmail_polling import gmail_polling_service
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    Startup: Initialize database engine, validate configuration
    Shutdown: Clean up resources, close connections
    """
    # Startup: Validate configuration and initialize resources
    print("🚀 Starting Customer Success Digital FTE API...")

    try:
        settings = get_settings()
        print(f"✅ Configuration loaded: {settings.app_name}")
        print(f"✅ Environment: {settings.app_env}")
        print(f"✅ Debug mode: {settings.debug}")
        print(f"✅ Database: {settings.postgres_host}")
        print(f"✅ CORS Origins: {settings.cors_origins}")

        # Initialize database engine
        await init_db_engine()
        print("✅ Database engine initialized")
        
        # Start Gmail polling in background
        if settings.debug:  # Only in development
            print("📧 Starting Gmail polling service...")
            asyncio.create_task(gmail_polling_service.start_polling())
            print("✅ Gmail polling started (checking every 30 seconds)")

    except Exception as e:
        print(f"❌ Startup error: {e}")
        raise

    yield

    # Shutdown: Clean up resources
    print("👋 Shutting down Customer Success Digital FTE API...")
    gmail_polling_service.stop_polling()
    await close_db_engine()


app = FastAPI(
    title="Customer Success Digital FTE",
    description="24/7 autonomous AI employee for multi-channel customer support across Email, WhatsApp, and Web",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
# IMPORTANT: routes_tickets must come BEFORE routes_main to handle POST /tickets first
app.include_router(tickets_router, prefix="/api/v1")  # Tickets routes (POST /tickets)
app.include_router(main_router, prefix="/api/v1")  # Main CRUD routes (GET /tickets)
app.include_router(api_router, prefix="/api/v1")  # Health routes
app.include_router(auth_router, prefix="/api/v1")  # Auth routes
app.include_router(agent_router, prefix="/api/v1")  # Agent routes
app.include_router(conversations_router, prefix="/api/v1")  # Conversations routes
app.include_router(webhooks_router, prefix="/api/v1")  # Webhook routes


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message.

    Returns:
        dict: Welcome message with API info
    """
    settings = get_settings()
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "environment": settings.app_env,
    }
