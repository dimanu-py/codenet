from src.shared.domain.criteria.condition.comparator_condition import ComparatorCondition
from tests.social.shared.domain.criteria.condition.field_mother import FieldMother
from tests.social.shared.domain.criteria.condition.operator_mother import (
    OperatorMother,
)
from tests.social.shared.domain.criteria.condition.value_mother import ValueMother


class ComparatorConditionMother:
    @staticmethod
    def any() -> ComparatorCondition:
        return ComparatorCondition(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )
