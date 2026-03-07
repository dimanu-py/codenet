from src.shared.domain.criteria.sorts import Sorts


class SortsMother:
    @staticmethod
    def empty() -> Sorts:
        return Sorts(conditions=[])
