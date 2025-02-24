from sqlalchemy.sql import select, Select
from sqlalchemy.sql.elements import BinaryExpression

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter import Filter
from src.shared.domain.criteria.filter_operator import FilterOperator
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlAlchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if criteria.is_empty():
            return query

        for filter_ in criteria.filters:
            primitives_filter = filter_.to_primitives()
            column = getattr(model, primitives_filter["field"])
            condition = self._build_condition(filter_, column)
            query = query.where(condition)

        return query

    @staticmethod
    def _build_condition(filter_: Filter, column: str) -> BinaryExpression:
        primitive_filter = filter_.to_primitives()
        if filter_.operator_is(FilterOperator.EQUAL):
            return column == primitive_filter["value"]  # type: ignore
        if filter_.operator_is(FilterOperator.NOT_EQUAL):
            return column != primitive_filter["value"]  # type: ignore
        if filter_.operator_is(FilterOperator.CONTAINS):
            return column.ilike(f"%{primitive_filter['value']}%")  # type: ignore
        else:
            raise NotImplementedError
