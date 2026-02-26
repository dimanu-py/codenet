from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.condition.logical_operator import LogicalOperator
from src.shared.infra.criteria.operator_to_sql_translator import (
    OperatorToSqlTranslatorFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class ConditionToSqlQueryConverter(ABC):
    @abstractmethod
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        raise NotImplementedError


class NestedLogicalConditionToSqlQueryAndConverter(ConditionToSqlQueryConverter):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ConditionToSqlQueryConverterFactory.get(condition).convert(model, condition)
            for condition in condition[LogicalOperator.AND]
        ]
        return and_(*query_predicates)


class NestedLogicalConditionToSqlQueryOrConverter(ConditionToSqlQueryConverter):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ConditionToSqlQueryConverterFactory.get(condition).convert(model, condition)
            for condition in condition[LogicalOperator.OR]
        ]
        return or_(*query_predicates)


class ComparatorConditionToSqlQueryConverter(ConditionToSqlQueryConverter):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        field = getattr(model, condition["field"])
        operator = next(key for key in condition.keys() if key != "field")
        value = condition[operator]

        operator_to_sql_translator_strategy = OperatorToSqlTranslatorFactory.get(operator)
        return operator_to_sql_translator_strategy.build(field, value)


class ConditionToSqlQueryConverterFactory:
    @staticmethod
    def get(condition: dict[str, Any]) -> ConditionToSqlQueryConverter:
        if LogicalOperator.AND in condition:
            return NestedLogicalConditionToSqlQueryAndConverter()
        if LogicalOperator.OR in condition:
            return NestedLogicalConditionToSqlQueryOrConverter()
        return ComparatorConditionToSqlQueryConverter()
