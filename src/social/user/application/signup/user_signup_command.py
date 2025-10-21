from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserSignupCommand:
    id: str
    name: str
    username: str
    email: str
    password: str = field(default="")

    def to_primitives(self) -> dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
        }
