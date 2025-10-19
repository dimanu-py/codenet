import json

import pytest
from doublex import ANY_ARG, when
from expects import equal, expect

from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.infra.api.removal.removal_user_router import remove_user
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_id_mother import UserIdMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestRemovalUserRouter:
    async def test_should_return_202_when_user_is_removed(self) -> None:
        user_id = UserIdMother.any().value
        user_remover = AsyncStub(UserRemover)

        when(user_remover).execute(ANY_ARG).returns(None)

        response = await remove_user(
            user_id=user_id,
            user_remover=user_remover,
        )

        expect(response.status_code).to(equal(202))
        expect(json.loads(response.body)).to(equal({"message": "User removal request has been accepted."}))
