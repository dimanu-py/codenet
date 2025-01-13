from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from tests.contexts.social.user.domain.user_email_mother import UserEmailMother
from tests.contexts.social.user.domain.user_name_mother import UserNameMother
from tests.contexts.social.user.domain.user_id_mother import UserIdMother
from tests.contexts.social.user.domain.user_username_mother import UserUsernameMother
from tests.contexts.social.user.domain.user_profile_picture_mother import (
    UserProfilePictureMother,
)


class RegisterUserCommandMother:
    @classmethod
    def create(cls, fixed_values: dict | None = None) -> RegisterUserCommand:
        primitives = {
            "id": UserIdMother.create().value,
            "name": UserNameMother.create().value,
            "username": UserUsernameMother.create().value,
            "email": UserEmailMother.create().value,
            "profile_picture": UserProfilePictureMother.create().value,
            **(fixed_values if fixed_values else {}),
        }
        return RegisterUserCommand(**primitives)
