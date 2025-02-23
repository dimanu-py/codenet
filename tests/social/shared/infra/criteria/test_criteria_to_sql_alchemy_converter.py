import pytest
from expects import expect, equal
from sqlalchemy.sql import Select

from src.shared.domain.criteria.filter_operator import FilterOperator
from src.shared.infra.criteria.criteria_to_sql_alchemy_converter import (
    CriteriaToSqlAlchemyConverter,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.shared.domain.criteria.criteria_mother import CriteriaMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


@pytest.mark.integration
class TestCriteriaToSqlAlchemyConverter:
    def setup_method(self) -> None:
        self._converter = CriteriaToSqlAlchemyConverter()

    def test_should_generate_select_query_from_empty_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                "SELECT users.id, users.name, users.username, users.email \n"
                "FROM users"
            )
        )

    def test_should_generate_select_query_with_one_filter(self) -> None:
        user_name = UserNameMother.any()
        criteria = CriteriaMother.with_one_filter(
            "name", FilterOperator.EQUAL, user_name.value
        )
        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name.value}'"
            )
        )

    def test_should_generate_select_query_with_multiple_filters(self) -> None:
        user_name = UserNameMother.any()
        user_username = UserUsernameMother.any()
        criteria = CriteriaMother.create(
            [
                {
                    "field": "name",
                    "operator": FilterOperator.EQUAL,
                    "value": user_name.value,
                },
                {
                    "field": "username",
                    "operator": FilterOperator.EQUAL,
                    "value": user_username.value,
                }
            ]
        )
        query = self.stringify(self._converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name.value}' AND users.username = '{user_username.value}'"
            )
        )

    @staticmethod
    def stringify(query: Select) -> str:
        return query.compile(compile_kwargs={"literal_binds": True}).string
