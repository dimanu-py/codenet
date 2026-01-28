from dataclasses import dataclass


@dataclass(frozen=True)
class UserSignupCommand:
    id: str
    name: str
    username: str
    email: str
    password: str

    def to_primitives(self) -> dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }
