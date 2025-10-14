from sindripy.mothers import ObjectMother

from src.shared.domain.criteria.condition.value import Value


class ValueMother(ObjectMother):
    @classmethod
    def any(cls) -> Value:
        return Value(cls._faker().word())
