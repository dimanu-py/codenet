from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user import User
from tests.social.user.domain.mother.user_email_mother import UserEmailMother
from tests.social.user.domain.mother.user_id_mother import UserIdMother
from tests.social.user.domain.mother.user_name_mother import UserNameMother
from tests.social.user.domain.mother.user_username_mother import UserUsernameMother


class UserMother:
    @staticmethod
    def any() -> User:
        return User(
            id=UserIdMother.any().value,
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )

    @staticmethod
    def from_signup_command(command: UserSignupCommand) -> User:
        return User(**command.to_primitives())
