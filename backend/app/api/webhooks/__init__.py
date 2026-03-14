"""
Webhooks Router - Aggregates all webhook handlers.
"""
from fastapi import APIRouter
from app.api.webhooks.whatsapp import router as whatsapp_router
from app.api.webhooks.gmail import router as gmail_router

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

# Include sub-routers
router.include_router(whatsapp_router, prefix="/whatsapp")
router.include_router(gmail_router, prefix="/gmail")
