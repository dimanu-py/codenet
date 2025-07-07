from tests.social.user.application.removal.user_removal_command_mother import (
    UserRemovalCommandMother,
)
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.user_mother import UserMother


class TestUserRemoval(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_remover = UserRemover(repository=self._repository)

    async def test_should_remove_existing_user(self) -> None:
        user = UserMother.any()
        self._should_find(user)
        command = UserRemovalCommandMother.create(user_id=user.id.value)

        self._should_remove(user)

        await self._user_remover(command)
