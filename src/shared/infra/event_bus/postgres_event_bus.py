from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus


class PostgresEventBus(EventBus):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, events: Iterable[DomainEvent]) -> None:
        raise NotImplementedError
