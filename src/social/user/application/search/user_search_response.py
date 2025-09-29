from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class UserSearchResponse:
    users: list[dict]

    def dump(self) -> dict:
        return asdict(self)
