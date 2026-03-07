from sqlalchemy.sql import Select, select

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.expression_to_sql_converter import ExpressionToSqlConverterFactory
from src.shared.infra.criteria.sorts_to_sql_converter import SortsToSqlConverter
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlalchemyConverter:
    def __init__(self) -> None:
        self._query = None

    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        self._build_basic_query_selecting_all_columns(model)

        if criteria.has_sorting():
            self._convert_sorts_dsl_to_sql_ordering(criteria, model)

        if criteria.is_empty():
            return self._query

        self._convert_expression_dls_to_sql_where_predicate(criteria, model)

        return self._query

    def _build_basic_query_selecting_all_columns(self, model: type[Base]) -> None:
        self._query = select(model)

    def _convert_sorts_dsl_to_sql_ordering(self, criteria: Criteria, model: type[Base]) -> None:
        self._query = self._query.order_by(*SortsToSqlConverter.convert(criteria, model))

    def _convert_expression_dls_to_sql_where_predicate(self, criteria: Criteria, model: type[Base]) -> None:
        self._query = self._query.where(ExpressionToSqlConverterFactory.convert(model, criteria.expression))
