from src.contexts.social.user.domain.user_id import UserId


class UserIdMother:
    @classmethod
    def create(cls) -> UserId:
        return UserId("1f322ec7-a36c-44e2-b339-71b966f95a99")
