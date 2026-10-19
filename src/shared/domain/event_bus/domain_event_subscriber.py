from abc import ABC, abstractmethod

from shared.domain.event_bus.domain_event import DomainEvent


class DomainEventSubscriber[T: DomainEvent](ABC):
    @abstractmethod
    async def on(self, event: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribed_to(self) -> type[T]:
        raise NotImplementedError
