from src.social.user.application.signup.user_signup_command import UserSignupCommand
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


class UserSignupCommandMother:
    @staticmethod
    def any() -> UserSignupCommand:
        return UserSignupCommand(
            id=UserIdMother.any().value,
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )

    @staticmethod
    def invalid(**overrides) -> UserSignupCommand:
        defaults = {
            "id": UserIdMother.any().value,
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        defaults.update(overrides)
        return UserSignupCommand(**defaults)
