from typing import Any, Self, Union

from src.shared.domain.criteria.condition.condition import Condition
from src.shared.domain.criteria.filter_expression import FilterExpression
from src.shared.domain.criteria.logical_operator import LogicalOperator


class Filters:
    def __init__(
        self, expression: Union[FilterExpression, Condition]
    ) -> None:
        self._expression = expression

    def is_empty(self) -> bool:
        return isinstance(self._expression, FilterExpression) and self._expression.is_empty()

    @classmethod
    def from_primitives(
        cls,
        filters: dict[str, Any],
    ) -> Self:
        return cls(expression=FilterExpression.from_primitives(filters))

    def to_primitives(self) -> dict[str, Any]:
        return self._expression.to_primitives()
