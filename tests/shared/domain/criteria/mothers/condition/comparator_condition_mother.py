from src.shared.domain.criteria.condition.comparator_condition import (
    ComparatorCondition,
)
from tests.shared.domain.criteria.mothers.condition.field_mother import FieldMother
from tests.shared.domain.criteria.mothers.condition.operator_mother import (
    OperatorMother,
)
from tests.shared.domain.criteria.mothers.condition.value_mother import ValueMother


class ComparatorConditionMother:
    @staticmethod
    def any() -> ComparatorCondition:
        return ComparatorCondition(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )
