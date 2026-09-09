from typing import Any

from value_object import List

from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import Operator
from src.shared.domain.criteria.value import Value


class Filter:
    def __init__(self, field: str, operator: str, value: str) -> None:
        self.field = Field(field)
        self.operator = Operator(operator)
        self.value = Value(value)

    def field_name(self) -> str:
        return self.field.value

    def to_primitives(self) -> dict[str, str]:
        return {
            "field": self.field.value,
            f"{self.operator.value}": self.value.value,
        }


class Filters(List[Filter]):
    def __init__(self, filters: list[Filter]) -> None:
        super().__init__(value=filters)

    def has_filters(self) -> bool:
        return len(self._value) > 0

    @classmethod
    def empty(cls) -> "Filters":
        return cls(filters=[])

    def to_primitives(self) -> dict[str, Any]:
        if self._is_empty():
            return {}
        if self._has_one_filter():
            return self._value[0].to_primitives()
        return {LogicalOperator.AND: [filter_.to_primitives() for filter_ in self._value]}

    def _is_empty(self) -> bool:
        return len(self._value) == 0

    def _has_one_filter(self) -> bool:
        return len(self._value) == 1
