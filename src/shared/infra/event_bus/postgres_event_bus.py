from collections import defaultdict
from typing import override

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event_subscriber import DomainEventSubscriber
from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel


class PostgresEventBus(EventBus):
    def __init__(self, session: AsyncSession, subscribers: list[DomainEventSubscriber]) -> None:
        self._session = session
        self._subscribers_by_event: defaultdict[type[DomainEvent], list[DomainEventSubscriber]] = defaultdict(list)
        for subscriber in subscribers:
            self._subscribers_by_event[subscriber.subscribed_to()].append(subscriber)
        self._event_class_by_name = {event_class.name: event_class for event_class in self._subscribers_by_event}

    @override
    async def publish(self, events: list[DomainEvent]) -> None:
        if not events:
            return
        await self._store_events(events)

    async def consume(self, amount: int) -> None:
        events_to_consume = await self._get_events_to_consume(amount=amount)
        for event in events_to_consume:
            await self._execute_subscribers_for(event)

    async def _store_events(self, events: list[DomainEvent]) -> None:
        events_to_publish = [DomainEventToConsumeModel.from_domain(event) for event in events]
        self._session.add_all(events_to_publish)
        await self._session.flush()

    async def _get_events_to_consume(self, amount: int) -> list[DomainEventToConsumeModel]:
        query = await self._session.execute(
            select(DomainEventToConsumeModel)
            .order_by(DomainEventToConsumeModel.inserted_at.asc())
            .limit(amount)
            .with_for_update(skip_locked=True)
        )
        return query.scalars().all()

    def _get_event_class_from_name(self, event_to_consume: DomainEventToConsumeModel) -> DomainEvent | None:
        event_class = self._event_class_by_name.get(event_to_consume.name)
        if not event_class:
            return None
        return event_class(
            id=event_to_consume.id, occurred_at=event_to_consume.occurred_at, attributes=event_to_consume.attributes
        )

    async def _execute_subscribers_for(self, db_event: DomainEventToConsumeModel) -> None:
        event = self._get_event_class_from_name(db_event)
        if not event:
            return
        subscribed_to_event = self._subscribers_by_event[type(event)]
        try:
            for subscriber in subscribed_to_event:
                await subscriber.on(event)
            await self._delete_consumed_event(db_event)
        except Exception:
            await self._increase_attempts(db_event)

    async def _delete_consumed_event(self, event: DomainEventToConsumeModel) -> None:
        query = delete(DomainEventToConsumeModel).where(DomainEventToConsumeModel.id == event.id)
        await self._session.execute(query)
        await self._session.flush()

    async def _increase_attempts(self, event: DomainEventToConsumeModel) -> None:
        query = (
            update(DomainEventToConsumeModel)
            .where(
                DomainEventToConsumeModel.id == event.id,
            )
            .values(attempts=DomainEventToConsumeModel.attempts + 1)
        )
        await self._session.execute(query)
        await self._session.flush()
