from src.shared.domain.criteria.expression import ComparisonExpression, CompositeExpression
from tests.shared.domain.criteria.mothers.field_mother import FieldMother
from tests.shared.domain.criteria.mothers.logical_operator_mother import LogicalOperatorMother
from tests.shared.domain.criteria.mothers.operator_mother import OperatorMother
from tests.shared.domain.criteria.mothers.value_mother import ValueMother


class ComparisonExpressionMother:
    @staticmethod
    def any() -> ComparisonExpression:
        return ComparisonExpression(
            field=FieldMother.any(),
            operator=OperatorMother.any(),
            value=ValueMother.any(),
        )


class CompositeExpressionMother:
    @staticmethod
    def any() -> CompositeExpression:
        return CompositeExpression(
            operator=LogicalOperatorMother.any(),
            conditions=[ComparisonExpressionMother.any()],
        )
