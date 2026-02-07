from sindripy.mothers import ObjectMother


class UserUsernamePrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().user_name()
