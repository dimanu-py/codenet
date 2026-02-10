from datetime import UTC

from sindripy.mothers import ObjectMother

from tests.shared.infra.event_bus.dummy_domain_event import DummyDomainEvent, DummyDomainEventAttributes


class DummyDomainEventMother(ObjectMother):
    @classmethod
    def any(cls) -> DummyDomainEvent:
        return DummyDomainEvent(
            id=cls._faker().uuid4(),
            occurred_at=cls._faker().date_time(tzinfo=UTC),
            attributes=DummyDomainEventAttributes(
                id=cls._faker().uuid4(),
                name=cls._faker().name(),
            ),
        )
