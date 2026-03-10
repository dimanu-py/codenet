from abc import ABC, abstractmethod
from typing import Self, override

from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.invalid_criteria import (
    InvalidCompositeExpressionStructure,
    InvalidCriteriaStructure,
    InvalidExpressionStructure,
)
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import ComparisonOperatorDoesNotExist, Operator
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
    def __init__(self, field: Field, operator: Operator, value: Value) -> None:
        self.field = field
        self.operator = operator
        self.value = value

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

    def field_name(self) -> str:
        return self.field.value

    @override
    def to_primitives(self) -> dict[str, str | list]:
        return {
            "field": self.field.value,
            f"{self.operator.value}": self.value.value,
        }


class CompositeExpression(Expression):
    def __init__(
        self,
        operator: LogicalOperator,
        conditions: list[Expression],
    ) -> None:
        self.logical_operator = operator
        self.conditions = conditions

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

    def is_and(self) -> bool:
        return self.logical_operator == LogicalOperator.AND

    @override
    def to_primitives(self) -> dict[str, str | list]:
        return {self.logical_operator: [item.to_primitives() for item in self.conditions]}


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
