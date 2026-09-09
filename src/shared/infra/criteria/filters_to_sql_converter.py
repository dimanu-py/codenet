from sqlalchemy import ColumnElement, and_, or_

from src.shared.domain.criteria.criteria import AndCriteria, Criteria, OrCriteria
from src.shared.domain.criteria.filter import Filter
from src.shared.infra.criteria.operator_to_sql_translator import (
    OperatorToSqlConverterFactory,
)
from src.shared.infra.persistence.sqlalchemy.base import Base


class FilterToSqlConverter:
    @staticmethod
    def convert(model: type[Base], filter_: Filter) -> ColumnElement[bool]:
        field = getattr(model, filter_.field_name())
        operator_to_sql_translator_strategy = OperatorToSqlConverterFactory.get(filter_.operator)
        return operator_to_sql_translator_strategy.convert(field, filter_.value.value)


class CriteriaToSqlPredicateConverter:
    @staticmethod
    def convert(model: type[Base], criteria: Criteria) -> ColumnElement[bool]:
        if isinstance(criteria, AndCriteria):
            return and_(
                CriteriaToSqlPredicateConverter.convert(model, criteria.left),
                CriteriaToSqlPredicateConverter.convert(model, criteria.right),
            )
        if isinstance(criteria, OrCriteria):
            return or_(
                CriteriaToSqlPredicateConverter.convert(model, criteria.left),
                CriteriaToSqlPredicateConverter.convert(model, criteria.right),
            )
        return and_(*(FilterToSqlConverter.convert(model, filter_) for filter_ in criteria.filters))
