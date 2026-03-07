from sqlalchemy import UnaryExpression
from sqlalchemy.sql import Select, select
from sqlalchemy.sql.elements import ColumnElement

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.expression_to_sql_converter import ExpressionToSqlConverterFactory
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlalchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if criteria.has_sorting():
            query = query.order_by(*self._build_order_by_clause(criteria, model))

        if criteria.is_empty():
            return query

        query = query.where(self._build_where_predicate(criteria, model))

        return query

    @staticmethod
    def _build_where_predicate(
        criteria: Criteria,
        model: type[Base],
    ) -> ColumnElement[bool] | None:
        return ExpressionToSqlConverterFactory.convert(model, criteria.expression)

    @staticmethod
    def _build_order_by_clause(criteria: Criteria, model: type[Base]) -> tuple[UnaryExpression, ...]:
        order_by_clauses = []

        for sort_condition in criteria.sorts:
            field = getattr(model, sort_condition.field_name())
            if sort_condition.is_ascending():
                order_by_clauses.append(field.asc())
            else:
                order_by_clauses.append(field.desc())

        return tuple(order_by_clauses)
