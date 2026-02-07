from sindripy.mothers import ObjectMother


class AccountEmailPrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().email()
