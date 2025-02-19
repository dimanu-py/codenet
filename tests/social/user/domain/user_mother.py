from src.social.user.domain.user import User
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


class UserMother:
    @classmethod
    def any(cls) -> User:
        return User(
            id_=UserIdMother.any(),
            name=UserNameMother.any(),
            username=UserUsernameMother.any(),
            email=UserEmailMother.any(),
        )

    @classmethod
    def create(cls, fixed_values: dict) -> User:
        primitives = {
            "id_": UserIdMother.any().value,
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        primitives.update(fixed_values)

        return User.signup(**primitives)
