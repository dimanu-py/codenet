import random

from src.shared.domain.criteria.sort_direction import SortDirection


class SortDirectionMother:
    _OPTIONS = ["ascending", "descending"]

    @classmethod
    def any(cls) -> SortDirection:
        return SortDirection(random.choice(cls._OPTIONS))
