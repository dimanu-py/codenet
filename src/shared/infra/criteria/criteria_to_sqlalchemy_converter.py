from sqlalchemy import UnaryExpression
from sqlalchemy.sql import Select, select

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.expression_to_sql_converter import ExpressionToSqlConverterFactory
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlalchemyConverter:
    def __init__(self) -> None:
        self._query = None

    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        self._build_basic_query_selecting_all_columns(model)

        if criteria.has_sorting():
            self._build_order_by_clauses(criteria, model)

        if criteria.is_empty():
            return self._query

        self._build_where_conditions(criteria, model)

        return self._query

    def _build_basic_query_selecting_all_columns(self, model: type[Base]) -> None:
        self._query = select(model)

    def _build_order_by_clauses(self, criteria: Criteria, model: type[Base]) -> None:
        self._query = self._query.order_by(*self._translate_sorts_to_sql_order_by(criteria, model))

    def _build_where_conditions(self, criteria: Criteria, model: type[Base]) -> None:
        self._query = self._query.where(ExpressionToSqlConverterFactory.convert(model, criteria.expression))

    @staticmethod
    def _translate_sorts_to_sql_order_by(criteria: Criteria, model: type[Base]) -> tuple[UnaryExpression, ...]:
        order_by_clauses = []

        for sort_condition in criteria.sorts:
            field = getattr(model, sort_condition.field_name())
            if sort_condition.is_ascending():
                order_by_clauses.append(field.asc())
            else:
                order_by_clauses.append(field.desc())

        return tuple(order_by_clauses)
