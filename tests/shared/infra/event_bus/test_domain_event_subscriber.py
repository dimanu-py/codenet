import pytest
from expects import equal, expect, be

from shared.domain.event_bus.domain_event_subscriber import DomainEventSubscriber
from tests.shared.infra.event_bus.dummy_domain_event import DummyDomainEvent
from tests.shared.infra.event_bus.mothers.dummy_domain_event_mother import DummyDomainEventMother


class DummyEventSubscriber(DomainEventSubscriber[DummyDomainEvent]):
    def __init__(self) -> None:
        self.executed_events = []

    async def on(self, event: DummyDomainEvent) -> None:
        self.executed_events.append(event)

    def subscribed_to(self) -> type[DummyDomainEvent]:
        return DummyDomainEvent


@pytest.mark.unit
class TestDomainEventSubscriber:
    async def test_should_execute_on_event_received(self) -> None:
        subscriber = DummyEventSubscriber()
        event = DummyDomainEventMother.any()

        await subscriber.on(event)

        expect(subscriber.executed_events).to(equal([event]))

    def test_should_return_the_event_its_subscribed_to(self) -> None:
        subscriber = DummyEventSubscriber()

        event_subscribed_to = subscriber.subscribed_to()

        expect(event_subscribed_to).to(be(DummyDomainEvent))
