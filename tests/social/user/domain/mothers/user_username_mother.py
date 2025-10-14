from sindripy.mothers import ObjectMother

from src.social.user.domain.user_username import UserUsername


class UserUsernameMother(ObjectMother):
    @classmethod
    def any(cls) -> UserUsername:
        return UserUsername(cls._faker().user_name())
