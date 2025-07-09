from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SearchUserQuery:
    filters: dict[str, Any]
