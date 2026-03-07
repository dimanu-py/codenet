from sqlalchemy import UnaryExpression

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.persistence.sqlalchemy.base import Base


class SortsToSqlConverter:
    @staticmethod
    def convert(criteria: Criteria, model: type[Base]) -> tuple[UnaryExpression, ...]:
        order_by_clauses = []

        for sort_condition in criteria.sorts:
            field = getattr(model, sort_condition.field_name())
            if sort_condition.is_ascending():
                order_by_clauses.append(field.asc())
            else:
                order_by_clauses.append(field.desc())

        return tuple(order_by_clauses)
