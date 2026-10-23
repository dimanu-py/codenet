from dataclasses import dataclass

from src.shared.domain.event_bus.domain_event import DomainEvent, DomainEventAttributes


class DummyDomainEventAttributes(DomainEventAttributes):
    id: str
    name: str


@dataclass(frozen=True)
class DummyDomainEvent(DomainEvent):
    name = "dummy_event"
    attributes: DummyDomainEventAttributes
