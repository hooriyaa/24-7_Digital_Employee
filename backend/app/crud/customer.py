"""
Customer CRUD operations.
"""
import uuid
from typing import Any

from pydantic import BaseModel, Field, EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.customer import Customer


class CustomerCreate(BaseModel):
    """Customer creation schema."""
    email: str = Field(..., description="Customer email")
    name: str = Field(..., description="Customer name")
    phone: str | None = Field(default=None, description="Customer phone")


class CustomerUpdate(BaseModel):
    """Customer update schema."""
    email: str | None = Field(default=None, description="Customer email")
    name: str | None = Field(default=None, description="Customer name")
    phone: str | None = Field(default=None, description="Customer phone")
    custom_metadata: dict | None = Field(default=None, description="Customer metadata")


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    """
    Customer CRUD operations.

    Extends base CRUD with customer-specific methods.
    """

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> Customer | None:
        """
        Get customer by email address.

        Args:
            session: Async database session
            email: Customer email

        Returns:
            Customer or None if not found
        """
        return await self.get_by_field(session, field_name="email", value=email)

    async def get_by_phone(
        self,
        session: AsyncSession,
        phone: str
    ) -> Customer | None:
        """
        Get customer by phone number.

        Args:
            session: Async database session
            phone: Customer phone number

        Returns:
            Customer or None if not found
        """
        return await self.get_by_field(session, field_name="phone", value=phone)

    async def get_or_create(
        self,
        session: AsyncSession,
        *,
        email: str,
        name: str,
        phone: str | None = None
    ) -> Customer:
        """
        Get existing customer by email or create new one.

        Args:
            session: Async database session
            email: Customer email
            name: Customer name
            phone: Optional phone number

        Returns:
            Existing or newly created customer
        """
        # Try to get by email first
        customer = await self.get_by_email(session, email)
        if customer:
            return customer
        
        # Try to get by phone if provided
        if phone:
            customer = await self.get_by_phone(session, phone)
            if customer:
                return customer
        
        # Create new customer
        customer_data = CustomerCreate(email=email, name=name, phone=phone)
        return await self.create(session, obj_in=customer_data)


# Singleton instance
customer_crud = CRUDCustomer(Customer)
