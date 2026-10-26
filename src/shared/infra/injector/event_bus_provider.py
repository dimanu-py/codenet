from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.event_bus import EventBus
from src.shared.infra.event_bus.postgres_event_bus import PostgresEventBus
from src.shared.infra.injector.registry import dependency_provider


@dependency_provider
class EventBusProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def event_bus(self, session: AsyncSession) -> EventBus:
        return PostgresEventBus(session=session, subscribers=[])
