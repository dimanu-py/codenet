import pytest
from expects import equal, expect


@pytest.mark.asyncio
@pytest.mark.unit
class UserModuleRoutersTestConfig:
    _response = None

    def _assert_contract_is_met_with(self, expected_status_code: int, expected_body: dict[str, str]):
        expect(self._response.status_code).to(equal(expected_status_code))
        expect(self._response.detail).to(equal(expected_body))
