from src.contexts.social.user.domain.user_profile_picture import UserProfilePicture
from tests.contexts.shared.domain.random_generator import RandomGenerator


class UserProfilePictureMother:
    @classmethod
    def create(cls) -> UserProfilePicture:
        return UserProfilePicture(f"{RandomGenerator.url()}.jpg")
