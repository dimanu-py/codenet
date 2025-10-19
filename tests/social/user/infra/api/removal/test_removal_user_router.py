import json

import pytest
from doublex import ANY_ARG, when
from expects import equal, expect

from src.shared.domain.exceptions.application_error import ApplicationError
from src.social.user.application.removal.user_not_found_error import UserNotFoundError
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.infra.api.removal.removal_user_router import remove_user
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_id_mother import UserIdMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestRemovalUserRouter:
    def setup_method(self) -> None:
        self._user_remover = AsyncStub(UserRemover)
        self._response = None

    async def test_should_return_202_when_user_is_removed(self) -> None:
        user_id = UserIdMother.any().value
        self._stub_successful_removal()

        self._response = await remove_user(
            user_id=user_id,
            user_remover=self._user_remover,
        )

        self._assert_contract_is_met_with(202, {"message": "User removal request has been accepted."})

    async def test_should_return_404_when_user_to_remove_does_not_exist(self) -> None:
        user_id = UserIdMother.any().value
        self._stub_removal_error(UserNotFoundError)

        self._response = await remove_user(
            user_id=user_id,
            user_remover=self._user_remover,
        )

        self._assert_contract_is_met_with(404, {"detail": "User with that id not found"})

    def _stub_successful_removal(self) -> None:
        when(self._user_remover).execute(ANY_ARG).returns(None)

    def _stub_removal_error(self, error: ApplicationError) -> None:
        when(self._user_remover).execute(ANY_ARG).raises(error)

    def _assert_contract_is_met_with(self, expected_status_code: int, expected_body: dict[str, str]):
        expect(self._response.status_code).to(equal(expected_status_code))
        expect(json.loads(self._response.body)).to(equal(expected_body))
