import pytest
from expects import expect, equal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel
from src.shared.infra.event_bus.postgres_event_bus import PostgresEventBus
from tests.shared.infra.event_bus.dummy_domain_event import DummyDomainEvent, DummyDomainEventAttributes
from tests.shared.infra.event_bus.mothers.dummy_domain_event_mother import DummyDomainEventMother


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresEventBus:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._event_bus = PostgresEventBus(session=session)

    async def test_should_publish_a_single_event(self) -> None:
        events = [DummyDomainEventMother.any()]

        await self._event_bus.publish(events)

        inserted_event = await self._get_events_to_consume(events=events)
        expect(inserted_event).to(equal(events))

    async def _get_events_to_consume(self, events: list[DomainEvent]) -> list[DomainEvent]:
        event_ids = [event.id for event in events]
        result = await self._session.execute(
            select(DomainEventToConsumeModel).where(DomainEventToConsumeModel.id.in_(event_ids)),
        )
        events_to_consume = result.scalars().all()
        return [
            DummyDomainEvent(
                id=event.id,
                occurred_at=event.occurred_at,
                attributes=DummyDomainEventAttributes(**event.attributes)
            )
            for event in events_to_consume
        ]
