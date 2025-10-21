from sindripy.mothers import ObjectMother


class UserEmailPrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().email()
