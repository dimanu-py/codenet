from src.social.user.domain.user import User
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_username_mother import UserUsernameMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother


class UserMother:
    @classmethod
    def any(cls) -> User:
        return User(
            id_=UserIdMother.any(),
            name=UserNameMother.any(),
            username=UserUsernameMother.any(),
            email=UserEmailMother.any(),
        )
