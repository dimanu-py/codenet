from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.condition.logical_operator import LogicalOperator
from src.shared.infra.criteria.operator_to_sql_translate_strategy import (
    OperatorToSqlTranslateStrategyFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class ConditionToSqlQueryStrategy(ABC):
    @abstractmethod
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        raise NotImplementedError


class NestedLogicalConditionToSqlQueryAndStrategy(ConditionToSqlQueryStrategy):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ConditionToSqlQueryStrategyFactory.get(condition).convert(model, condition)
            for condition in condition[LogicalOperator.AND]
        ]
        return and_(*query_predicates)


class NestedLogicalConditionToSqlQueryOrStrategy(ConditionToSqlQueryStrategy):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        query_predicates = [
            ConditionToSqlQueryStrategyFactory.get(condition).convert(model, condition)
            for condition in condition[LogicalOperator.OR]
        ]
        return or_(*query_predicates)


class ComparatorConditionToSqlQueryStrategy(ConditionToSqlQueryStrategy):
    def convert(
        self,
        model: type[Base],
        condition: dict[str, Any],
    ) -> ColumnElement[bool]:
        operator_to_sql_translator_strategy = OperatorToSqlTranslateStrategyFactory.get(condition["operator"])
        field = getattr(model, condition["field"])
        value = condition["value"]
        return operator_to_sql_translator_strategy.build(field, value)


class ConditionToSqlQueryStrategyFactory:
    @staticmethod
    def get(condition: dict[str, Any]) -> ConditionToSqlQueryStrategy:
        if LogicalOperator.AND in condition:
            return NestedLogicalConditionToSqlQueryAndStrategy()
        if LogicalOperator.OR in condition:
            return NestedLogicalConditionToSqlQueryOrStrategy()
        return ComparatorConditionToSqlQueryStrategy()
