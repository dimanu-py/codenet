from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserRequest:
    name: str
    username: str
    email: str
    profile_picture: str
