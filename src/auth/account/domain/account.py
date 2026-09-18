from datetime import datetime
from typing import Self

from value_object import Aggregate

from src.auth.account.domain.account_created_at import AccountCreatedAt
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_id import AccountId
from src.auth.account.domain.account_password_hash import AccountPasswordHash
from src.auth.account.domain.account_status import AccountStatus
from src.auth.account.domain.account_username import AccountUsername
from src.shared.domain.clock import Clock


class Account(Aggregate):
    def __init__(self, id: str, username: str, email: str, password: str, status: str, created_at: datetime) -> None:
        self._id = AccountId(id)
        self._username = AccountUsername(username)
        self._email = AccountEmail(email)
        self._password = AccountPasswordHash(password)
        self._status = AccountStatus(status)
        self._created_at = AccountCreatedAt(created_at)

    @classmethod
    def signup(cls, id: str, username: str, email: str, password: str, clock: Clock) -> Self:
        return cls(
            id=id,
            username=username,
            email=email,
            password=password,
            status=AccountStatus.default(),
            created_at=clock.now(),
        )

    def has_email(self, email: AccountEmail) -> bool:
        return self._email == email

    def has_username(self, username: AccountUsername) -> bool:
        return self._username == username

    @property
    def id(self) -> AccountId:
        return self._id
