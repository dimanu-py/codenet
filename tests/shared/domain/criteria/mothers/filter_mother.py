from src.shared.domain.criteria.filter import Filter
from tests.shared.domain.criteria.mothers.field_mother import FieldMother
from tests.shared.domain.criteria.mothers.operator_mother import OperatorMother
from tests.shared.domain.criteria.mothers.value_mother import ValueMother


class FilterMother:
    @staticmethod
    def any() -> Filter:
        return Filter(
            field=FieldMother.any().value,
            operator=OperatorMother.any(),
            value=ValueMother.any().value,
        )
