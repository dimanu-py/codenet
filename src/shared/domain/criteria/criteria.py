from typing import Any, Self, override

from src.shared.domain.criteria.expression import Expression
from src.shared.domain.criteria.logical_group import (
    LogicalGroup,
)


class Criteria:
    def __init__(self, expression: Expression) -> None:
        self._expression = expression

    def is_empty(self) -> bool:
        return isinstance(self._expression, LogicalGroup) and self._expression.is_empty()

    @classmethod
    def from_primitives(cls, filter_expression: dict[str, Any]) -> Self:
        return cls(
            expression=LogicalGroup.from_primitives(filter_expression)
            if filter_expression
            else LogicalGroup.empty()
        )

    def to_primitives(self) -> dict[str, Any]:
        return self._expression.to_primitives()

    @override
    def __eq__(self, other: Self) -> bool:
        return self.to_primitives() == other.to_primitives()
