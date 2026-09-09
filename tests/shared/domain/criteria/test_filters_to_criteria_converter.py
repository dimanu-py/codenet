import pytest
from expects import be_false, be_true, equal, expect, raise_error

from src.shared.domain.criteria.criteria import AndCriteria, Criteria, OrCriteria
from src.shared.domain.criteria.filters_to_criteria_converter import FiltersToCriteriaConverter
from src.shared.domain.criteria.invalid_criteria import (
    InvalidCriteriaStructure,
    InvalidExpressionStructure,
    MissingDirectionInSortCondition,
    MissingFieldInSortCondition,
    SortConditionInvalidStructure,
)
from src.shared.domain.criteria.operator import ComparisonOperatorDoesNotExist, Operator
from src.shared.domain.criteria.sort_direction import SortDirectionDoesNotExist


@pytest.mark.unit
class TestFiltersToCriteriaConverter:
    def test_should_create_empty_criteria(self) -> None:
        empty_criteria = FiltersToCriteriaConverter.convert(filters={})

        expect(empty_criteria.has_filters()).to(be_false)

    def test_should_create_criteria_from_comparison_filters(self) -> None:
        criteria = FiltersToCriteriaConverter.convert(filters={"field": "age", Operator.GREATER_THAN: "30"})

        expect(criteria.has_filters()).to(be_true)
        expect(isinstance(criteria, Criteria)).to(be_true)

    def test_should_create_and_criteria_from_and_filters(self) -> None:
        criteria = FiltersToCriteriaConverter.convert(
            filters={"and": [{"field": "age", Operator.EQUALS: "30"}, {"field": "name", Operator.EQUALS: "John"}]}
        )

        expect(criteria.has_filters()).to(be_true)
        expect(isinstance(criteria, AndCriteria)).to(be_true)

    def test_should_create_or_criteria_from_or_filters(self) -> None:
        criteria = FiltersToCriteriaConverter.convert(
            filters={"or": [{"field": "age", Operator.EQUALS: "30"}, {"field": "name", Operator.EQUALS: "John"}]}
        )

        expect(criteria.has_filters()).to(be_true)
        expect(isinstance(criteria, OrCriteria)).to(be_true)

    def test_should_combine_more_than_two_conditions_in_a_logical_group(self) -> None:
        criteria = FiltersToCriteriaConverter.convert(
            filters={
                "and": [
                    {"field": "age", Operator.EQUALS: "30"},
                    {"field": "name", Operator.EQUALS: "John"},
                    {"field": "status", Operator.EQUALS: "active"},
                ]
            }
        )

        expect(criteria.to_primitives()["filters"]).to(
            equal(
                {
                    "and": [
                        {
                            "and": [
                                {"field": "age", "equals": "30"},
                                {"field": "name", "equals": "John"},
                            ]
                        },
                        {"field": "status", "equals": "active"},
                    ]
                }
            )
        )

    def test_should_create_criteria_without_sorting_by_default(self) -> None:
        criteria_without_sorts = FiltersToCriteriaConverter.convert(filters={})

        expect(criteria_without_sorts.has_sorting()).to(be_false)

    def test_should_create_criteria_with_empty_sorting(self) -> None:
        criteria_with_empty_sorts = FiltersToCriteriaConverter.convert(filters={}, sorts=[])

        expect(criteria_with_empty_sorts.has_sorting()).to(be_false)

    @pytest.mark.parametrize(
        "sorting",
        [
            pytest.param([{"field": "age", "direction": "ascending"}], id="single_sorting"),
            pytest.param(
                [{"field": "age", "direction": "ascending"}, {"field": "name", "direction": "descending"}],
                id="multiple_sorting",
            ),
        ],
    )
    def test_should_create_criteria_with_sorting(self, sorting: list[dict[str, str]]) -> None:
        criteria_with_sorts = FiltersToCriteriaConverter.convert(
            filters={"field": "age", Operator.EQUALS: "30"},
            sorts=sorting,
        )

        expect(criteria_with_sorts.has_sorting()).to(be_true)

    def test_should_fail_when_filters_is_not_a_dictionary(self) -> None:
        invalid_filters = "not_a_dictionary"

        expect(lambda: FiltersToCriteriaConverter.convert(filters=invalid_filters)).to(
            raise_error(InvalidCriteriaStructure)
        )

    def test_should_fail_when_filters_is_not_composite_nor_comparison(self) -> None:
        invalid_filters = {"invalid": "filters"}

        expect(lambda: FiltersToCriteriaConverter.convert(filters=invalid_filters)).to(
            raise_error(InvalidExpressionStructure)
        )

    def test_should_fail_when_condition_in_logical_group_does_not_have_valid_structure(self) -> None:
        invalid_and_filters = {
            "and": [
                {"field": "age", Operator.EQUALS: "30"},
                {"invalid": "condition"},
            ]
        }

        expect(lambda: FiltersToCriteriaConverter.convert(filters=invalid_and_filters)).to(
            raise_error(InvalidExpressionStructure)
        )

    def test_should_fail_when_passing_non_existing_operator(self) -> None:
        filters_with_non_existing_operator = {"field": "age", "multiplication": "30"}

        expect(lambda: FiltersToCriteriaConverter.convert(filters=filters_with_non_existing_operator)).to(
            raise_error(ComparisonOperatorDoesNotExist)
        )

    def test_should_fail_when_sorting_has_missing_field(self) -> None:
        sorting_with_missing_field = [{"direction": "ascending"}]

        expect(lambda: FiltersToCriteriaConverter.convert(filters={}, sorts=sorting_with_missing_field)).to(
            raise_error(MissingFieldInSortCondition)
        )

    def test_should_fail_when_sorting_has_missing_direction(self) -> None:
        sorting_with_missing_direction = [{"field": "age"}]

        expect(lambda: FiltersToCriteriaConverter.convert(filters={}, sorts=sorting_with_missing_direction)).to(
            raise_error(MissingDirectionInSortCondition)
        )

    def test_should_fail_when_sorting_has_extra_keys(self) -> None:
        sorting_with_extra_keys = [{"field": "age", "direction": "ascending", "extra": "value"}]

        expect(lambda: FiltersToCriteriaConverter.convert(filters={}, sorts=sorting_with_extra_keys)).to(
            raise_error(SortConditionInvalidStructure)
        )

    def test_should_fail_when_sorting_direction_does_not_exist(self) -> None:
        sorting_with_non_existing_direction = [{"field": "age", "direction": "upwards"}]

        expect(lambda: FiltersToCriteriaConverter.convert(filters={}, sorts=sorting_with_non_existing_direction)).to(
            raise_error(SortDirectionDoesNotExist)
        )
