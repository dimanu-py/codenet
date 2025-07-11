import random

from src.shared.domain.criteria.condition.logical_operator import LogicalOperator


class LogicalOperatorMother:
    @classmethod
    def any(cls) -> LogicalOperator:
        random_operator = cls._generate_aggregation()
        return LogicalOperator(random_operator)

    @staticmethod
    def _generate_aggregation() -> str:
        return random.choice(list(LogicalOperator))
