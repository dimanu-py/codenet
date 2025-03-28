from dataclasses import dataclass


@dataclass(frozen=True)
class UserSignupRequest:
    name: str
    username: str
    email: str
