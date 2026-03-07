from typing import Self

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.logical_operator import LogicalOperator
from src.shared.domain.criteria.operator import Operator


class AccountByLoginIdentifierCriteria(Criteria):
    @classmethod
    def for_login_identifier(cls, login: str) -> Self:
        return cls.from_primitives(
            expression={
                LogicalOperator.OR: [
                    {
                        "field": "email",
                        Operator.EQUALS: login,
                    },
                    {
                        "field": "username",
                        Operator.EQUALS: login,
                    },
                ]
            }
        )
