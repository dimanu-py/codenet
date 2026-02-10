import asyncio
from collections.abc import Awaitable, Callable

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
        await self._store_events_with_retry_fallback(events)

    async def _store_events_with_retry_fallback(self, events: list[DomainEvent]) -> None:
        await self._retry(lambda: self._store_events(events), max_attempts=3, delay=30)

    async def _store_events(self, events: list[DomainEvent]) -> None:
        events_to_publish = [DomainEventToConsumeModel.from_domain(event) for event in events]
        self._session.add_all(events_to_publish)
        await self._session.commit()

    async def _retry(
        self,
        func: Callable[[], Awaitable],
        max_attempts: int = 3,
        delay: float = 30,
        _attempt: int = 1
    ) -> None:
        try:
            await func()
        except Exception as error:
            if _attempt >= max_attempts:
                raise error

            await asyncio.sleep(delay * _attempt)
            return await self._retry(func, max_attempts, delay, _attempt + 1)
