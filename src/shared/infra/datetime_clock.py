from datetime import UTC, datetime
from typing import override

from src.shared.domain.clock import Clock


class DatetimeClock(Clock):
    @override
    def now(self) -> datetime:
        return datetime.now(UTC)
