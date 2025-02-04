from dataclasses import dataclass


@dataclass(frozen=True)
class UserSignupCommand:
    id: str
    name: str
    username: str
    email: str
