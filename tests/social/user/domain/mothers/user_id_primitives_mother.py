from sindripy.mothers import StringUuidPrimitivesMother


class UserIdPrimitivesMother:
    @staticmethod
    def any() -> str:
        return StringUuidPrimitivesMother.any()
