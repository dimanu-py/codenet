from typing import override

from src.auth.session.domain.token_issuer import TokenIssuer


class FakeTokenIssuer(TokenIssuer):
    def __init__(self, token: dict) -> None:
        self._token = token
        self.received_account_id: str | None = None

    @override
    async def generate_token(self, account_id: str) -> dict:
        self.received_account_id = account_id
        return self._token
