from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user import UserPrimitives
from tests.social.user.domain.mothers.user_email_primitives_mother import UserEmailPrimitivesMother
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_password_primitives_mother import UserPasswordPrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


class UserPrimitivesMother:
    @staticmethod
    def any() -> UserPrimitives:
        return UserPrimitives(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
            password=UserPasswordPrimitivesMother.any(),
        )

    @staticmethod
    def from_signup_command(command: UserSignupCommand) -> UserPrimitives:
        return UserPrimitives(**command.to_primitives())

    @staticmethod
    def with_username(username: str) -> UserPrimitives:
        return UserPrimitives(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=username,
            email=UserEmailPrimitivesMother.any(),
            password=UserPasswordPrimitivesMother.any(),
        )
