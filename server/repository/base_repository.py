from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Type, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from server.model.base_model import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC, Generic[T]):
    """Base repository class providing common CRUD operations."""

    def __init__(self, db_session: Session, model_class: Type[T]):
        self.db_session = db_session
        self.model_class = model_class

    def create(self, entity: T) -> T:
        """Create a new entity in the database."""
        try:
            self.db_session.add(entity)
            self.db_session.commit()
            self.db_session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error creating {self.model_class.__name__}: {str(e)}")

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        try:
            return self.db_session.get(self.model_class, entity_id)
        except SQLAlchemyError as e:
            raise RuntimeError(
                f"Error retrieving {self.model_class.__name__} by ID {entity_id}: {str(e)}"
            )

    def get_all(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[T]:
        """Retrieve all entities with optional pagination."""
        try:
            query = select(self.model_class)
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            result = self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RuntimeError(
                f"Error retrieving all {self.model_class.__name__}: {str(e)}"
            )

    def update(self, entity_id: int, update_data: Dict[str, Any]) -> Optional[T]:
        """Update an entity by ID with the provided data."""
        try:
            # First check if entity exists
            entity = self.get_by_id(entity_id)
            if not entity:
                return None

            # Update the entity
            stmt = (
                update(self.model_class)
                .where(self.model_class.id == entity_id)
                .values(update_data)
            )
            self.db_session.execute(stmt)
            self.db_session.commit()

            # Return updated entity
            return self.get_by_id(entity_id)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(
                f"Error updating {self.model_class.__name__} with ID {entity_id}: {str(e)}"
            )

    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""
        try:
            # First check if entity exists
            entity = self.get_by_id(entity_id)
            if not entity:
                return False

            # Delete the entity
            stmt = delete(self.model_class).where(self.model_class.id == entity_id)
            self.db_session.execute(stmt)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(
                f"Error deleting {self.model_class.__name__} with ID {entity_id}: {str(e)}"
            )

    def count(self) -> int:
        """Count total number of entities."""
        try:
            result = self.db_session.execute(select(self.model_class))
            return len(result.scalars().all())
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error counting {self.model_class.__name__}: {str(e)}")

    def exists(self, entity_id: int) -> bool:
        """Check if an entity exists by ID."""
        return self.get_by_id(entity_id) is not None
