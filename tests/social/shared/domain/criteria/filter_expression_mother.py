from src.shared.domain.criteria.filter_expression import FilterExpression
from tests.social.shared.domain.criteria.condition.comparator_condition_mother import (
	ComparatorConditionMother,
)
from tests.social.shared.domain.criteria.logical_operator_mother import (
    LogicalOperatorMother,
)


class FilterExpressionMother:
    @staticmethod
    def any() -> FilterExpression:
        return FilterExpression(
            operator=LogicalOperatorMother.any(),
            conditions=[ComparatorConditionMother.any()],
        )

    @staticmethod
    def empty() -> FilterExpression:
        return FilterExpression(operator=LogicalOperatorMother.any(), conditions=[])
