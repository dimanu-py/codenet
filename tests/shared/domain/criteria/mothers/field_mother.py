from sindripy.mothers import ObjectMother

from src.shared.domain.criteria.field import Field


class FieldMother(ObjectMother):
    @classmethod
    def any(cls) -> Field:
        return Field(cls._faker().word())
