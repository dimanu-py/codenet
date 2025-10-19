import pytest

from tests.social.user.domain.mothers.user_id_mother import UserIdMother


@pytest.fixture
def user_id() -> str:
    return UserIdMother.any().value
