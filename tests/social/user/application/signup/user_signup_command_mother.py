from src.social.user.application.signup.user_signup_command import UserSignupCommand
from tests.social.user.domain.mother.user_email_mother import UserEmailMother
from tests.social.user.domain.mother.user_id_mother import UserIdMother
from tests.social.user.domain.mother.user_name_mother import UserNameMother
from tests.social.user.domain.mother.user_username_mother import UserUsernameMother


class UserSignupCommandMother:
    @staticmethod
    def any() -> UserSignupCommand:
        return UserSignupCommand(
            id=UserIdMother.any().value,
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )

    @classmethod
    def invalid(cls, **overrides) -> UserSignupCommand:
        defaults = cls.any().to_primitives()
        defaults.update(overrides)
        return UserSignupCommand(**defaults)
