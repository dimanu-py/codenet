from datetime import datetime

from src.shared.domain.value_objects.aggregate import Aggregate


class Account(Aggregate):
    def __init__(self, id: str, email: str, password: str, status: str, created_at: str) -> None:
        self._id = id
        self._email = email
        self._password = password
        self._status = status
        self._created_at = datetime.fromisoformat(created_at)
