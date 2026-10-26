from datetime import datetime

from src.shared.domain.event_bus.domain_event import DomainEvent, DomainEventAttributes


class AccountSignedUpAttributes(DomainEventAttributes):
    id: str
    username: str
    email: str
    status: str
    created_at: datetime


class AccountSignedUp(DomainEvent):
    name = "codenet.v1.account.signed_up"
    attributes: AccountSignedUpAttributes
