from src.shared.domain.criteria.filter_field import FilterField
from src.shared.domain.criteria.filter_operator import FilterOperator
from src.shared.domain.criteria.filter_value import FilterValue


class Filter:
    _value: FilterValue
    _operator: FilterOperator
    _field: FilterField

    def __init__(
        self, field: FilterField, operator: FilterOperator, value: FilterValue
    ) -> None:
        self._field = field
        self._operator = operator
        self._value = value

    @classmethod
    def from_primitives(cls, field: str, operator: str, value: str) -> "Filter":
        return Filter(
            field=FilterField(field),
            operator=FilterOperator(operator),
            value=FilterValue(value),
        )

    def to_primitives(self) -> dict[str, str]:
        return {
            "field": self._field.value,
            "operator": self._operator.value,
            "value": self._value.value,
        }

    def operator_is(self, operator: FilterOperator) -> bool:
        return self._operator == operator
