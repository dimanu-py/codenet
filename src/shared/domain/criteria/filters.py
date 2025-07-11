from typing import Any, Self, Union

from src.shared.domain.criteria.condition.comparator_condition import ComparatorCondition
from src.shared.domain.criteria.nested_logical_condition import NestedLogicalCondition


class Filters:
    def __init__(self, expression: Union[NestedLogicalCondition, ComparatorCondition]) -> None:
        self._expression = expression

    def is_empty(self) -> bool:
        return (
            isinstance(self._expression, NestedLogicalCondition)
            and self._expression.is_empty()
        )

    @classmethod
    def from_primitives(
        cls,
        filters: dict[str, Any],
    ) -> Self:
        return cls(expression=NestedLogicalCondition.from_primitives(filters))

    def to_primitives(self) -> dict[str, Any]:
        return self._expression.to_primitives()
