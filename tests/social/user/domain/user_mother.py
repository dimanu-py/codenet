from src.social.user.domain.user import User
from tests.social.user.domain.user_id_mother import UserIdMother


class UserMother:
    @classmethod
    def any(cls) -> User:
        return User(
            id_=UserIdMother.any(),
            name="Dimanu",
            username="dimanu",
            email="dimanu@py.com",
        )
