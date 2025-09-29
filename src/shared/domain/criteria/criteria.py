from typing import Any, Self, override

from src.shared.domain.criteria.condition.condition import Condition
from src.shared.domain.criteria.condition.nested_logical_condition import (
    NestedLogicalCondition,
)


class Criteria:
    def __init__(self, expression: Condition) -> None:
        self._expression = expression

    def is_empty(self) -> bool:
        return isinstance(self._expression, NestedLogicalCondition) and self._expression.is_empty()

    @classmethod
    def from_primitives(cls, filter_expression: dict[str, Any]) -> Self:
        return cls(
            expression=NestedLogicalCondition.from_primitives(filter_expression)
            if filter_expression
            else NestedLogicalCondition.empty()
        )

    def to_primitives(self) -> dict[str, Any]:
        return self._expression.to_primitives()

    @override
    def __eq__(self, other: Self) -> bool:
        return self.to_primitives() == other.to_primitives()
