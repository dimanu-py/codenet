import random

from src.shared.domain.criteria.filter_operator import FilterOperator


class FilterOperatorMother:
    @classmethod
    def any(cls) -> FilterOperator:
        random_operator = cls._generate_operator()
        return FilterOperator(random_operator)

    @staticmethod
    def _generate_operator() -> str:
        return random.choice(list(FilterOperator))
