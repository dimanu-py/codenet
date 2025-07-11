from src.shared.domain.criteria.nested_logical_condition import NestedLogicalCondition
from tests.social.shared.domain.criteria.condition.comparator_condition_mother import (
	ComparatorConditionMother,
)
from tests.social.shared.domain.criteria.logical_operator_mother import (
    LogicalOperatorMother,
)


class NestedLogicalConditionMother:
    @staticmethod
    def any() -> NestedLogicalCondition:
        return NestedLogicalCondition(
            operator=LogicalOperatorMother.any(),
            conditions=[ComparatorConditionMother.any()],
        )

    @staticmethod
    def empty() -> NestedLogicalCondition:
        return NestedLogicalCondition(operator=LogicalOperatorMother.any(), conditions=[])
