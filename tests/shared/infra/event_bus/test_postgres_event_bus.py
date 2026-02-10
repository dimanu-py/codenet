import pytest
from expects import expect, equal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel
from src.shared.infra.event_bus.postgres_event_bus import PostgresEventBus
from tests.shared.infra.event_bus.dummy_domain_event import DummyDomainEvent
from tests.shared.infra.event_bus.mothers.dummy_domain_event_mother import DummyDomainEventMother


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresEventBus:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._event_bus = PostgresEventBus(session=session)

    async def test_should_publish_a_single_event(self) -> None:
        event = DummyDomainEventMother.any()

        await self._event_bus.publish([event])

        inserted_events = await self._get_events_to_consume(event_id=event.id)
        expect(inserted_events).to(equal([event]))

    async def _get_events_to_consume(self, event_id: str) -> list[DomainEvent]:
        result = await self._session.execute(
            select(DomainEventToConsumeModel).where(DomainEventToConsumeModel.id == event_id),
        )
        events_to_consume = result.scalars()
        return [
            DummyDomainEvent(id=event.id, occurred_at=event.occurred_at, attributes=event.attributes)
            for event in events_to_consume
        ]
