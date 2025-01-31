from src.social.user.domain.user import User


class UserMother:
    @classmethod
    def any(cls) -> User:
        return User(
            id_="2827970f-4848-48a2-abd2-aa8f205b295a",
            name="Dimanu",
            username="dimanu",
            email="dimanu@py.com",
        )
