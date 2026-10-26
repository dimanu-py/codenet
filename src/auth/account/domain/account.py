from datetime import datetime
from typing import Self

from value_object import AggregateRoot

from src.auth.account.domain.account_created_at import AccountCreatedAt
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_id import AccountId
from src.auth.account.domain.account_password_hash import AccountPasswordHash
from src.auth.account.domain.account_signed_up import AccountSignedUp, AccountSignedUpAttributes
from src.auth.account.domain.account_status import AccountStatus
from src.auth.account.domain.account_username import AccountUsername
from src.shared.domain.clock import Clock
from src.shared.domain.event_bus.domain_event import DomainEvent


class Account(AggregateRoot):
    def __init__(self, id: str, username: str, email: str, password: str, status: str, created_at: datetime) -> None:
        self._id = AccountId(id)
        self._username = AccountUsername(username)
        self._email = AccountEmail(email)
        self._password = AccountPasswordHash(password)
        self._status = AccountStatus(status)
        self._created_at = AccountCreatedAt(created_at)
        self.__domain_events = []

    @classmethod
    def signup(cls, id: str, username: str, email: str, password: str, clock: Clock) -> Self:
        account = cls(
            id=id,
            username=username,
            email=email,
            password=password,
            status=AccountStatus.default(),
            created_at=clock.now(),
        )
        account._record(
            event=AccountSignedUp(
                id=id,
                occurred_at=clock.now(),
                attributes=AccountSignedUpAttributes(**account.to_primitives(exclude="password")),
            )
        )
        return account

    def has_email(self, email: AccountEmail) -> bool:
        return self._email == email

    def has_username(self, username: AccountUsername) -> bool:
        return self._username == username

    @property
    def id(self) -> AccountId:
        return self._id

    def _record(self, event: DomainEvent) -> None:
        self.__domain_events.append(event)

    def pull_domain_events(self) -> list[DomainEvent]:
        recorded_events = self.__domain_events
        self.__domain_events = []
        return recorded_events
