from dataclasses import dataclass
from typing import TypedDict

from src.shared.domain.event_bus.domain_event import DomainEvent


class DummyDomainEventAttributes(TypedDict):
    id: str
    name: str


@dataclass(frozen=True)
class DummyDomainEvent(DomainEvent):
    attributes: DummyDomainEventAttributes

    @property
    def type(self) -> str:
        return "dummy_event"
