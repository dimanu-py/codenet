from abc import ABC, abstractmethod

from sqlalchemy.sql.elements import BinaryExpression

from src.shared.domain.criteria.condition.operator import Operator


class ConditionStrategy(ABC):
    @abstractmethod
    def build(self, column: str, value: str) -> BinaryExpression:
        raise NotImplementedError


class EqualConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column == value  # type: ignore


class NotEqualConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column != value  # type: ignore


class ContainsConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column.ilike(f"%{value}%")  # type: ignore


class AllConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column.is_not(None)  # type: ignore


class GreaterThanConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column > value  # type: ignore


class GreaterThanOrEqualConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column >= value  # type: ignore


class LessThanConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column < value  # type: ignore


class LessThanOrEqualConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return column <= value  # type: ignore


class NotContainsConditionStrategy(ConditionStrategy):
    def build(self, column: str, value: str) -> BinaryExpression:
        return ~column.ilike(f"%{value}%")  # type: ignore


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
