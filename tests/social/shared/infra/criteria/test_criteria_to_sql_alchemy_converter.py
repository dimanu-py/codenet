import pytest
from expects import expect, equal

from src.shared.infra.criteria.criteria_to_sql_alchemy_converter import (
    CriteriaToSqlAlchemyConverter,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.shared.domain.criteria.criteria_mother import CriteriaMother


@pytest.mark.integration
class TestCriteriaToSqlAlchemyConverter:
    def test_should_generate_select_query_from_empty_criteria(self) -> None:
        criteria = CriteriaMother.empty()
        converter = CriteriaToSqlAlchemyConverter()

        query = converter.convert(model=UserModel, criteria=criteria)

        expect(query).to(
            equal("SELECT users.id, users.name, users.username, users.email \nFROM users")
        )
