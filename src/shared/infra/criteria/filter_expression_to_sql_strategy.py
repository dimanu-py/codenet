from abc import ABC, abstractmethod

from sqlalchemy.sql.elements import ColumnElement

from src.shared.infra.persistence.sqlalchemy.base import Base


class FilterExpressionToSqlStrategy(ABC):
    @abstractmethod
    def convert(self, model: type[Base], condition: Condition) -> ColumnElement[bool]:
        raise NotImplementedError
