from sindripy.mothers import StringUuidPrimitivesMother


class AccountIdPrimitivesMother:
    @staticmethod
    def any() -> str:
        return StringUuidPrimitivesMother.any()
