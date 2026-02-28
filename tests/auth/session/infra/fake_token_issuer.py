from typing import override

from src.auth.session.domain.token_issuer import TokenIssuer


class FakeTokenIssuer(TokenIssuer):
    def __init__(self, token: dict) -> None:
        self._token = token

    @override
    async def generate_token(self, identification: str) -> dict:
        return self._token
