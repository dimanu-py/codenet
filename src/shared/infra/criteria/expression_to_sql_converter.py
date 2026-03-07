from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.expression import CompositeExpression, ComparisonExpression, Expression
from src.shared.infra.criteria.operator_to_sql_translator import (
    OperatorToSqlTranslatorFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class AndCompositeExpressionToSqlConverter:
    @staticmethod
    def convert(
        model: type[Base],
        expression: CompositeExpression,
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.convert(model, condition) for condition in expression.conditions
        ]
        return and_(*query_predicates)


class OrCompositeExpressionToSqlConverter:
    @staticmethod
    def convert(
        model: type[Base],
        expression: CompositeExpression,
    ) -> ColumnElement[bool]:
        query_predicates = [
            ExpressionToSqlConverterFactory.convert(model, condition) for condition in expression.conditions
        ]
        return or_(*query_predicates)


class ComparisonExpressionToSqlConverter:
    @staticmethod
    def convert(
        model: type[Base],
        expression: ComparisonExpression,
    ) -> ColumnElement[bool]:
        field = getattr(model, expression.field_name())
        operator_to_sql_translator_strategy = OperatorToSqlTranslatorFactory.get(expression.operator)
        return operator_to_sql_translator_strategy.build(field, expression.value.value)


class ExpressionToSqlConverterFactory:
    @staticmethod
    def convert(model: type[Base], expression: Expression) -> ColumnElement[bool]:
        if isinstance(expression, ComparisonExpression):
            return ComparisonExpressionToSqlConverter.convert(model, expression)
        if isinstance(expression, CompositeExpression):
            if expression.is_and():
                return AndCompositeExpressionToSqlConverter.convert(model, expression)
            else:
                return OrCompositeExpressionToSqlConverter.convert(model, expression)
        raise ValueError(f"Unsupported expression type: {type(expression)}")
