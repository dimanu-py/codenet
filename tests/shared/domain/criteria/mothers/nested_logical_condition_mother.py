from src.shared.domain.criteria.logical_group import (
    LogicalGroup,
)
from tests.shared.domain.criteria.mothers.comparator_condition_mother import (
    ComparatorConditionMother,
)
from tests.shared.domain.criteria.mothers.logical_operator_mother import (
    LogicalOperatorMother,
)


class NestedLogicalConditionMother:
    @staticmethod
    def any() -> LogicalGroup:
        return LogicalGroup(
            operator=LogicalOperatorMother.any(),
            conditions=[ComparatorConditionMother.any()],
        )

    @staticmethod
    def empty() -> LogicalGroup:
        return LogicalGroup(operator=LogicalOperatorMother.any(), conditions=[])
