from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel


class PostgresEventBus(EventBus):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, events: list[DomainEvent]) -> None:
        if not events:
            return
        await self._store_events(events)

    async def _store_events(self, events: list[DomainEvent]) -> None:
        events_to_publish = [DomainEventToConsumeModel.from_domain(event) for event in events]
        self._session.add_all(events_to_publish)
        await self._session.commit()
