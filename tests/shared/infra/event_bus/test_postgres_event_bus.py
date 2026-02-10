import pytest
from expects import expect, equal

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.infra.event_bus.postgres_event_bus import PostgresEventBus
from tests.shared.domain.event_bus.mothers.domain_event_mother import DomainEventMother


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresEventBus:
    def setup_method(self) -> None:
        self._event_bus = PostgresEventBus()

    async def test_should_publish_a_single_event(self) -> None:
        event = DomainEventMother.any()

        await self._event_bus.publish([event])

        inserted_events = await self._get_events_to_consume()
        expect(inserted_events).to(equal([event]))

    async def _get_events_to_consume(self) -> list[DomainEvent]:
        pass
