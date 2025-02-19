from dataclasses import dataclass


@dataclass(frozen=True)
class UserSignupCommand:
    id: str
    name: str
    username: str
    email: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
        }
