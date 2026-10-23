from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.event_bus.domain_event_subscriber import DomainEventSubscriber
from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel


class PostgresEventBus(EventBus):
    def __init__(self, session: AsyncSession, subscribers: list[DomainEventSubscriber]) -> None:
        self._session = session
        self._subscribers = subscribers

    @override
    async def publish(self, events: list[DomainEvent]) -> None:
        if not events:
            return
        await self._store_events(events)

    async def consume(self, amount: int) -> None:
        events_to_consume = await self._get_events_to_consume(amount=amount)
        if not events_to_consume:
            return
        raise NotImplementedError

    async def _store_events(self, events: list[DomainEvent]) -> None:
        events_to_publish = [DomainEventToConsumeModel.from_domain(event) for event in events]
        self._session.add_all(events_to_publish)
        await self._session.flush()

    async def _get_events_to_consume(self, amount: int) -> list:
        query = await self._session.execute(
            select(DomainEventToConsumeModel)
            .order_by(DomainEventToConsumeModel.inserted_at.asc())
            .limit(amount)
            .with_for_update(skip_locked=True)
        )
        events_to_consume = query.scalars().all()
        return events_to_consume
