import random

from src.shared.domain.criteria.condition.operator import Operator


class OperatorMother:
    @classmethod
    def any(cls) -> Operator:
        random_operator = cls._generate_operator()
        return Operator(random_operator)

    @staticmethod
    def _generate_operator() -> str:
        return random.choice(list(Operator))
