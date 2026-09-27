from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict


class DomainEventPrimitives(TypedDict):
    id: str
    occurred_at: datetime
    name: str
    attributes: dict


@dataclass(frozen=True, kw_only=True)
class DomainEvent(ABC):
    id: str
    occurred_at: datetime
    attributes: dict

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def to_primitives(self) -> DomainEventPrimitives:
        return DomainEventPrimitives(
            id=self.id,
            occurred_at=self.occurred_at,
            name=self.name,
            attributes=self.attributes,
        )
