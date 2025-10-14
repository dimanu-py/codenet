from sindripy.mothers import StringUuidPrimitivesMother

from src.social.user.domain.user_id import UserId


class UserIdMother:
    @staticmethod
    def any() -> UserId:
        return UserId(StringUuidPrimitivesMother.any())
