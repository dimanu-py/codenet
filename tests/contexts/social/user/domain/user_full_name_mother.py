from src.contexts.social.user.domain.user_full_name import UserFullName


class UserFullNameMother:
    @classmethod
    def create(cls) -> UserFullName:
        return UserFullName("John Doe")
