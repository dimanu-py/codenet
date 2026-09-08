from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter import Filter, Filters
from src.shared.domain.criteria.operator import Operator


class AccountByLoginIdentifierCriteria:
    @classmethod
    def for_login_identifier(cls, login: str) -> Criteria:
        is_email = Criteria(filters=Filters([Filter(field="email", operator=Operator.EQUALS, value=login)]))
        is_username = Criteria(filters=Filters([Filter(field="username", operator=Operator.EQUALS, value=login)]))
        return is_email | is_username
