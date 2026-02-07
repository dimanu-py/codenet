from src.backoffice.user.domain.user import User
from tests.backoffice.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.backoffice.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


class UserMother:
    @staticmethod
    def any() -> User:
        return User(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
        )

    @classmethod
    def create(cls, **overrides) -> User:
        default = cls.any().to_primitives()
        return User(**{**default, **overrides})

    @classmethod
    def with_username(cls, username: str) -> User:
        return cls.create(username=username)

    @classmethod
    def create(cls, **overrides) -> User:
        default = cls.any().to_primitives()
        return User(**{**default, **overrides})
