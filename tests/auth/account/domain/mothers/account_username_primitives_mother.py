from sindripy.mothers import ObjectMother


class AccountUsernamePrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().user_name()
