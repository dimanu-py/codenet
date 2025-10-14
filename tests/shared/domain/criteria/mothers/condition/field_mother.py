from sindripy.mothers import ObjectMother

from src.shared.domain.criteria.condition.field import Field


class FieldMother(ObjectMother):
    @classmethod
    def any(cls) -> Field:
        return Field(cls._faker().word())
