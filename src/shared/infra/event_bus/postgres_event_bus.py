from collections import defaultdict
from typing import override

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.domain_event_subscriber import DomainEventSubscriber
from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.domain_event_dead_letter_model import DomainEventDeadLetterModel
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel


class _SubscriptionMapper:
    def __init__(self, subscribers: list[DomainEventSubscriber]) -> None:
        self._event_class_by_name: dict[str, type[DomainEvent]] = {}
        self._subscribers_by_event_name: defaultdict[str, list[DomainEventSubscriber]] = defaultdict(list)
        for subscriber in subscribers:
            event_class = subscriber.subscribed_to()
            self._event_class_by_name[event_class.name] = event_class
            self._subscribers_by_event_name[event_class.name].append(subscriber)

    def event_class_for(self, event_name: str) -> type[DomainEvent] | None:
        return self._event_class_by_name.get(event_name)

    def subscribers_for_publishing(self, event_name: str) -> list[DomainEventSubscriber]:
        return self._subscribers_by_event_name.get(event_name, [])

    def subscribers_for_consuming(self, event_name: str, subscriber_name: str) -> list[DomainEventSubscriber]:
        subscribers_for_event = self._subscribers_by_event_name.get(event_name, [])
        return [subscriber for subscriber in subscribers_for_event if subscriber.name == subscriber_name]


class PostgresEventBus(EventBus):
    _MAX_ATTEMPTS_TO_CONSUME: int = 3

    def __init__(self, session: AsyncSession, subscribers: list[DomainEventSubscriber]) -> None:
        self._session = session
        self._subscription_mapper = _SubscriptionMapper(subscribers)

    @override
    async def publish(self, events: list[DomainEvent]) -> None:
        if not events:
            return
        await self._store_events_to_publish(events)

    async def consume(self, subscribers: list[str], amount: int) -> None:
        events_to_consume = await self._get_events_to_consume(subscribers=subscribers, amount=amount)
        for event in events_to_consume:
            await self._execute_subscribers_for(event)

    async def _store_events_to_publish(self, events: list[DomainEvent]) -> None:
        events_to_publish = []
        for event in events:
            subscribers = self._subscription_mapper.subscribers_for_publishing(event.name)
            for subscriber in subscribers:
                events_to_publish.append(DomainEventToConsumeModel.from_domain(event, subscriber.name))
        await self._store_events(events_to_publish)

    async def _store_events(self, events: list[DomainEventToConsumeModel | DomainEventDeadLetterModel]) -> None:
        self._session.add_all(events)
        await self._session.flush()

    async def _get_events_to_consume(self, subscribers: list[str], amount: int) -> list[DomainEventToConsumeModel]:
        for_subscribers = [DomainEventToConsumeModel.subscriber_name.in_(subscribers)] if subscribers else []
        query = await self._session.execute(
            select(DomainEventToConsumeModel)
            .where(*for_subscribers)
            .order_by(DomainEventToConsumeModel.inserted_at.asc())
            .limit(amount)
            .with_for_update(skip_locked=True)
        )
        return query.scalars().all()

    async def _execute_subscribers_for(self, db_event: DomainEventToConsumeModel) -> None:
        event_class = self._subscription_mapper.event_class_for(db_event.name)
        subscribers_to_event = self._subscription_mapper.subscribers_for_consuming(
            db_event.name, db_event.subscriber_name
        )
        if not event_class or not subscribers_to_event:
            return
        event = event_class(id=db_event.id, occurred_at=db_event.occurred_at, attributes=db_event.attributes)
        try:
            for subscriber in subscribers_to_event:
                await subscriber.on(event)
            await self._delete_consumed_event(db_event)
        except Exception:
            if db_event.has_reached_max_attempts(self._MAX_ATTEMPTS_TO_CONSUME):
                await self._send_event_to_dead_letter(db_event)
            else:
                await self._increase_attempts(db_event)

    async def _delete_consumed_event(self, event: DomainEventToConsumeModel) -> None:
        query = delete(DomainEventToConsumeModel).where(
            DomainEventToConsumeModel.id == event.id,
            DomainEventToConsumeModel.subscriber_name == event.subscriber_name,
        )
        await self._session.execute(query)
        await self._session.flush()

    async def _increase_attempts(self, event: DomainEventToConsumeModel) -> None:
        query = (
            update(DomainEventToConsumeModel)
            .where(
                DomainEventToConsumeModel.id == event.id,
                DomainEventToConsumeModel.subscriber_name == event.subscriber_name,
            )
            .values(attempts=DomainEventToConsumeModel.attempts + 1)
        )
        await self._session.execute(query)
        await self._session.flush()

    async def _send_event_to_dead_letter(self, event: DomainEventToConsumeModel) -> None:
        await self._store_events([DomainEventDeadLetterModel.from_published_event(event)])
        await self._delete_consumed_event(event)
