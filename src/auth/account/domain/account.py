from datetime import datetime

from src.shared.domain.value_objects.aggregate import Aggregate


class Account(Aggregate):
    def __init__(self, id: str, email: str, plain_password: str, status: str, created_at: str) -> None:
        self._id = id
        self._email = email
        self._password = plain_password
        self._status = status
        self._created_at = datetime.fromisoformat(created_at)
