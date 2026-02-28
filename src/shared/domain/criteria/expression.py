from abc import ABC, abstractmethod
from typing import Self, override

from src.shared.domain.criteria.criteria_error import InvalidCriteriaStructure
from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import Operator
from src.shared.domain.criteria.value import Value


class Expression(ABC):
    @abstractmethod
    def from_primitives(self, expression: dict[str, list | str]) -> Self:
        raise NotImplementedError

    @abstractmethod
    def to_primitives(self) -> dict[str, list | str]:
        raise NotImplementedError


class Comparison(Expression):
    _value: Value
    _operator: Operator
    _field: Field

    def __init__(self, field: str, operator: str, value: str) -> None:
        self._field = Field(field)
        self._operator = Operator(operator)
        self._value = Value(value)

    @classmethod
    @override
    def from_primitives(cls, expression: dict[str, str | list]) -> Self:
        raw_operator = next(key for key in expression.keys() if key in Operator)
        operator = Operator(raw_operator)

        return cls(
            field=expression["field"],  # type: ignore
            operator=operator,
            value=expression[operator],  # type: ignore
        )

    @override
    def to_primitives(self) -> dict[str, str | list]:
        return {
            "field": self._field.value,
            f"{self._operator.value}": self._value.value,
        }


class LogicalGroup(Expression):
    _logical_operator: LogicalOperator
    _conditions: list[Expression]

    def __init__(
        self,
        operator: LogicalOperator,
        conditions: list[Expression],
    ) -> None:
        self._logical_operator = operator
        self._conditions = conditions

    @classmethod
    @override
    def from_primitives(cls, expression: dict[str, str | list]) -> Expression:
        if LogicalOperator.AND in expression:
            conditions = [ExpressionFactory.from_primitives(item) for item in expression[LogicalOperator.AND]]  # type: ignore
            return cls(operator=LogicalOperator.AND, conditions=conditions)
        if LogicalOperator.OR in expression:
            conditions = [ExpressionFactory.from_primitives(item) for item in expression[LogicalOperator.OR]]  # type: ignore
            return cls(operator=LogicalOperator.OR, conditions=conditions)
        raise InvalidCriteriaStructure("Logical group filter must contain either 'AND' or 'OR'")

    @classmethod
    def empty(cls) -> Self:
        return cls(operator=LogicalOperator.AND, conditions=[])

    def has_and_logical_operator(self) -> bool:
        return self._logical_operator == LogicalOperator.AND

    @override
    def to_primitives(self) -> dict[str, str | list]:
        key = LogicalOperator.AND if self._logical_operator is LogicalOperator.AND else LogicalOperator.OR
        return {key: [item.to_primitives() for item in self._conditions]}

    def is_empty(self) -> bool:
        return len(self._conditions) == 0


class EmptyExpression(Expression):
    @classmethod
    @override
    def from_primitives(cls, expression: dict[str, list | str]) -> Self:
        return cls()

    @override
    def to_primitives(self) -> dict[str, list | str]:
        return {}


class ExpressionFactory:
    @classmethod
    def from_primitives(cls, expression: dict[str, list | str]) -> Expression:
        cls._ensure_expression_has_valid_structure(expression)
        if cls._is_logical_group(expression):
            return LogicalGroup.from_primitives(expression)
        if cls._is_simple_comparison(expression):
            return Comparison.from_primitives(expression)
        raise InvalidCriteriaStructure("Criteria filter expression must contain 'field' or a logical operator 'and/or'")

    @classmethod
    def empty(cls) -> Expression:
        return EmptyExpression()

    @classmethod
    def _is_logical_group(cls, expression: dict[str, list | str]) -> bool:
        return LogicalOperator.AND in expression or LogicalOperator.OR in expression

    @classmethod
    def _ensure_expression_has_valid_structure(cls, expression: dict[str, list | str]) -> None:
        if not isinstance(expression, dict):
            raise InvalidCriteriaStructure("Criteria must be a dictionary")

    @classmethod
    def _is_simple_comparison(cls, expression: dict[str, list | str]) -> bool:
        return "field" in expression
