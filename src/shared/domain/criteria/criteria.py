from typing import Any, Self, override

from src.shared.domain.criteria.expression import EmptyExpression, Expression, ExpressionFactory


class Criteria:
    def __init__(self, expression: Expression) -> None:
        self._expression = expression

    def is_empty(self) -> bool:
        return isinstance(self._expression, EmptyExpression)

    @classmethod
    def from_primitives(cls, expression: dict[str, Any]) -> Self:
        return cls(
            expression=ExpressionFactory.from_primitives(expression)
            if expression
            else ExpressionFactory.empty()
        )

    def to_primitives(self) -> dict[str, Any]:
        return self._expression.to_primitives()

    @override
    def __eq__(self, other: Self) -> bool:
        return self.to_primitives() == other.to_primitives()
