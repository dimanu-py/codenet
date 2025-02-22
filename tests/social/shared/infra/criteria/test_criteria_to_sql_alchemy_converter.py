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


@pytest.mark.integration
class TestCriteriaToSqlAlchemyConverter:
    def test_should_generate_select_query_from_empty_criteria(self) -> None:
        criteria = CriteriaMother.empty()
        converter = CriteriaToSqlAlchemyConverter()

        query = self.stringify(converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                "SELECT users.id, users.name, users.username, users.email \nFROM users"
            )
        )

    def test_should_generate_select_query_with_one_filter(self) -> None:
        user_name = UserNameMother.any()
        criteria = CriteriaMother.with_one_filter(
            "name", FilterOperator.EQUAL, user_name.value
        )
        converter = CriteriaToSqlAlchemyConverter()

        query = self.stringify(converter.convert(model=UserModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT users.id, users.name, users.username, users.email \n"
                f"FROM users \n"
                f"WHERE users.name = '{user_name.value}'"
            )
        )

    @staticmethod
    def stringify(query: Select) -> str:
        return query.compile(compile_kwargs={"literal_binds": True}).string
