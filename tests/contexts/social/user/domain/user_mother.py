from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_email import UserEmail
from src.contexts.social.user.domain.user_full_name import UserFullName
from src.contexts.social.user.domain.user_id import UserId
from src.contexts.social.user.domain.user_name import UserName
from src.contexts.social.user.domain.user_profile_picture import UserProfilePicture


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
            id_=UserId("1f322ec7-a36c-44e2-b339-71b966f95a99"),
            name=UserFullName("John Doe"),
            username=UserName("john_doe"),
            email=UserEmail("johndoe@gmail.com"),
            profile_picture=UserProfilePicture(
                "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg"
            ),
        )
