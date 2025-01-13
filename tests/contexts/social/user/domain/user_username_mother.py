from src.contexts.social.user.domain.user_username import UserUsername


class UserUsernameMother:
    @classmethod
    def create(cls) -> UserUsername:
        return UserUsername("john_doe")
