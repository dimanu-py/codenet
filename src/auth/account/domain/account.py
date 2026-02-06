from datetime import datetime
from typing import Self

from src.shared.domain.value_objects.aggregate import Aggregate


class Account(Aggregate):
    def __init__(self, id: str, email: str, password: str, status: str, created_at: str) -> None:
        self._id = id
        self._email = email
        self._password = password
        self._status = status
        self._created_at = datetime.fromisoformat(created_at)

    @classmethod
    def signup(cls, id: str, email: str, password: str) -> Self:
        return cls(
            id=id,
            email=email,
            password=password,
            status="active",
            created_at=datetime.now().isoformat(),
        )