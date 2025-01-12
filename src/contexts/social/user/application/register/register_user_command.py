from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class RegisterUserCommand:
    id: str
    name: str
    username: str
    email: str
    profile_picture: str
