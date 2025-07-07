from dataclasses import dataclass


@dataclass(frozen=True)
class UserRemovalCommand:
    user_id: str

    def to_primitives(self) -> dict[str, str]:
        return {"user_id": self.user_id}
