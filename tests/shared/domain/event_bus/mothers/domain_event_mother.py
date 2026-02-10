from src.shared.domain.event_bus.domain_event import DomainEvent


class DomainEventMother:
    @classmethod
    def any(cls) -> DomainEvent:
        raise NotImplementedError
