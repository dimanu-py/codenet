from dataclasses import dataclass


@dataclass(frozen=True)
class SearchUserQuery:
    filters: list[dict]
