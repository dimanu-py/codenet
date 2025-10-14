from sindripy.mothers import ObjectMother

from src.social.user.domain.user_name import UserName


class UserNameMother(ObjectMother):
    @classmethod
    def any(cls) -> UserName:
        return UserName(cls._faker().name())
