from typing import override, NamedTuple

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event_subscriber import DomainEventSubscriber
from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel


class _SubscriptionEntry(NamedTuple):
    event_class: type[DomainEvent]
    subscribers: list[DomainEventSubscriber]


class PostgresEventBus(EventBus):
    def __init__(self, session: AsyncSession, subscribers: list[DomainEventSubscriber]) -> None:
        self._session = session
        self._entries_by_event_name: dict[str, _SubscriptionEntry] = {}
        for subscriber in subscribers:
            event_class = subscriber.subscribed_to()
            entry = self._entries_by_event_name.setdefault(event_class.name, _SubscriptionEntry(event_class, []))
            entry.subscribers.append(subscriber)

    @override
    async def publish(self, events: list[DomainEvent]) -> None:
        if not events:
            return
        await self._store_events_to_publish(events)

    async def consume(self, amount: int) -> None:
        events_to_consume = await self._get_events_to_consume(amount=amount)
        for event in events_to_consume:
            await self._execute_subscribers_for(event)

    async def _store_events_to_publish(self, events: list[DomainEvent]) -> None:
        events_to_publish = [DomainEventToConsumeModel.from_domain(event) for event in events]
        await self._store_events(events_to_publish)

    async def _store_events(self, events_to_publish: list[DomainEventToConsumeModel]) -> None:
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

    async def _execute_subscribers_for(self, db_event: DomainEventToConsumeModel) -> None:
        entry = self._entries_by_event_name.get(db_event.name)
        if not entry:
            return
        event = entry.event_class(id=db_event.id, occurred_at=db_event.occurred_at, attributes=db_event.attributes)
        try:
            for subscriber in entry.subscribers:
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
