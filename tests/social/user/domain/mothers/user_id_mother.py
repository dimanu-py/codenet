from src.social.user.domain.user_id import UserId
from tests.shared.domain.value_objects.mothers.uuid_primitives_mother import (
    UuidPrimitivesMother,
)


class UserIdMother:
    @staticmethod
    def any() -> UserId:
        return UserId(UuidPrimitivesMother.any())
