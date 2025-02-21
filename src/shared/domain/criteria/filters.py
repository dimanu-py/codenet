from dataclasses import dataclass

from src.shared.domain.criteria.filter import Filter


@dataclass(frozen=True)
class Filters:
    _value: list[Filter]

    @classmethod
    def from_primitives(cls, filters: list[dict[str, str]]) -> "Filters":
        value = [
            Filter.from_primitives(
                field=filter["field"],
                operator=filter["operator"],
                value=filter["value"],
            )
            for filter in filters
        ]
        return Filters(value)

    def to_primitives(self) -> list[dict[str, str]]:
        return [filter_.to_primitives() for filter_ in self._value]
