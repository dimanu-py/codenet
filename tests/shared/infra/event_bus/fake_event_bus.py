from typing import override

from expects import be_empty, contain, expect

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.domain.event_bus.event_bus import EventBus


class FakeEventBus(EventBus):
    def __init__(self) -> None:
        self._published_events = []

    @override
    async def publish(self, events: list[DomainEvent]) -> None:
        self._published_events.extend(events)

    def should_have_published(self, events: list[DomainEvent]) -> None:
        expect(self._published_events).to(contain(*events))

    def should_have_no_events(self) -> None:
        expect(self._published_events).to(be_empty)
