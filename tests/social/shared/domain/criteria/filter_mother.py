from src.shared.domain.criteria.filter import Filter
from tests.social.shared.domain.criteria.filter_field_mother import FilterFieldMother
from tests.social.shared.domain.criteria.filter_operator_mother import (
    FilterOperatorMother,
)
from tests.social.shared.domain.criteria.filter_value_mother import FilterValueMother


class FilterMother:
    @classmethod
    def any(cls) -> Filter:
        return Filter(
            field=FilterFieldMother.any(),
            operator=FilterOperatorMother.any(),
            value=FilterValueMother.any(),
        )
