"""
Automation Services.

Provides automated workflows for customer support:
- Auto-responder for common queries (Task 4.1)
- SLA monitoring with alerts (Task 4.2)
"""
from app.services.automation.auto_responder import auto_responder_service, AutoResponderService
from app.services.automation.sla_monitoring import sla_monitoring_service, SLAMonitoringService

__all__ = [
    "auto_responder_service",
    "AutoResponderService",
    "sla_monitoring_service",
    "SLAMonitoringService",
]
