from src.social.user.application.signup.user_signup_command import UserSignupCommand
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

    @staticmethod
    def from_signup_command(command: UserSignupCommand) -> User:
        return User(**command.to_primitives())

    @staticmethod
    def with_username(username: str) -> User:
        return User(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=username,
            email=UserEmailPrimitivesMother.any(),
        )

    @classmethod
    def create(cls, **overrides) -> User:
        default = cls.any().to_primitives()
        return User(**{**default, **overrides})
