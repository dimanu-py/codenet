from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.expression import CompositeExpression, ComparisonExpression
from src.shared.infra.criteria.operator_to_sql_translator import (
    OperatorToSqlTranslatorFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class ExpressionToSqlConverter(ABC):
    @abstractmethod
    def convert(
        self,
        model: type[Base],
        expression: ComparisonExpression | CompositeExpression,
    ) -> ColumnElement[bool]:
        raise NotImplementedError


class AndCompositeExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: CompositeExpression,
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.get(condition).convert(model, condition)
            for condition in expression.conditions
        ]
        return and_(*query_predicates)


class OrCompositeExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: CompositeExpression,
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.get(condition).convert(model, condition)
            for condition in expression.conditions
        ]
        return or_(*query_predicates)


class ComparatorExpressionToSqlConverter(ExpressionToSqlConverter):
    def convert(
        self,
        model: type[Base],
        expression: ComparisonExpression,
    ) -> ColumnElement[bool]:
        field = getattr(model, expression.field_name())
        operator_to_sql_translator_strategy = OperatorToSqlTranslatorFactory.get(expression.operator)
        return operator_to_sql_translator_strategy.build(field, expression.value.value)


class ExpressionToSqlConverterFactory:
    @staticmethod
    def get(expression: ComparisonExpression | CompositeExpression) -> ExpressionToSqlConverter:
        if isinstance(expression, ComparisonExpression):
            return ComparatorExpressionToSqlConverter()
        if expression.is_and():
            return AndCompositeExpressionToSqlConverter()
        else:
            return OrCompositeExpressionToSqlConverter()
