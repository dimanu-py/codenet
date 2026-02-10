from abc import ABC, abstractmethod

from src.shared.domain.event_bus.domain_event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None:
        raise NotImplementedError
