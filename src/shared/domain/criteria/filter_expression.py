from typing import Any, Self

from src.shared.domain.criteria.condition.comparator_condition import ComparatorCondition
from src.shared.domain.criteria.logical_operator import LogicalOperator


class FilterExpression:
    _logical_operator: LogicalOperator
    _conditions: list["ComparatorCondition | FilterExpression"]

    def __init__(
        self,
        operator: LogicalOperator,
        conditions: list["ComparatorCondition | FilterExpression"],
    ) -> None:
        self._logical_operator = operator
        self._conditions = conditions

    @classmethod
    def from_primitives(cls, data: dict[str, Any]) -> "ComparatorCondition | FilterExpression":
        if LogicalOperator.AND in data:
            conditions = [
                cls.from_primitives(item) for item in data[LogicalOperator.AND]
            ]
            return cls(operator=LogicalOperator.AND, conditions=conditions)
        if LogicalOperator.OR in data:
            conditions = [
                cls.from_primitives(item) for item in data[LogicalOperator.OR]
            ]
            return cls(operator=LogicalOperator.OR, conditions=conditions)
        return ComparatorCondition.from_primitives(data)

    @classmethod
    def empty(cls) -> Self:
        return cls(operator=LogicalOperator.AND, conditions=[])

    def has_and_logical_operator(self) -> bool:
        return self._logical_operator == LogicalOperator.AND

    def to_primitives(self) -> dict[str, Any]:
        key = (
            LogicalOperator.AND
            if self._logical_operator is LogicalOperator.AND
            else LogicalOperator.OR
        )
        return {key: [item.to_primitives() for item in self._conditions]}

    def is_empty(self) -> bool:
        return len(self._conditions) == 0
