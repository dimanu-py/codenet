from typing import override

from src.shared.domain.criteria.filters import Filters


class Criteria:
    _filters: Filters

    def __init__(self, filters: Filters) -> None:
        self._filters = filters

    @classmethod
    def from_primitives(cls, filters: list[dict]) -> "Criteria":
        return Criteria(filters=Filters.from_primitives(filters))

    def to_primitives(self) -> list[dict]:
        return self._filters.to_primitives()

    @override
    def __eq__(self, other: "Criteria") -> bool:
        return self.to_primitives() == other.to_primitives()
