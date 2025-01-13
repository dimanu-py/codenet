from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.domain.user import User
from tests.contexts.social.user.domain.user_email_mother import UserEmailMother
from tests.contexts.social.user.domain.user_name_mother import UserNameMother
from tests.contexts.social.user.domain.user_id_mother import UserIdMother
from tests.contexts.social.user.domain.user_username_mother import UserUsernameMother
from tests.contexts.social.user.domain.user_profile_picture_mother import (
    UserProfilePictureMother,
)


class UserMother:
    @classmethod
    def from_command(cls, command: RegisterUserCommand) -> User:
        return User.create(
            id_=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
            profile_picture=command.profile_picture,
        )

    @classmethod
    def create(cls) -> User:
        return User(
            id_=UserIdMother.create(),
            name=UserNameMother.create(),
            username=UserUsernameMother.create(),
            email=UserEmailMother.create(),
            profile_picture=UserProfilePictureMother.create(),
        )
