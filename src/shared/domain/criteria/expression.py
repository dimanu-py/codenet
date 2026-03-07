from abc import ABC, abstractmethod
from typing import Self, override

from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.invalid_criteria import InvalidCriteriaStructure, InvalidCompositeExpressionStructure, \
    InvalidExpressionStructure
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import Operator, ComparisonOperatorDoesNotExist
from src.shared.domain.criteria.value import Value


class Expression(ABC):
    @classmethod
    @abstractmethod
    def from_primitives(cls, expression: dict[str, list | str]) -> Self:
        raise NotImplementedError

    @abstractmethod
    def to_primitives(self) -> dict[str, list | str]:
        raise NotImplementedError


class ComparisonExpression(Expression):
    _value: Value
    _operator: Operator
    _field: Field

    def __init__(self, field: Field, operator: Operator, value: Value) -> None:
        self._field = field
        self._operator = operator
        self._value = value

    @classmethod
    @override
    def from_primitives(cls, expression: dict[str, str | list]) -> Self:
        raw_operator = next((key for key in expression.keys() if key in Operator), None)
        if raw_operator is None:
            raise ComparisonOperatorDoesNotExist()

        return cls(
            field=Field(expression["field"]),
            operator=Operator(raw_operator),
            value=Value(expression[Operator(raw_operator)]),
        )

    @override
    def to_primitives(self) -> dict[str, str | list]:
        return {
            "field": self._field.value,
            f"{self._operator.value}": self._value.value,
        }


class CompositeExpression(Expression):
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
        raise InvalidCompositeExpressionStructure()

    @override
    def to_primitives(self) -> dict[str, str | list]:
        key = LogicalOperator.AND if self._logical_operator is LogicalOperator.AND else LogicalOperator.OR
        return {key: [item.to_primitives() for item in self._conditions]}


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
        if cls._is_composite_expression(expression):
            return CompositeExpression.from_primitives(expression)
        if cls._is_comparison_expression(expression):
            return ComparisonExpression.from_primitives(expression)
        raise InvalidExpressionStructure()

    @classmethod
    def empty(cls) -> Expression:
        return EmptyExpression()

    @classmethod
    def _is_composite_expression(cls, expression: dict[str, list | str]) -> bool:
        return LogicalOperator.AND in expression or LogicalOperator.OR in expression

    @classmethod
    def _ensure_expression_has_valid_structure(cls, expression: dict[str, list | str]) -> None:
        if not isinstance(expression, dict):
            raise InvalidCriteriaStructure()

    @classmethod
    def _is_comparison_expression(cls, expression: dict[str, list | str]) -> bool:
        return "field" in expression
