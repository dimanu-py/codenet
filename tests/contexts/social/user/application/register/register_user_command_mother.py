from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)


class RegisterUserCommandMother:
    @classmethod
    def create(cls, fixed_values: dict | None = None) -> RegisterUserCommand:
        primitives = {
            "id": "8a97585f-4d7a-42ba-8d82-ab8da94d2c4a",
            "name": "John Doe",
            "username": "john_doe",
            "email": "johndoe@gmail.com",
            "profile_picture": "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
            **(fixed_values if fixed_values else {}),
        }
        return RegisterUserCommand(**primitives)
