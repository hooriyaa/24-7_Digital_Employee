"""
SLA Monitoring Service (Task 4.2).

Monitors tickets for SLA violations and sends alerts:
- High priority tickets: Alert if no response in 5 minutes
- Urgent priority tickets: Alert if no response in 2 minutes
- Normal priority tickets: Alert if no response in 30 minutes

Sends WhatsApp alerts to manager when SLA is at risk.
"""
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional
import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.ticket import Ticket
from app.models.customer import Customer
from app.config import get_settings
from app.services.channels.whatsapp import ultramsg_service


class SLAMonitoringService:
    """
    SLA Monitoring Service.

    Tracks ticket response times and sends alerts when SLA thresholds are breached.

    SLA Thresholds:
    - Urgent: 2 minutes
    - High: 5 minutes
    - Normal: 30 minutes
    - Low: 60 minutes
    """

    # SLA thresholds in minutes
    SLA_THRESHOLDS = {
        "urgent": 2,
        "high": 5,
        "normal": 30,
        "low": 60,
    }

    # Alert thresholds (percentage of SLA time elapsed)
    WARNING_THRESHOLD = 0.5  # 50% of SLA time
    CRITICAL_THRESHOLD = 0.8  # 80% of SLA time

    def __init__(self):
        """Initialize SLA monitoring service."""
        self.settings = get_settings()
        self._manager_phone: Optional[str] = None

    def set_manager_phone(self, phone: str):
        """
        Set manager phone number for alerts.

        Args:
            phone: Manager's WhatsApp phone number
        """
        self._manager_phone = phone

    def get_sla_threshold(self, priority: str) -> int:
        """
        Get SLA threshold in minutes for priority level.

        Args:
            priority: Ticket priority (urgent, high, normal, low)

        Returns:
            SLA threshold in minutes
        """
        return self.SLA_THRESHOLDS.get(priority.lower(), 30)

    async def check_ticket_sla(
        self,
        session: AsyncSession,
        ticket_id: uuid.UUID,
    ) -> dict:
        """
        Check SLA status for a specific ticket.

        Args:
            session: Async database session
            ticket_id: Ticket ID to check

        Returns:
            dict with SLA status and time remaining
        """
        ticket = await session.get(Ticket, ticket_id)

        if not ticket:
            return {"error": "Ticket not found"}

        # Get ticket age in minutes
        now = datetime.now(timezone.utc)
        ticket_age = (now - ticket.created_at.replace(tzinfo=timezone.utc)).total_seconds() / 60

        # Get SLA threshold
        sla_threshold = self.get_sla_threshold(ticket.priority)

        # Calculate remaining time
        time_remaining = sla_threshold - ticket_age
        percentage_elapsed = (ticket_age / sla_threshold) * 100

        # Determine status
        if time_remaining <= 0:
            status = "breached"
        elif percentage_elapsed >= self.CRITICAL_THRESHOLD * 100:
            status = "critical"
        elif percentage_elapsed >= self.WARNING_THRESHOLD * 100:
            status = "warning"
        else:
            status = "ok"

        return {
            "ticket_id": str(ticket_id),
            "priority": ticket.priority,
            "status": ticket.status,
            "sla_threshold_minutes": sla_threshold,
            "ticket_age_minutes": round(ticket_age, 2),
            "time_remaining_minutes": round(time_remaining, 2),
            "percentage_elapsed": round(percentage_elapsed, 2),
            "sla_status": status,
        }

    async def check_all_tickets_sla(
        self,
        session: AsyncSession,
    ) -> list[dict]:
        """
        Check SLA status for all open tickets.

        Args:
            session: Async database session

        Returns:
            List of SLA status dicts for tickets at risk
        """
        # Get all open/in_progress tickets
        query = select(Ticket).where(
            Ticket.status.in_(["open", "in_progress"])
        )
        result = await session.exec(query)
        tickets = result.all()

        sla_results = []
        for ticket in tickets:
            status = await self.check_ticket_sla(session, ticket.id)
            if status.get("sla_status") in ["breached", "critical", "warning"]:
                sla_results.append(status)

        return sla_results

    async def send_sla_alert(
        self,
        session: AsyncSession,
        ticket_id: uuid.UUID,
        alert_type: str = "critical",
    ) -> dict:
        """
        Send SLA alert to manager via WhatsApp.

        Args:
            session: Async database session
            ticket_id: Ticket ID that triggered alert
            alert_type: Type of alert (warning, critical, breached)

        Returns:
            dict with alert result
        """
        if not self._manager_phone:
            return {
                "success": False,
                "error": "Manager phone number not configured",
            }

        # Get ticket details
        ticket = await session.get(Ticket, ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}

        # Get customer details
        customer = await session.get(Customer, ticket.customer_id)
        customer_email = customer.email if customer else "Unknown"

        # Calculate SLA details
        now = datetime.now(timezone.utc)
        ticket_age = (now - ticket.created_at.replace(tzinfo=timezone.utc)).total_seconds() / 60
        sla_threshold = self.get_sla_threshold(ticket.priority)
        time_remaining = sla_threshold - ticket_age

        # Build alert message
        if alert_type == "breached":
            emoji = "🚨"
            urgency = "SLA BREACHED"
        elif alert_type == "critical":
            emoji = "⚠️"
            urgency = "CRITICAL - SLA At Risk"
        else:
            emoji = "⏰"
            urgency = "WARNING - SLA Approaching"

        alert_message = f"""{emoji} *{urgency}*

*Ticket ID:* {str(ticket_id)[:8]}
*Priority:* {ticket.priority.upper()}
*Subject:* {ticket.subject or 'No Subject'}
*Customer:* {customer_email}
*Status:* {ticket.status}

*Time Elapsed:* {round(ticket_age, 1)} minutes
*SLA Threshold:* {sla_threshold} minutes
*Time Remaining:* {round(max(0, time_remaining), 1)} minutes

⚡ Immediate action required!"""

        try:
            # Send WhatsApp alert
            result = await ultramsg_service.send_message(
                phone=self._manager_phone,
                message=alert_message,
            )

            if result.get("success"):
                return {
                    "success": True,
                    "message_id": result.get("message_id"),
                    "alert_type": alert_type,
                    "ticket_id": str(ticket_id),
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error"),
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    async def run_sla_monitor(
        self,
        session: AsyncSession,
    ) -> dict:
        """
        Run SLA monitoring check for all tickets.

        Args:
            session: Async database session

        Returns:
            dict with monitoring results
        """
        # Get all at-risk tickets
        at_risk_tickets = await self.check_all_tickets_sla(session)

        alerts_sent = 0
        alerts_failed = 0

        for ticket_status in at_risk_tickets:
            ticket_id = uuid.UUID(ticket_status["ticket_id"])
            sla_status = ticket_status["sla_status"]

            # Send alert for critical and breached tickets
            if sla_status in ["breached", "critical"]:
                result = await self.send_sla_alert(
                    session,
                    ticket_id,
                    alert_type=sla_status,
                )
                if result.get("success"):
                    alerts_sent += 1
                else:
                    alerts_failed += 1

        return {
            "tickets_checked": len(at_risk_tickets),
            "alerts_sent": alerts_sent,
            "alerts_failed": alerts_failed,
            "at_risk_tickets": at_risk_tickets,
        }


# Singleton instance
sla_monitoring_service = SLAMonitoringService()
