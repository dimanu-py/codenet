from src.social.user.application.signup.user_signup_command import UserSignupCommand
from tests.social.user.domain.mothers.user_email_primitives_mother import UserEmailPrimitivesMother
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_password_primitives_mother import UserPasswordPrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


class UserSignupCommandMother:
    @staticmethod
    def any() -> UserSignupCommand:
        return UserSignupCommand(
            id=UserIdPrimitivesMother.any(),
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
            password=UserPasswordPrimitivesMother.any(),
        )
