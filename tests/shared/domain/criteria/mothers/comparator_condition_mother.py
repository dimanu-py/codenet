from src.shared.domain.criteria.comparator_condition import (
    ComparatorCondition,
)
from tests.shared.domain.criteria.mothers.field_mother import FieldMother
from tests.shared.domain.criteria.mothers.operator_mother import (
    OperatorMother,
)
from tests.shared.domain.criteria.mothers.value_mother import ValueMother


class ComparatorConditionMother:
    @staticmethod
    def any() -> ComparatorCondition:
        return ComparatorCondition(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )
