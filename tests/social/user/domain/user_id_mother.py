from src.social.user.domain.user_id import UserId
from tests.shared.domain.random_generator import RandomGenerator
from tests.shared.domain.value_objects.uuid_primitives_mother import (
    UuidPrimitivesMother,
)


class UserIdMother:
    @staticmethod
    def any() -> UserId:
        return UserId(UuidPrimitivesMother.any())
