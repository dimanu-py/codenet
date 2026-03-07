from typing import Self

from sindripy.value_objects import List

from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.invalid_criteria import (
    MissingFieldInSortCondition,
    MissingDirectionInSortCondition,
    SortConditionInvalidStructure,
)
from src.shared.domain.criteria.sort_direction import SortDirection


class SortCondition:
    def __init__(self, field: Field, direction: SortDirection) -> None:
        self._field = field
        self._direction = direction

    @classmethod
    def from_primitives(cls, condition: dict[str, str]) -> Self:
        cls._ensure_condition_has_field_and_direction(condition)
        cls._ensure_condition_has_not_extra_keys(condition)
        return cls(
            field=Field(condition["field"]),
            direction=SortDirection(condition["direction"]),
        )

    def to_primitives(self) -> dict[str, str]:
        return {
            "field": self._field.value,
            "direction": self._direction.value,
        }

    @classmethod
    def _ensure_condition_has_field_and_direction(cls, condition: dict[str, str]) -> None:
        if "field" not in condition:
            raise MissingFieldInSortCondition()
        if "direction" not in condition:
            raise MissingDirectionInSortCondition()

    @classmethod
    def _ensure_condition_has_not_extra_keys(cls, condition: dict[str, str]) -> None:
        allowed_keys = {"field", "direction"}
        extra_keys = set(condition.keys()) - allowed_keys
        if extra_keys:
            raise SortConditionInvalidStructure()


class Sorts(List[SortCondition]):
    def __init__(self, conditions: list[SortCondition]) -> None:
        super().__init__(value=conditions)

    def is_not_empty(self) -> bool:
        return not len(self._value) == 0

    @classmethod
    def empty(cls) -> Self:
        return cls(conditions=[])

    def to_primitives(self) -> list[dict[str, str]]:
        return [condition.to_primitives() for condition in self._value]
