import pytest
from expects import equal, expect
from object_mother import StringPrimitivesMother
from sqlalchemy.sql.selectable import Select

from src.shared.domain.criteria.filters_to_criteria_converter import FiltersToCriteriaConverter
from src.shared.domain.criteria.operator import Operator
from src.shared.domain.criteria.sort_direction import SortDirection
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import (
    CriteriaToSqlalchemyConverter,
)
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.shared.infra.criteria.dummy_model import DummyModel


@pytest.mark.unit
class TestCriteriaToSqlalchemyConverter:
    def setup_method(self) -> None:
        self._converter = CriteriaToSqlalchemyConverter()

    def test_should_generate_select_query_from_empty_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(equal("SELECT test_table.id, test_table.name, test_table.username \nFROM test_table"))

    def test_should_generate_select_query_with_one_filter(self) -> None:
        user_name = StringPrimitivesMother.any()
        criteria = CriteriaMother.with_single_filter("name", Operator.EQUALS, user_name)

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name = '{user_name}'"
            )
        )

    def test_should_generate_select_query_with_multiple_filters_with_and_logical_operator(
        self,
    ) -> None:
        user_name = StringPrimitivesMother.any()
        user_username = StringPrimitivesMother.any()
        criteria = CriteriaMother.with_multiple_filters(
            {
                "and": [
                    {
                        "field": "name",
                        Operator.EQUALS: user_name,
                    },
                    {
                        "field": "username",
                        Operator.EQUALS: user_username,
                    },
                ]
            }
        )

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name = '{user_name}' AND test_table.username = '{user_username}'"
            )
        )

    def test_should_generate_select_query_with_multiple_filters_with_or_logical_operator(
        self,
    ) -> None:
        user_name = StringPrimitivesMother.any()
        user_username = StringPrimitivesMother.any()
        criteria = CriteriaMother.with_multiple_filters(
            {
                "or": [
                    {
                        "field": "name",
                        Operator.EQUALS: user_name,
                    },
                    {
                        "field": "username",
                        Operator.EQUALS: user_username,
                    },
                ]
            }
        )

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name = '{user_name}' OR test_table.username = '{user_username}'"
            )
        )

    def test_should_generate_negated_query(self) -> None:
        user_name = StringPrimitivesMother.any()
        criteria = CriteriaMother.with_single_filter("name", Operator.NOT_EQUALS, user_name)

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name != '{user_name}'"
            )
        )

    def test_should_generate_query_with_contains(self) -> None:
        user_name = StringPrimitivesMother.any()
        criteria = CriteriaMother.with_single_filter("name", Operator.CONTAINS, user_name)

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE lower(test_table.name) LIKE lower('%{user_name}%')"
            )
        )

    def test_should_generate_query_with_nested_filters(self) -> None:
        user_name = StringPrimitivesMother.any()
        first_username = StringPrimitivesMother.any()
        second_username = StringPrimitivesMother.any()

        criteria = CriteriaMother.with_multiple_filters(
            {
                "and": [
                    {
                        "field": "name",
                        Operator.EQUALS: user_name,
                    },
                    {
                        "or": [
                            {
                                "field": "username",
                                Operator.EQUALS: first_username,
                            },
                            {
                                "field": "username",
                                Operator.EQUALS: second_username,
                            },
                        ]
                    },
                ]
            }
        )

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name = '{user_name}' AND (test_table.username = '{first_username}' OR test_table.username = '{second_username}')"  # noqa: E501
            )
        )

    def test_should_generate_query_with_one_sorting_condition_and_no_filters(self) -> None:
        criteria = CriteriaMother.with_sorting(sorts=[{"field": "name", "direction": SortDirection.ASCENDING}])

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                "SELECT test_table.id, test_table.name, test_table.username \n"
                "FROM test_table "
                "ORDER BY test_table.name ASC"
            )
        )

    def test_should_generate_query_with_multiple_sorting_conditions_and_no_filters(self) -> None:
        criteria = CriteriaMother.with_sorting(
            sorts=[
                {"field": "name", "direction": SortDirection.ASCENDING},
                {"field": "username", "direction": SortDirection.DESCENDING},
            ]
        )

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                "SELECT test_table.id, test_table.name, test_table.username \n"
                "FROM test_table "
                "ORDER BY test_table.name ASC, test_table.username DESC"
            )
        )

    def test_should_generate_query_with_filters_and_sorting(self) -> None:
        criteria = FiltersToCriteriaConverter.convert(
            filters={
                "field": "name",
                Operator.EQUALS: "John Doe",
            },
            sorts=[
                {"field": "username", "direction": SortDirection.DESCENDING},
            ],
        )

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=criteria))

        expect(query).to(
            equal(
                "SELECT test_table.id, test_table.name, test_table.username \n"
                "FROM test_table \n"
                "WHERE test_table.name = 'John Doe' "
                "ORDER BY test_table.username DESC"
            )
        )

    def test_should_generate_query_composing_criteria_with_and_operator(self) -> None:
        user_name = StringPrimitivesMother.any()
        user_username = StringPrimitivesMother.any()
        matches_name = CriteriaMother.with_single_filter("name", Operator.EQUALS, user_name)
        matches_username = CriteriaMother.with_single_filter("username", Operator.EQUALS, user_username)

        query = self.stringify(self._converter.convert(model=DummyModel, criteria=matches_name & matches_username))

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.name = '{user_name}' AND test_table.username = '{user_username}'"
            )
        )

    def test_should_generate_query_composing_criteria_with_or_operator(self) -> None:
        first_username = StringPrimitivesMother.any()
        second_username = StringPrimitivesMother.any()
        matches_first_username = CriteriaMother.with_single_filter("username", Operator.EQUALS, first_username)
        matches_second_username = CriteriaMother.with_single_filter("username", Operator.EQUALS, second_username)

        query = self.stringify(
            self._converter.convert(model=DummyModel, criteria=matches_first_username | matches_second_username)
        )

        expect(query).to(
            equal(
                f"SELECT test_table.id, test_table.name, test_table.username \n"
                f"FROM test_table \n"
                f"WHERE test_table.username = '{first_username}' OR test_table.username = '{second_username}'"
            )
        )

    @staticmethod
    def stringify(query: Select) -> str:
        return query.compile(compile_kwargs={"literal_binds": True}).string
