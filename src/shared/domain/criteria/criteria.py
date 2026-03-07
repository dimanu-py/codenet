from typing import Any, Self, override

from src.shared.domain.criteria.expression import EmptyExpression, Expression, ExpressionFactory
from src.shared.domain.criteria.sorts import Sorts


class Criteria:
    def __init__(self, expression: Expression, sorts: Sorts) -> None:
        self.expression = expression
        self.sorts = sorts

    def is_empty(self) -> bool:
        return isinstance(self.expression, EmptyExpression)

    def has_sorting(self) -> bool:
        return self.sorts.is_not_empty()

    @classmethod
    def from_primitives(cls, expression: dict[str, Any], sorts: list[dict[str, str]] | None = None) -> Self:
        return cls(
            expression=ExpressionFactory.from_primitives(expression) if expression else ExpressionFactory.empty(),
            sorts=Sorts.from_primitives(sorts) if sorts else Sorts.empty(),
        )

    def to_primitives(self) -> dict[str, Any]:
        return {
            "expression": self.expression.to_primitives(),
            "sorts": self.sorts.to_primitives(),
        }

    @override
    def __eq__(self, other: Self) -> bool:
        return self.to_primitives() == other.to_primitives()
