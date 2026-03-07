from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.shared.domain.criteria.operator import Operator


class OperatorToSqlConverter(ABC):
    @abstractmethod
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        raise NotImplementedError


class EqualOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column == value


class NotEqualOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column != value


class ContainsOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column.ilike(f"%{value}%")


class GreaterThanOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column > value


class GreaterThanOrEqualOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column >= value


class LessThanOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column < value


class LessThanOrEqualOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column <= value


class NotContainsOperatorToSqlConverter(OperatorToSqlConverter):
    def convert(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return ~column.ilike(f"%{value}%")


class OperatorToSqlConverterFactory:
    @staticmethod
    def get(operator: Operator) -> OperatorToSqlConverter:
        translators = {
            Operator.EQUALS: EqualOperatorToSqlConverter(),
            Operator.NOT_EQUALS: NotEqualOperatorToSqlConverter(),
            Operator.GREATER_THAN: GreaterThanOperatorToSqlConverter(),
            Operator.GREATER_THAN_OR_EQUAL_TO: GreaterThanOrEqualOperatorToSqlConverter(),
            Operator.LESS_THAN: LessThanOperatorToSqlConverter(),
            Operator.LESS_THAN_OR_EQUAL_TO: LessThanOrEqualOperatorToSqlConverter(),
            Operator.CONTAINS: ContainsOperatorToSqlConverter(),
            Operator.NOT_CONTAINS: NotContainsOperatorToSqlConverter(),
        }
        operator_translator = translators.get(operator)
        if not operator_translator:
            raise NotImplementedError(f"Condition strategy for {operator} is not implemented.")
        return operator_translator
