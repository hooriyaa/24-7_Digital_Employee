"""
Base CRUD operations with async support.

Generic CRUD class for SQLModel entities with async session handling.
"""
from typing import Any, Generic, Type, TypeVar, Union

from pydantic import BaseModel
from sqlmodel import SQLModel, select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func

# Type variables for generic CRUD operations
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD base class for SQLModel entities.
    
    Provides async CRUD operations that can be inherited by specific
    entity CRUD classes.
    
    Type Parameters:
        ModelType: SQLModel class for database operations
        CreateSchemaType: Pydantic schema for creation
        UpdateSchemaType: Pydantic schema for updates
    
    Example:
        class CustomerCRUD(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
            pass
        
        customer_crud = CustomerCRUD(Customer)
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD with model class.
        
        Args:
            model: SQLModel class for database operations
        """
        self.model = model
    
    async def get(
        self,
        session: AsyncSession,
        id: Any
    ) -> ModelType | None:
        """
        Get a single entity by ID.
        
        Args:
            session: Async database session
            id: Entity ID
            
        Returns:
            Entity or None if not found
        """
        result = await session.get(self.model, id)
        return result
    
    async def get_by_field(
        self,
        session: AsyncSession,
        field_name: str,
        value: Any
    ) -> ModelType | None:
        """
        Get a single entity by a specific field.
        
        Args:
            session: Async database session
            field_name: Name of the field to filter by
            value: Value to match
            
        Returns:
            Entity or None if not found
        """
        field = getattr(self.model, field_name)
        statement = select(self.model).where(field == value)
        result = await session.exec(statement)
        return result.first()
    
    async def get_multi(
        self,
        session: AsyncSession,
        *,
        offset: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None
    ) -> list[ModelType]:
        """
        Get multiple entities with pagination and optional filters.
        
        Args:
            session: Async database session
            offset: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional dictionary of field=value filters
            
        Returns:
            List of entities
        """
        statement = select(self.model)
        
        # Apply filters if provided
        if filters:
            conditions = []
            for field_name, value in filters.items():
                field = getattr(self.model, field_name)
                conditions.append(field == value)
            statement = statement.where(and_(*conditions))
        
        # Apply pagination
        statement = statement.offset(offset).limit(limit)
        
        result = await session.exec(statement)
        return result.all()
    
    async def count(
        self,
        session: AsyncSession,
        filters: dict[str, Any] | None = None
    ) -> int:
        """
        Count entities with optional filters.
        
        Args:
            session: Async database session
            filters: Optional dictionary of field=value filters
            
        Returns:
            Total count of entities
        """
        statement = select(func.count()).select_from(self.model)
        
        if filters:
            conditions = []
            for field_name, value in filters.items():
                field = getattr(self.model, field_name)
                conditions.append(field == value)
            statement = statement.where(and_(*conditions))
        
        result = await session.exec(statement)
        return result.one()
    
    async def create(
        self,
        session: AsyncSession,
        *,
        obj_in: CreateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        Create a new entity.
        
        Args:
            session: Async database session
            obj_in: Pydantic schema or dict with creation data
            
        Returns:
            Created entity
        """
        # Convert dict to model if needed
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = self.model.model_validate(obj_in)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        Update an existing entity.
        
        Args:
            session: Async database session
            db_obj: Existing entity to update
            obj_in: Pydantic schema or dict with update data
            
        Returns:
            Updated entity
        """
        # Convert to dict if Pydantic schema
        if not isinstance(obj_in, dict):
            obj_in = obj_in.model_dump(exclude_unset=True)
        
        # Update fields
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update_by_id(
        self,
        session: AsyncSession,
        *,
        id: Any,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType | None:
        """
        Update an entity by ID.
        
        Args:
            session: Async database session
            id: Entity ID
            obj_in: Pydantic schema or dict with update data
            
        Returns:
            Updated entity or None if not found
        """
        db_obj = await self.get(session, id=id)
        if not db_obj:
            return None
        return await self.update(session, db_obj=db_obj, obj_in=obj_in)
    
    async def remove(
        self,
        session: AsyncSession,
        *,
        id: Any
    ) -> ModelType | None:
        """
        Remove an entity by ID.
        
        Args:
            session: Async database session
            id: Entity ID
            
        Returns:
            Removed entity or None if not found
        """
        db_obj = await self.get(session, id=id)
        if not db_obj:
            return None
        
        await session.delete(db_obj)
        await session.commit()
        return db_obj
    
    async def remove_by_field(
        self,
        session: AsyncSession,
        *,
        field_name: str,
        value: Any
    ) -> ModelType | None:
        """
        Remove an entity by a specific field.
        
        Args:
            session: Async database session
            field_name: Name of the field to filter by
            value: Value to match
            
        Returns:
            Removed entity or None if not found
        """
        db_obj = await self.get_by_field(session, field_name=field_name, value=value)
        if not db_obj:
            return None
        
        await session.delete(db_obj)
        await session.commit()
        return db_obj
