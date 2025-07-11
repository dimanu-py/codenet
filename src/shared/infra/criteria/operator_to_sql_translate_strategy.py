from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.shared.domain.criteria.condition.operator import Operator


class OperatorToSqlTranslateStrategy(ABC):
    @abstractmethod
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        raise NotImplementedError


class EqualOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column == value


class NotEqualOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column != value


class ContainsOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column.ilike(f"%{value}%")


class GreaterThanOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column > value


class GreaterThanOrEqualOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column >= value


class LessThanOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column < value


class LessThanOrEqualOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column <= value


class NotContainsOperatorToSqlTranslateStrategy(OperatorToSqlTranslateStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return ~column.ilike(f"%{value}%")


class OperatorToSqlTranslateStrategyFactory:
    @staticmethod
    def get(operator: str) -> OperatorToSqlTranslateStrategy:
        strategies = {
            Operator.EQUAL: EqualOperatorToSqlTranslateStrategy(),
            Operator.NOT_EQUAL: NotEqualOperatorToSqlTranslateStrategy(),
            Operator.GREATER_THAN: GreaterThanOperatorToSqlTranslateStrategy(),
            Operator.GREATER_THAN_OR_EQUAL: GreaterThanOrEqualOperatorToSqlTranslateStrategy(),
            Operator.LESS_THAN: LessThanOperatorToSqlTranslateStrategy(),
            Operator.LESS_THAN_OR_EQUAL: LessThanOrEqualOperatorToSqlTranslateStrategy(),
            Operator.CONTAINS: ContainsOperatorToSqlTranslateStrategy(),
            Operator.NOT_CONTAINS: NotContainsOperatorToSqlTranslateStrategy(),
        }
        condition_strategy = strategies.get(operator)
        if not condition_strategy:
            raise NotImplementedError(
                f"Condition strategy for {operator} is not implemented."
            )
        return condition_strategy
