from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.persistence.sqlalchemy.base import Base


class CriteriaToSqlAlchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> str:
        raise NotImplementedError
