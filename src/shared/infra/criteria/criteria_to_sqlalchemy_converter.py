from sqlalchemy.sql import select, Select, and_, or_
from sqlalchemy.sql.elements import BinaryExpression

from src.shared.domain.criteria.condition.condition import Condition
from src.shared.domain.criteria.condition.condition_strategies import (
    ConditionStrategyFactory,
)
from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter_expression import FilterExpression
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlalchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if criteria.is_empty():
            return query

        where_clause = self._construct_where_clause(model, criteria._expression)
        if where_clause is not None:
            query = query.where(where_clause)
        return query

    def _construct_where_clause(
        self, model: type[Base], node: FilterExpression | Condition
    ) -> BinaryExpression | None:
        if isinstance(node, FilterExpression):
            if node.is_empty():
                return None

            conditions = [
                self._construct_where_clause(model, filter_)
                for filter_ in node._conditions
            ]
            if node.has_and_logical_operator():
                return and_(*conditions)
            return or_(*conditions)

        condition_primitives = node.to_primitives()
        column = getattr(model, condition_primitives["field"])
        return self._build_condition(node, column)

    def _build_condition(self, condition: Condition, column: str) -> BinaryExpression:
        condition_strategy = ConditionStrategyFactory.get(condition._operator)
        return condition_strategy.build(column, condition._value.value)
