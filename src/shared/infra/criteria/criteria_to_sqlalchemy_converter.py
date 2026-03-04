from sqlalchemy.sql import Select, select
from sqlalchemy.sql.elements import ColumnElement

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.expression_to_sql_converter import ExpressionToSqlConverterFactory
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlalchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if criteria.is_empty():
            return query

        where_predicate = self._build_where_predicate(criteria, model)
        if where_predicate is not None:
            query = query.where(where_predicate)
        return query

    @staticmethod
    def _build_where_predicate(
        criteria: Criteria,
        model: type[Base],
    ) -> ColumnElement[bool] | None:
        expression = criteria.to_primitives()
        expression_to_sql_converter = ExpressionToSqlConverterFactory.get(expression)
        return expression_to_sql_converter.convert(model, expression)
