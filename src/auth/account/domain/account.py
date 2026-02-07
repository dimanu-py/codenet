from datetime import datetime
from typing import Self

from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_id import AccountId
from src.auth.account.domain.account_password_hash import AccountPasswordHash
from src.auth.account.domain.account_status import AccountStatus
from src.shared.domain.clock import Clock
from src.shared.domain.value_objects.aggregate import Aggregate


class Account(Aggregate):
    def __init__(self, id: str, email: str, password: str, status: str, created_at: datetime) -> None:
        self._id = AccountId(id)
        self._email = AccountEmail(email)
        self._password = AccountPasswordHash(password)
        self._status = AccountStatus(status)
        self._created_at = created_at

    @classmethod
    def signup(cls, id: str, email: str, password: str, clock: Clock) -> Self:
        return cls(
            id=id,
            email=email,
            password=password,
            status="active",
            created_at=clock.now(),
        )
