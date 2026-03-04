from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.infra.criteria.operator_to_sql_translator import (
    OperatorToSqlTranslatorFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class ExpressionToSqlConverter(ABC):
    @abstractmethod
    def convert(
        self,
        model: type[Base],
        expression: dict[str, Any],
    ) -> ColumnElement[bool]:
        raise NotImplementedError


class AndCompositeExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.get(condition).convert(model, condition)
            for condition in expression[LogicalOperator.AND]
        ]
        return and_(*query_predicates)


class OrCompositeExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.get(condition).convert(model, condition)
            for condition in expression[LogicalOperator.OR]
        ]
        return or_(*query_predicates)


class ComparatorExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: dict[str, Any],
    ) -> ColumnElement[bool]:
        field = getattr(model, expression["field"])
        operator = next(key for key in expression.keys() if key != "field")
        value = expression[operator]

        operator_to_sql_translator_strategy = OperatorToSqlTranslatorFactory.get(operator)
        return operator_to_sql_translator_strategy.build(field, value)


class ExpressionToSqlConverterFactory:
    @staticmethod
    def get(expression: dict[str, Any]) -> ExpressionToSqlConverter:
        if LogicalOperator.AND in expression:
            return AndCompositeExpressionToSqlConverter()
        if LogicalOperator.OR in expression:
            return OrCompositeExpressionToSqlConverter()
        return ComparatorExpressionToSqlConverter()
