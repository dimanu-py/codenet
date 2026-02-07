import pytest
from expects import equal, expect


@pytest.mark.asyncio
@pytest.mark.unit
class UserModuleRoutersTestConfig:
    _response = None

    def _assert_contract_is_met_on_success(
        self, expected_status_code: int, expected_body: dict[str, str] | list[dict]
    ) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.data).to(equal(expected_body))

    def _assert_contract_is_met_on_error(self, expected_status_code: int, expected_message: str) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.error["message"]).to(equal(expected_message))
