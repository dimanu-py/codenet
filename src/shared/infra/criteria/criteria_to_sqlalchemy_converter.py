from sqlalchemy.sql import select, Select
from sqlalchemy.sql.elements import ColumnElement

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.condition_to_sql_query_strategy import (
    ConditionToSqlQueryStrategyFactory,
)
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
        condition = criteria.to_primitives()
        condition_to_sql_query_strategy = ConditionToSqlQueryStrategyFactory.get(
            condition
        )
        where_predicate = condition_to_sql_query_strategy.convert(model, condition)
        return where_predicate
