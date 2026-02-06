from datetime import datetime
from unittest.mock import Mock

from src.shared.domain.clock import Clock


class MockClock(Clock):
    def __init__(self) -> None:
        self._mock_now = Mock()

    def now(self) -> datetime:
        self._mock_now.assert_called_with()
        return self._mock_now.return_value

    def should_generate(self, date: datetime) -> None:
        self._mock_now()
        self._mock_now.return_value = date
