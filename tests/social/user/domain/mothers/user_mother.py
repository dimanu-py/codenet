from src.social.user.domain.user import User
from tests.social.user.domain.mothers.user_email_primitives_mother import UserEmailPrimitivesMother
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


class UserMother:
    @staticmethod
    def any() -> User:
        return User(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )

    @classmethod
    def with_username(cls, username: str) -> User:
        return cls.create(username=username)

    @classmethod
    def create(cls, **overrides) -> User:
        default = cls.any().to_primitives()
        return User(**{**default, **overrides})
