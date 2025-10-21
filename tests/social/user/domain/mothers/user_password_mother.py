from sindripy.mothers import ObjectMother

from src.social.user.domain.user_password import UserPassword


class UserPasswordMother(ObjectMother):
    @classmethod
    def any(cls) -> UserPassword:
        return UserPassword.from_plain_text(cls._faker().password())
