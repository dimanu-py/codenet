from src.social.user.domain.user import User
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


class UserMother:
    @staticmethod
    def any() -> User:
        return User(
            id=UserIdMother.any(),
            name=UserNameMother.any(),
            username=UserUsernameMother.any(),
            email=UserEmailMother.any(),
        )

    @staticmethod
    def create(fixed_values: dict) -> User:
        primitives = {
            "id": UserIdMother.any().value,
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        primitives.update(fixed_values)

        return User.signup(**primitives)
