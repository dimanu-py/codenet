from src.contexts.social.user.domain.user_profile_picture import UserProfilePicture


class UserProfilePictureMother:
    @classmethod
    def create(cls) -> UserProfilePicture:
        return UserProfilePicture(
            "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg"
        )
