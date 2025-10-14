from sindripy.mothers import ObjectMother

from src.social.user.domain.user_email import UserEmail


class UserEmailMother(ObjectMother):
    @classmethod
    def any(cls) -> UserEmail:
        return UserEmail(cls._faker().email())
