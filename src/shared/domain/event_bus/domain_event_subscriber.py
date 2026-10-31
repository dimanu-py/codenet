from abc import ABC, abstractmethod
from typing import ClassVar

from src.shared.domain.event_bus.domain_event import DomainEvent


class DomainEventSubscriber[T: DomainEvent](ABC):
    name: ClassVar[str]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not isinstance(getattr(cls, "name", None), str):
            raise TypeError(f"{cls.__name__} must define a class attribute 'name'")

    @abstractmethod
    async def on(self, event: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribed_to(self) -> type[T]:
        raise NotImplementedError
