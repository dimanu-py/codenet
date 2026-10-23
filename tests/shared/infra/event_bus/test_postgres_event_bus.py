from datetime import datetime

import pytest
from expects import equal, expect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel
from src.shared.infra.event_bus.postgres_event_bus import (
    PostgresEventBus,
)
from tests.shared.infra.event_bus.dummy_domain_event import DummyDomainEvent, DummyDomainEventAttributes, DummyUnknownEvent
from tests.shared.infra.event_bus.mothers.dummy_domain_event_mother import DummyDomainEventMother
from tests.shared.infra.event_bus.dummy_event_subscriber import DummyEventSubscriber


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresEventBus:
    _NUMBER_OF_EVENTS_TO_CONSUME = 3
    _EVENT_CLASSES_BY_NAME = {
        DummyDomainEvent.name: DummyDomainEvent,
        DummyUnknownEvent.name: DummyUnknownEvent,
    }

    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._event_bus = PostgresEventBus(session=session, subscribers=[DummyEventSubscriber()])

    async def test_should_publish_a_single_event(self) -> None:
        events = [DummyDomainEventMother.any()]

        await self._event_bus.publish(events)

        events_to_consume = await self._get_stored_events(events=events)
        expect(events_to_consume).to(equal(events))

    async def test_should_publish_multiple_events(self) -> None:
        events = DummyDomainEventMother.many(3)

        await self._event_bus.publish(events)

        events_to_consume = await self._get_stored_events(events)
        expect(events_to_consume).to(equal(events))

    async def test_should_not_publish_events_when_there_are_no_events_to_publish(self) -> None:
        events = []

        await self._event_bus.publish(events)

        events_to_consume = await self._get_stored_events(events)
        expect(events_to_consume).to(equal(events))

    async def test_should_not_consume_anything_when_there_are_no_events(self) -> None:
        query = select(func.count()).select_from(DomainEventToConsumeModel)
        events_to_consume_before = (await self._session.execute(query)).scalar_one()

        await self._event_bus.consume(amount=self._NUMBER_OF_EVENTS_TO_CONSUME)

        events_to_consume_after = (await self._session.execute(query)).scalar_one()
        expect(events_to_consume_before).to(equal(events_to_consume_after))

    async def test_should_consume_event_when_is_subscribed_to_it(self) -> None:
        events = [DummyDomainEventMother.any()]
        await self._event_bus.publish(events)

        await self._event_bus.consume(amount=self._NUMBER_OF_EVENTS_TO_CONSUME)

        events_to_consume = await self._get_stored_events(events=events)
        expect(events_to_consume).to(equal([]))

    async def test_should_not_consume_unknown_event(self) -> None:
        event_unknown = DummyDomainEventMother.unknown()
        events = [event_unknown, DummyDomainEventMother.any()]
        await self._event_bus.publish(events)

        await self._event_bus.consume(amount=self._NUMBER_OF_EVENTS_TO_CONSUME)

        events_to_consume = await self._get_stored_events(events=events)
        expect(events_to_consume).to(equal([event_unknown]))

    async def _get_stored_events(self, events: list[DomainEvent]) -> list[DomainEvent]:
        event_ids = [event.id for event in events]
        result = await self._session.execute(
            select(DomainEventToConsumeModel).where(DomainEventToConsumeModel.id.in_(event_ids)),
        )
        events_to_consume = result.scalars().all()
        return [
            self._EVENT_CLASSES_BY_NAME[event.name](
                id=event.id, occurred_at=event.occurred_at, attributes=DummyDomainEventAttributes(**event.attributes)
            )
            for event in events_to_consume
        ]
