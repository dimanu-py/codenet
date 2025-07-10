from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.shared.domain.criteria.condition.operator import Operator


class ConditionStrategy(ABC):
    @abstractmethod
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        raise NotImplementedError


class EqualConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column == value


class NotEqualConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column != value


class ContainsConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column.ilike(f"%{value}%")


class AllConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column.is_not(None)


class GreaterThanConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column > value


class GreaterThanOrEqualConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column >= value


class LessThanConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column < value


class LessThanOrEqualConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column <= value


class NotContainsConditionStrategy(ConditionStrategy):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return ~column.ilike(f"%{value}%")


class ConditionStrategyFactory:
    @staticmethod
    def get(operator: Operator) -> ConditionStrategy:
        strategies = {
            Operator.EQUAL: EqualConditionStrategy(),
            Operator.NOT_EQUAL: NotEqualConditionStrategy(),
            Operator.CONTAINS: ContainsConditionStrategy(),
            Operator.ALL: AllConditionStrategy(),
            Operator.GREATER_THAN: GreaterThanConditionStrategy(),
            Operator.GREATER_THAN_OR_EQUAL: GreaterThanOrEqualConditionStrategy(),
            Operator.LESS_THAN: LessThanConditionStrategy(),
            Operator.LESS_THAN_OR_EQUAL: LessThanOrEqualConditionStrategy(),
            Operator.NOT_CONTAINS: NotContainsConditionStrategy(),
        }
        condition_strategy = strategies.get(operator)
        if not condition_strategy:
            raise NotImplementedError(
                f"Condition strategy for {operator} is not implemented."
            )
        return condition_strategy
