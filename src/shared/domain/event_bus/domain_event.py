from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import TypedDict

from src.shared.domain.uuid_generator import UuidGenerator


class DomainEventPrimitives(TypedDict):
    id: str
    occurred_at: str
    type: str
    attributes: TypedDict


@dataclass(frozen=True, kw_only=True)
class DomainEvent(ABC):
    id: str = field(default_factory=lambda: UuidGenerator.random())
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    attributes: TypedDict

    @property
    @abstractmethod
    def type(self) -> str:
        raise NotImplementedError

    def to_primitives(self) -> DomainEventPrimitives:
        return DomainEventPrimitives(
            id=self.id,
            occurred_at=self.occurred_at.isoformat(),
            type=self.type,
            attributes=self.attributes,
        )
