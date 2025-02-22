from sqlalchemy.sql import select

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlAlchemyConverter:
    @staticmethod
    def convert(model: type[Base], criteria: Criteria) -> str:
        query = select(model)
        return query.compile(compile_kwargs={"literal_binds": True}).string
