from src.contexts.social.user.domain.user_email import UserEmail


class UserEmailMother:
    @classmethod
    def create(cls) -> UserEmail:
        return UserEmail("johndoe@gmail.com")
