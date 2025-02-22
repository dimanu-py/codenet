from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class UserSearchResponse:
    users: list[dict]

    def dump(self) -> dict:
        return asdict(self)
