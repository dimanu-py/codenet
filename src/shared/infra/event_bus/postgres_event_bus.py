from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus


class PostgresEventBus(EventBus):
    async def publish(self, events: list[DomainEvent]) -> None:
        raise NotImplementedError
