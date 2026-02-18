from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[T], ABC):
    """Base service class with common CRUD operations"""

    def __init__(self) -> None:
        self._db: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    @abstractmethod
    def _to_entity(self, data: Dict[str, Any]) -> T:
        """Convert dict to entity model"""
        pass

    @abstractmethod
    def _to_dict(self, entity: T) -> Dict[str, Any]:
        """Convert entity model to dict"""
        pass

    def get_all(
        self, skip: int = 0, limit: int = 100, **filters: Any
    ) -> tuple[List[Dict[str, Any]], int]:
        """Get all entities with optional filters"""
        items = list(self._db.values())

        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                if value is not None:
                    items = [item for item in items if item.get(key) == value]

        total = len(items)
        items = items[skip : skip + limit]

        return items, total

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Get entity by ID"""
        return self._db.get(entity_id)

    def create(self, entity_data: CreateSchemaType) -> Dict[str, Any]:
        """Create new entity"""
        entity_dict = entity_data.model_dump()
        entity_dict["id"] = self._next_id
        self._next_id += 1

        self._db[entity_dict["id"]] = entity_dict
        return entity_dict

    def update(self, entity_id: int, entity_data: UpdateSchemaType) -> Optional[Dict[str, Any]]:
        """Update entity"""
        if entity_id not in self._db:
            return None

        stored_entity = self._db[entity_id]
        update_data = entity_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            stored_entity[field] = value

        return stored_entity

    def delete(self, entity_id: int) -> bool:
        """Delete entity"""
        if entity_id not in self._db:
            return False

        del self._db[entity_id]
        return True

    def exists(self, entity_id: int) -> bool:
        """Check if entity exists"""
        return entity_id in self._db

    def count(self) -> int:
        """Get total count of entities"""
        return len(self._db)

    def search(
        self,
        query: str,
        fields: List[str],
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Search entities by query in specified fields"""
        query_lower = query.lower()

        items = []
        for item in self._db.values():
            for field in fields:
                field_value = str(item.get(field, ""))
                if query_lower in field_value.lower():
                    items.append(item)
                    break

        total = len(items)
        items = items[skip : skip + limit]

        return items, total
