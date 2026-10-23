from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, ClassVar


class DomainEventAttributes(TypedDict): ...


class DomainEventPrimitives(TypedDict):
    id: str
    occurred_at: datetime
    name: str
    attributes: DomainEventAttributes


@dataclass(frozen=True, kw_only=True)
class DomainEvent(ABC):
    name: ClassVar[str]

    id: str
    occurred_at: datetime
    attributes: DomainEventAttributes

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not isinstance(getattr(cls, "name", None), str):
            raise TypeError(f"{cls.__name__} must define a class attribute 'name'")

    def to_primitives(self) -> DomainEventPrimitives:
        return DomainEventPrimitives(
            id=self.id,
            occurred_at=self.occurred_at,
            name=self.name,
            attributes=self.attributes,
        )
