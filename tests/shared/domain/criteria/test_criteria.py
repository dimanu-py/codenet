import pytest
from expects import be_false, be_true, expect, raise_error

from src.shared.domain.criteria.criteria import Criteria
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
class TestCriteria:
    def test_should_create_empty_criteria(self) -> None:
        empty_criteria = Criteria.from_primitives(expression={})

        expect(empty_criteria.is_empty()).to(be_true)

    @pytest.mark.parametrize(
        "expression",
        [
            pytest.param(
                {"and": [{"field": "age", Operator.EQUALS: "30"}, {"field": "name", Operator.EQUALS: "John"}]},
                id="composite_expression",
            ),
            pytest.param({"field": "age", Operator.GREATER_THAN: "30"}, id="comparison_expression"),
        ],
    )
    def test_should_create_criteria_with_expression(self, expression: dict) -> None:
        criteria = Criteria.from_primitives(expression=expression)

        expect(criteria.is_empty()).to(be_false)

    def test_should_create_criteria_without_sorting_by_default(self) -> None:
        criteria_without_sorts = Criteria.from_primitives(expression={})

        expect(criteria_without_sorts.has_sorting()).to(be_false)

    def test_should_create_criteria_with_empty_sorting(self) -> None:
        criteria_with_empty_sorts = Criteria.from_primitives(
            expression={},
            sorts=[],
        )

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
        criteria_with_sorts = Criteria.from_primitives(
            expression={"field": "age", Operator.EQUALS: "30"},
            sorts=sorting,
        )

        expect(criteria_with_sorts.has_sorting()).to(be_true)

    def test_should_fail_when_expression_is_not_a_dictionary(self) -> None:
        invalid_expression = "not_a_dictionary"

        expect(lambda: Criteria.from_primitives(expression=invalid_expression)).to(
            raise_error(InvalidCriteriaStructure)
        )

    def test_should_fail_when_expression_is_not_composite_nor_comparison(self) -> None:
        invalid_expression = {"invalid": "expression"}

        expect(lambda: Criteria.from_primitives(expression=invalid_expression)).to(
            raise_error(InvalidExpressionStructure)
        )

    def test_should_fail_when_condition_in_composite_expression_does_not_have_valid_structure(self) -> None:
        invalid_composite_expression = {
            "and": [
                {"field": "age", Operator.EQUALS: "30"},
                {"invalid": "condition"},
            ]
        }

        expect(lambda: Criteria.from_primitives(expression=invalid_composite_expression)).to(
            raise_error(InvalidExpressionStructure)
        )

    def test_should_fail_when_passing_non_existing_operator(self) -> None:
        expression_with_non_existing_operator = {"field": "age", "multiplication": "30"}

        expect(lambda: Criteria.from_primitives(expression=expression_with_non_existing_operator)).to(
            raise_error(ComparisonOperatorDoesNotExist)
        )

    def test_should_fail_when_sorting_has_missing_field(self) -> None:
        sorting_with_missing_field = [{"direction": "ascending"}]

        expect(lambda: Criteria.from_primitives(expression={}, sorts=sorting_with_missing_field)).to(
            raise_error(MissingFieldInSortCondition)
        )

    def test_should_fail_when_sorting_has_missing_direction(self) -> None:
        sorting_with_missing_direction = [{"field": "age"}]

        expect(lambda: Criteria.from_primitives(expression={}, sorts=sorting_with_missing_direction)).to(
            raise_error(MissingDirectionInSortCondition)
        )

    def test_should_fail_when_sorting_has_extra_keys(self) -> None:
        sorting_with_extra_keys = [{"field": "age", "direction": "ascending", "extra": "value"}]

        expect(lambda: Criteria.from_primitives(expression={}, sorts=sorting_with_extra_keys)).to(
            raise_error(SortConditionInvalidStructure)
        )

    def test_should_fail_when_sorting_direction_does_not_exist(self) -> None:
        sorting_with_non_existing_direction = [{"field": "age", "direction": "upwards"}]

        expect(lambda: Criteria.from_primitives(expression={}, sorts=sorting_with_non_existing_direction)).to(
            raise_error(SortDirectionDoesNotExist)
        )
