import pytest
from expects import expect, be_true, raise_error, be_false

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.invalid_criteria import InvalidCriteriaStructure, InvalidExpressionStructure
from src.shared.domain.criteria.operator import Operator, ComparisonOperatorDoesNotExist


@pytest.mark.unit
class TestCriteria:
    def test_should_create_empty_criteria(self) -> None:
        empty_criteria = Criteria.from_primitives(expression={})

        expect(empty_criteria.is_empty()).to(be_true)

    def test_should_create_criteria_with_composite_expression(self) -> None:
        composite_expression = {
            "and": [
                {"field": "age", Operator.EQUALS: "30"},
                {"field": "name", Operator.EQUALS: "John"},
            ]
        }

        criteria = Criteria.from_primitives(expression=composite_expression)

        expect(criteria.is_empty()).to(be_false)

    def test_should_create_criteria_with_comparison_expression(self) -> None:
        comparison_expression = {"field": "age", Operator.GREATER_THAN: "30"}

        criteria = Criteria.from_primitives(expression=comparison_expression)

        expect(criteria.is_empty()).to(be_false)

    def test_should_fail_when_expression_is_not_a_dictionary(self) -> None:
        invalid_expression = "not_a_dictionary"

        expect(lambda: Criteria.from_primitives(expression=invalid_expression)).to(raise_error(InvalidCriteriaStructure))

    def test_should_fail_when_expression_is_not_composite_nor_comparison(self) -> None:
        invalid_expression = {"invalid": "expression"}

        expect(lambda: Criteria.from_primitives(expression=invalid_expression)).to(raise_error(InvalidExpressionStructure))

    def test_should_fail_when_condition_in_composite_expression_does_not_have_valid_structure(self) -> None:
        invalid_composite_expression = {
            "and": [
                {"field": "age", Operator.EQUALS: "30"},
                {"invalid": "condition"},
            ]
        }

        expect(lambda: Criteria.from_primitives(expression=invalid_composite_expression)).to(raise_error(InvalidExpressionStructure))

    def test_should_fail_when_passing_non_existing_operator(self) -> None:
        expression_with_non_existing_operator = {
            "field": "age",
            "multiplication": "30"
        }

        expect(lambda: Criteria.from_primitives(expression=expression_with_non_existing_operator)).to(raise_error(ComparisonOperatorDoesNotExist))