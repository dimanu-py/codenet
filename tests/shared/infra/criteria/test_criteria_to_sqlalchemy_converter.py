import pytest
from expects import equal, expect
from sqlalchemy.sql.selectable import Select

from src.shared.domain.criteria.condition.operator import Operator
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import (
    CriteriaToSqlalchemyConverter,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.mark.unit
class TestCriteriaToSqlalchemyConverter:
    def setup_method(self) -> None:
        self._converter = CriteriaToSqlalchemyConverter()

    def test_should_generate_select_query_from_empty_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(equal("SELECT users.id, users.name, users.username, users.email \nFROM users"))

    def test_should_generate_select_query_with_one_filter(self) -> None:
        user_name = UserNamePrimitivesMother.any()

        criteria = CriteriaMother.with_one_condition("name", Operator.EQUAL, user_name)
        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name}'"
            )
        )

    def test_should_generate_select_query_with_multiple_filters_with_and_logical_operator(
        self,
    ) -> None:
        user_name = UserNamePrimitivesMother.any()
        user_username = UserUsernamePrimitivesMother.any()
        criteria = CriteriaMother.with_conditions(
            {
                "and": [
                    {
                        "field": "name",
                        Operator.EQUAL: user_name,
                    },
                    {
                        "field": "username",
                        Operator.EQUAL: user_username,
                    },
                ]
            }
        )
        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name}' AND users.username = '{user_username}'"
            )
        )

    def test_should_generate_select_query_with_multiple_filters_with_or_logical_operator(
        self,
    ) -> None:
        user_name = UserNamePrimitivesMother.any()
        user_username = UserUsernamePrimitivesMother.any()
        criteria = CriteriaMother.with_conditions(
            {
                "or": [
                    {
                        "field": "name",
                        Operator.EQUAL: user_name,
                    },
                    {
                        "field": "username",
                        Operator.EQUAL: user_username,
                    },
                ]
            }
        )
        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name}' OR users.username = '{user_username}'"
            )
        )

    def test_should_generate_negated_query(self) -> None:
        user_name = UserNamePrimitivesMother.any()
        criteria = CriteriaMother.with_one_condition("name", Operator.NOT_EQUAL, user_name)

        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name != '{user_name}'"
            )
        )

    def test_should_generate_query_with_contains(self) -> None:
        user_name = UserNamePrimitivesMother.any()
        criteria = CriteriaMother.with_one_condition("name", Operator.CONTAINS, user_name)

        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE lower(users.name) LIKE lower('%{user_name}%')"
            )
        )

    def test_should_generate_query_with_nested_filters(self) -> None:
        user_name = UserNamePrimitivesMother.any()
        first_username = UserUsernamePrimitivesMother.any()
        second_username = UserUsernamePrimitivesMother.any()

        criteria = CriteriaMother.with_conditions(
            {
                "and": [
                    {
                        "field": "name",
                        Operator.EQUAL: user_name,
                    },
                    {
                        "or": [
                            {
                                "field": "username",
                                Operator.EQUAL: first_username,
                            },
                            {
                                "field": "username",
                                Operator.EQUAL: second_username,
                            },
                        ]
                    },
                ]
            }
        )

        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name}' AND (users.username = '{first_username}' OR users.username = '{second_username}')"  # noqa: E501
            )
        )

    @staticmethod
    def stringify(query: Select) -> str:
        return query.compile(compile_kwargs={"literal_binds": True}).string
