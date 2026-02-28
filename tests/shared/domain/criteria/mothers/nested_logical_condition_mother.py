from src.shared.domain.criteria.nested_logical_condition import (
    NestedLogicalCondition,
)
from tests.shared.domain.criteria.mothers.comparator_condition_mother import (
    ComparatorConditionMother,
)
from tests.shared.domain.criteria.mothers.logical_operator_mother import (
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
