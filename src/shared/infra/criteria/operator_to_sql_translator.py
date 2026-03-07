from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.shared.domain.criteria.operator import Operator


class OperatorToSqlTranslator(ABC):
    @abstractmethod
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        raise NotImplementedError


class EqualOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column == value


class NotEqualOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column != value


class ContainsOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column.ilike(f"%{value}%")


class GreaterThanOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column > value


class GreaterThanOrEqualOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column >= value


class LessThanOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column < value


class LessThanOrEqualOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return column <= value


class NotContainsOperatorToSqlTranslator(OperatorToSqlTranslator):
    def build(self, column: InstrumentedAttribute, value: str) -> ColumnElement[bool]:
        return ~column.ilike(f"%{value}%")


class OperatorToSqlTranslatorFactory:
    @staticmethod
    def get(operator: Operator) -> OperatorToSqlTranslator:
        translators = {
            Operator.EQUALS: EqualOperatorToSqlTranslator(),
            Operator.NOT_EQUALS: NotEqualOperatorToSqlTranslator(),
            Operator.GREATER_THAN: GreaterThanOperatorToSqlTranslator(),
            Operator.GREATER_THAN_OR_EQUAL_TO: GreaterThanOrEqualOperatorToSqlTranslator(),
            Operator.LESS_THAN: LessThanOperatorToSqlTranslator(),
            Operator.LESS_THAN_OR_EQUAL_TO: LessThanOrEqualOperatorToSqlTranslator(),
            Operator.CONTAINS: ContainsOperatorToSqlTranslator(),
            Operator.NOT_CONTAINS: NotContainsOperatorToSqlTranslator(),
        }
        operator_translator = translators.get(operator)
        if not operator_translator:
            raise NotImplementedError(f"Condition strategy for {operator} is not implemented.")
        return operator_translator
