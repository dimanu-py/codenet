from typing import Any, override

from src.shared.domain.criteria.filter import Filters
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.sorts import Sorts


class Criteria:
    def __init__(self, filters: Filters, sorts: Sorts | None = None) -> None:
        self.filters = filters
        self.sorts = sorts or Sorts.empty()

    @classmethod
    def empty(cls) -> "Criteria":
        return cls(
            filters=Filters.empty(),
            sorts=Sorts.empty(),
        )

    def has_filters(self) -> bool:
        return self.filters.has_filters()

    def has_sorting(self) -> bool:
        return self.sorts.has_sorting()

    def __and__(self, other: "Criteria") -> "AndCriteria":
        return AndCriteria(self, other)

    def __or__(self, other: "Criteria") -> "OrCriteria":
        return OrCriteria(self, other)

    def _filters_to_primitives(self) -> dict[str, Any]:
        return self.filters.to_primitives()

    def to_primitives(self) -> dict[str, Any]:
        return {
            "filters": self._filters_to_primitives(),
            "sorts": self.sorts.to_primitives(),
        }

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Criteria) and self.to_primitives() == other.to_primitives()


class AndCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria) -> None:
        super().__init__(filters=Filters.empty())
        self.left = left
        self.right = right

    @override
    def has_filters(self) -> bool:
        return self.left.has_filters() and self.right.has_filters()

    @override
    def _filters_to_primitives(self) -> dict[str, Any]:
        return {LogicalOperator.AND: [self.left._filters_to_primitives(), self.right._filters_to_primitives()]}


class OrCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria) -> None:
        super().__init__(filters=Filters.empty())
        self.left = left
        self.right = right

    @override
    def has_filters(self) -> bool:
        return self.left.has_filters() and self.right.has_filters()

    @override
    def _filters_to_primitives(self) -> dict[str, Any]:
        return {LogicalOperator.OR: [self.left._filters_to_primitives(), self.right._filters_to_primitives()]}
