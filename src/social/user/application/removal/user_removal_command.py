from dataclasses import dataclass


@dataclass(frozen=True)
class UserRemovalCommand:
    username: str

    def to_primitives(self) -> dict[str, str]:
        return {"username": self.username}
