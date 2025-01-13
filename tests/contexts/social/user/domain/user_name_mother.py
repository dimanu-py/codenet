from src.contexts.social.user.domain.user_name import UserName


class UserNameMother:
    @classmethod
    def create(cls) -> UserName:
        return UserName("john_doe")
