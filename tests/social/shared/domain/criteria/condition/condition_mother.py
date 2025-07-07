from src.shared.domain.criteria.condition.condition import Condition
from tests.social.shared.domain.criteria.condition.field_mother import FieldMother
from tests.social.shared.domain.criteria.condition.operator_mother import (
    OperatorMother,
)
from tests.social.shared.domain.criteria.condition.value_mother import ValueMother


class ConditionMother:
    @staticmethod
    def any() -> Condition:
        return Condition(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )
