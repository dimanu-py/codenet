from sqlalchemy.sql import select, Select

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter_operator import FilterOperator
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlAlchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> str:
        query = select(model)

        if criteria.is_empty():
            return self.stringify(query)

        for filter_ in criteria.filters:
            if filter_.operator_is(FilterOperator.EQUAL):
                primitives_filter = filter_.to_primitives()
                query = query.where(
                    getattr(model, primitives_filter["field"])
                    == primitives_filter["value"]
                )

        return self.stringify(query)

    @staticmethod
    def stringify(query: Select) -> str:
        return query.compile(compile_kwargs={"literal_binds": True}).string
