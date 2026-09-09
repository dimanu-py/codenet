from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter import Filter, Filters
from src.shared.domain.criteria.invalid_criteria import (
    InvalidCriteriaStructure,
    InvalidExpressionStructure,
)
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import ComparisonOperatorDoesNotExist, Operator
from src.shared.domain.criteria.sorts import Sorts


class FiltersToCriteriaConverter:
    @classmethod
    def convert(cls, filters: dict[str, Any], sorts: list[dict[str, str]] | None = None) -> Criteria:
        criteria = cls._parse_filters(filters) if filters else Criteria.empty()
        criteria.sorts = Sorts.from_primitives(sorts) if sorts else Sorts.empty()
        return criteria

    @classmethod
    def _parse_filters(cls, filters: dict[str, Any]) -> Criteria:
        cls._ensure_filters_have_valid_structure(filters)
        if cls._is_composite(filters):
            return cls._parse_composite(filters)
        if cls._is_comparison(filters):
            return cls._parse_comparison(filters)
        raise InvalidExpressionStructure()

    @classmethod
    def _parse_composite(cls, filters: dict[str, Any]) -> Criteria:
        logical_operator = LogicalOperator.AND if LogicalOperator.AND in filters else LogicalOperator.OR
        conditions = [cls._parse_filters(condition) for condition in filters[logical_operator]]

        combined = conditions[0]
        for condition in conditions[1:]:
            combined = combined & condition if logical_operator == LogicalOperator.AND else combined | condition
        return combined

    @classmethod
    def _parse_comparison(cls, filters: dict[str, Any]) -> Criteria:
        raw_operator = next((key for key in filters if key in Operator), None)
        if raw_operator is None:
            raise ComparisonOperatorDoesNotExist()

        return Criteria(
            filters=Filters(
                [
                    Filter(
                        field=filters["field"],
                        operator=Operator(raw_operator),
                        value=filters[Operator(raw_operator)],
                    )
                ]
            )
        )

    @classmethod
    def _is_composite(cls, filters: dict[str, Any]) -> bool:
        return LogicalOperator.AND in filters or LogicalOperator.OR in filters

    @classmethod
    def _is_comparison(cls, filters: dict[str, Any]) -> bool:
        return "field" in filters

    @classmethod
    def _ensure_filters_have_valid_structure(cls, filters: dict[str, Any]) -> None:
        if not isinstance(filters, dict):
            raise InvalidCriteriaStructure()
