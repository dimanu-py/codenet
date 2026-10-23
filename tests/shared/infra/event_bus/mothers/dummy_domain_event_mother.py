from datetime import UTC

from object_mother import ObjectMother

from tests.shared.infra.event_bus.dummy_domain_event import (
    DummyDomainEvent,
    DummyDomainEventAttributes,
    DummyUnknownEvent,
)


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

    @classmethod
    def many(cls, amount: int) -> list[DummyDomainEvent]:
        return [cls.any() for _ in range(amount)]

    @classmethod
    def unknown(cls) -> DummyUnknownEvent:
        return DummyUnknownEvent(
            id=cls._faker().uuid4(),
            occurred_at=cls._faker().date_time(tzinfo=UTC),
            attributes=DummyDomainEventAttributes(
                id=cls._faker().uuid4(),
                name=cls._faker().name(),
            ),
        )
