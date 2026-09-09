import pytest
from expects import be_false, be_true, equal, expect

from src.shared.domain.criteria.criteria import AndCriteria, Criteria, OrCriteria
from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.filter import Filter, Filters
from src.shared.domain.criteria.operator import Operator
from src.shared.domain.criteria.sort_direction import SortDirection
from src.shared.domain.criteria.sorts import SortCondition, Sorts


@pytest.mark.unit
class TestCriteria:
    def test_should_create_empty_criteria_by_default(self) -> None:
        criteria = Criteria.empty()

        expect(criteria.has_filters()).to(be_false)

    def test_should_create_criteria_with_filters(self) -> None:
        criteria = Criteria(filters=Filters([Filter(field="status", operator=Operator.EQUALS, value="active")]))

        expect(criteria.has_filters()).to(be_true)

    def test_should_create_criteria_without_sorting_by_default(self) -> None:
        criteria = Criteria.empty()

        expect(criteria.has_sorting()).to(be_false)

    def test_should_create_criteria_with_sorting(self) -> None:
        criteria = Criteria(
            filters=Filters.empty(),
            sorts=Sorts([SortCondition(field=Field("age"), direction=SortDirection.ASCENDING)]),
        )

        expect(criteria.has_sorting()).to(be_true)

    def test_should_combine_two_criteria_with_and_operator(self) -> None:
        is_active = Criteria(filters=Filters([Filter(field="status", operator=Operator.EQUALS, value="active")]))
        is_adult = Criteria(
            filters=Filters([Filter(field="age", operator=Operator.GREATER_THAN_OR_EQUAL_TO, value="18")])
        )

        combined = is_active & is_adult

        expect(isinstance(combined, AndCriteria)).to(be_true)
        expect(combined.has_filters()).to(be_true)
        expect(combined.to_primitives()).to(
            equal(
                {
                    "filters": {
                        "and": [
                            {"field": "status", "equals": "active"},
                            {"field": "age", "greater_or_equal_to": "18"},
                        ]
                    },
                    "sorts": [],
                }
            )
        )

    def test_should_combine_two_criteria_with_or_operator(self) -> None:
        is_gmail = Criteria(filters=Filters([Filter(field="email", operator=Operator.CONTAINS, value="@gmail.com")]))
        is_yahoo = Criteria(filters=Filters([Filter(field="email", operator=Operator.CONTAINS, value="@yahoo.com")]))

        combined = is_gmail | is_yahoo

        expect(isinstance(combined, OrCriteria)).to(be_true)
        expect(combined.has_filters()).to(be_true)
        expect(combined.to_primitives()).to(
            equal(
                {
                    "filters": {
                        "or": [
                            {"field": "email", "contains": "@gmail.com"},
                            {"field": "email", "contains": "@yahoo.com"},
                        ]
                    },
                    "sorts": [],
                }
            )
        )

    def test_should_support_nested_composition(self) -> None:
        is_adult = Criteria(
            filters=Filters([Filter(field="age", operator=Operator.GREATER_THAN_OR_EQUAL_TO, value="18")])
        )
        is_gmail = Criteria(filters=Filters([Filter(field="email", operator=Operator.CONTAINS, value="@gmail.com")]))
        is_yahoo = Criteria(filters=Filters([Filter(field="email", operator=Operator.CONTAINS, value="@yahoo.com")]))

        combined = is_adult & (is_gmail | is_yahoo)

        expect(isinstance(combined, AndCriteria)).to(be_true)
        expect(isinstance(combined.right, OrCriteria)).to(be_true)
        expect(combined.to_primitives()).to(
            equal(
                {
                    "filters": {
                        "and": [
                            {"field": "age", "greater_or_equal_to": "18"},
                            {
                                "or": [
                                    {"field": "email", "contains": "@gmail.com"},
                                    {"field": "email", "contains": "@yahoo.com"},
                                ]
                            },
                        ]
                    },
                    "sorts": [],
                }
            )
        )

    def test_two_criteria_with_same_filters_and_sorts_are_equal(self) -> None:
        first = Criteria(filters=Filters([Filter(field="status", operator=Operator.EQUALS, value="active")]))
        second = Criteria(filters=Filters([Filter(field="status", operator=Operator.EQUALS, value="active")]))

        expect(first).to(equal(second))
