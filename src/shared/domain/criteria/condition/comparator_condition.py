from typing import Self

from src.shared.domain.criteria.condition.field import Field
from src.shared.domain.criteria.condition.operator import Operator
from src.shared.domain.criteria.condition.value import Value


class ComparatorCondition:
    _value: Value
    _operator: Operator
    _field: Field

    def __init__(self, field: str, operator: str, value: str) -> None:
        self._field = Field(field)
        self._operator = Operator(operator)
        self._value = Value(value)

    @classmethod
    def from_primitives(cls, condition: dict) -> Self:
        operator = Operator(list(condition.keys())[-1])
        return cls(
            field=condition["field"],
            operator=operator,
            value=condition[operator],
        )

    def to_primitives(self) -> dict[str, str]:
        return {
            "field": self._field.value,
            f"{self._operator.value}": self._value.value,
        }

    def operator_is(self, operator: Operator) -> bool:
        return self._operator == operator
