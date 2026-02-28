from src.shared.domain.criteria.expression import Comparison, LogicalGroup
from tests.shared.domain.criteria.mothers.field_mother import FieldMother
from tests.shared.domain.criteria.mothers.logical_operator_mother import LogicalOperatorMother
from tests.shared.domain.criteria.mothers.operator_mother import OperatorMother
from tests.shared.domain.criteria.mothers.value_mother import ValueMother


class ComparisonMother:
    @staticmethod
    def any() -> Comparison:
        return Comparison(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )


class LogicalGroupMother:
    @staticmethod
    def any() -> LogicalGroup:
        return LogicalGroup(
            operator=LogicalOperatorMother.any(),
            conditions=[ComparisonMother.any()],
        )
