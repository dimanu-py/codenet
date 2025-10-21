from sindripy.mothers import ObjectMother


class UserPasswordPrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().password()
